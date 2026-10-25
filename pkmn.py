from dataclasses import dataclass, astuple, fields
from enum import IntEnum
from io import BytesIO
from bisect import bisect_right
import struct
from typing import ClassVar, Protocol, Self, cast, get_type_hints
from pathlib import Path
import argparse

def existing_file(path: str) -> Path:
    p = Path(path)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"Not an existing file: {path}")
    return p


def get_parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("savefile", type=existing_file)
    return parser.parse_args()


class InvalidSave(Exception):
    pass


class BinaryFileLike(Protocol):
    def read(self, size: int = -1, /) -> bytes: ...
    def write(self, data: bytes, /) -> int: ...

    def tell(self) -> int: ...
    def seek(self, offset: int, whence: int = 0, /) -> int: ...

    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def seekable(self) -> bool: ...

    def flush(self) -> None: ...
    def close(self) -> None: ...


# llm generated + human reviewed
class SectionedBinaryFileLike:
    def __init__(self, file: BinaryFileLike, sections: list[Section]) -> None:
        self._file = file
        self._sections = list(sections)
        self._position = 0
        self._closed = False

        # Virtual starting offset of each section, plus the final EOF.
        self._starts = [0]
        for section in self._sections:
            size = section.size()
            self._starts.append(self._starts[-1] + size)

        self._size = self._starts[-1]

    def readable(self) -> bool:
        return not self._closed and self._file.readable()

    def writable(self) -> bool:
        return not self._closed and self._file.writable()

    def seekable(self) -> bool:
        return not self._closed and self._file.seekable()

    def tell(self) -> int:
        self._check_closed()
        return self._position

    def seek(self, offset: int, whence: int = 0) -> int:
        self._check_closed()

        if whence == 0:
            position = offset
        elif whence == 1:
            position = self._position + offset
        elif whence == 2:
            position = self._size + offset
        else:
            raise ValueError("Invalid whence")

        if position < 0:
            raise ValueError("Negative seek position")

        self._position = position
        return position

    def _locate(self, position: int) -> tuple[int, int]:
        """Return (section index, offset within section)."""
        index = bisect_right(self._starts, position) - 1
        return index, position - self._starts[index]

    def read(self, size: int = -1) -> bytes:
        self._check_closed()

        if not self.readable():
            raise OSError("Stream is not readable")

        remaining = max(0, self._size - self._position)
        if size is not None and size >= 0:
            remaining = min(remaining, size)

        result = bytearray()

        while remaining:
            index, local = self._locate(self._position)
            section = self._sections[index]

            count = min(
                remaining,
                self._starts[index + 1] - self._position,
            )

            self._file.seek(section.offset + local)
            chunk = self._file.read(count)

            if not chunk:
                break

            result.extend(chunk)
            self._position += len(chunk)
            remaining -= len(chunk)

        return bytes(result)

    def write(self, data: bytes | bytearray | memoryview) -> int:
        self._check_closed()

        if not self.writable():
            raise OSError("Stream is not writable")

        view = memoryview(data).cast("B")

        if self._position + len(view) > self._size:
            raise ValueError("Write exceeds virtual file size")

        written = 0

        while written < len(view):
            index, local = self._locate(self._position)
            section = self._sections[index]

            count = min(
                len(view) - written,
                self._starts[index + 1] - self._position,
            )

            self._file.seek(section.offset + local)
            n = self._file.write(view[written:written + count].tobytes())

            if n is None:
                raise BlockingIOError(
                    0, "Underlying stream could not accept data", written
                )
            if n <= 0:
                raise OSError("Underlying stream made no write progress")

            self._position += n
            written += n

        return written

    def flush(self) -> None:
        self._check_closed()
        self._file.flush()

    def close(self) -> None:
        self._closed = True

    def _check_closed(self) -> None:
        if self._closed:
            raise ValueError("I/O operation on closed file")


class PkmnSpecies(IntEnum):
    pass

class PkmnItem(IntEnum):
    pass

class PkmnMove(IntEnum):
    pass

class PkmnLocation(IntEnum):
    pass

class PkmnPPBonus(Bitfield):
    pass

class PkmnPokerus(Bitfield):
    pass

class PkmnOrigins(Bitfield):
    pass

class PkmnIVsEggAbility(Bitfield):
    pass

class PkmnRibbonsObedience(Bitfield):
    pass

class LevelHelper:
    @staticmethod
    def exp2lvl(exp: int, species: PkmnSpecies) -> tuple[int, int]:
        pass

    @staticmethod
    def lvl2exp(lvl: int, exp: int, species: PkmnSpecies) -> int:
        pass

@dataclass
class PkmnData:
    _fmt: ClassVar[str]

    @staticmethod
    def _apply_key(data: bytes, key: int) -> bytes:
        encrypted = struct.unpack("<3I", data)
        decrypted = [b ^ key for b in encrypted]
        return struct.pack("<3I", *decrypted)

    def _pack(self) -> bytes:
        return struct.pack(self._fmt, *astuple(self))

    @classmethod
    def deserialize(cls, file: BinaryFileLike, key: int) -> Self:
        data = cls._apply_key(file.read(12), key)
        values = struct.unpack(cls._fmt, data)
        hints = get_type_hints(cls)
        return cls(*[hints[field.name](value)  for field, value in zip(fields(cls), values)])

    def serialize(self, file: BinaryFileLike, key: int) -> None:
        file.write(self._apply_key(self._pack(), key))

    def checksum(self) -> int:
        chunks = struct.unpack("<6H", self._pack())
        return sum(chunks) & 0xFFFF


@dataclass
class PkmnGrowth(PkmnData):
    _fmt: ClassVar[str] = "<HHIBBH"

    species: PkmnSpecies
    item_held: PkmnItem
    experience: int
    pp_bonuses: PkmnPPBonus
    friendship: int
    unused: int


@dataclass
class PkmnAttacks(PkmnData):
    _fmt: ClassVar[str] = "<HHHHBBBB"

    move1: PkmnMove
    move2: PkmnMove
    move3: PkmnMove
    move4: PkmnMove
    pp1: int
    pp2: int
    pp3: int
    pp4: int


@dataclass
class PkmnEVData(PkmnData):
    _fmt: ClassVar[str] = "<12B"

    hp: int
    attack: int
    defense: int
    speed: int
    sp_attack: int
    sp_defense: int
    coolness: int
    beauty: int
    cuteness: int
    smartness: int
    toughness: int
    feel: int


@dataclass
class PkmnMisc(PkmnData):
    _fmt: ClassVar[str] = "<BBHII"

    pokerus: PkmnPokerus
    met_location: PkmnLocation
    origins_info: PkmnOrigins
    ivs_egg_ability: PkmnIVsEggAbility
    ribbons_obedience: PkmnRibbonsObedience


@dataclass
class PokemonData:
    growth: PkmnGrowth
    attacks: PkmnAttacks
    ev_data: PkmnEVData
    misc: PkmnMisc

    @classmethod
    def _get_offsets(cls, pv: int) -> list[int]:
        match(pv % 24):
            case 0: return [0,12,24,36]
            case 1: return [0,12,36,24]
            case 2: return [0,24,12,36]
            case 3: return [0,24,36,12]
            case 4: return [0,36,12,24]
            case 5: return [0,36,24,12]
            case 6: return [12,0,24,36]
            case 7: return [12,0,36,24]
            case 8: return [12,24,0,36]
            case 9: return [12,24,36,0]
            case 10: return [12,36,0,24]
            case 11: return [12,36,24,0]
            case 12: return [24,0,12,36]
            case 13: return [24,0,36,12]
            case 14: return [24,12,0,36]
            case 15: return [24,12,36,0]
            case 16: return [24,36,0,12]
            case 17: return [24,36,12,0]
            case 18: return [36,0,12,24]
            case 19: return [36,0,24,12]
            case 20: return [36,12,0,24]
            case 21: return [36,12,24,0]
            case 22: return [36,24,0,12]
            case 23: return [36,24,12,0]
            case _: assert False

    def checksum(self) -> int:
        return (self.growth.checksum() + self.attacks.checksum() + self.ev_data.checksum() + self.misc.checksum()) & 0xFFFF

    def serialize(self, file: BinaryFileLike, otid: int, pv: int) -> None:
        key = otid ^ pv

        start = file.tell()
        order = self._get_offsets(pv)
        offsets = [order.index(i * 12) * 12 for i in range(4)]

        file.seek(start + offsets[0])
        self.growth.serialize(file, key)

        file.seek(start + offsets[1])
        self.attacks.serialize(file, key)

        file.seek(start + offsets[2])
        self.ev_data.serialize(file, key)

        file.seek(start + offsets[3])
        self.misc.serialize(file, key)

    @classmethod
    def deserialize(cls, file: BinaryFileLike, otid: int, pv: int) -> Self:
        key = otid ^ pv

        start = file.tell()
        order = cls._get_offsets(pv)
        offsets = [order.index(i * 12) * 12 for i in range(4)]

        file.seek(start + offsets[0])
        growth = PkmnGrowth.deserialize(file, key)

        file.seek(start + offsets[1])
        attacks = PkmnAttacks.deserialize(file, key)

        file.seek(start + offsets[2])
        ev_data = PkmnEVData.deserialize(file, key)

        file.seek(start + offsets[3])
        misc = PkmnMisc.deserialize(file, key)

        return cls(growth, attacks, ev_data, misc)


@dataclass
class Pokemon:
    personality_value: int
    original_trainer_id: int
    nickname: bytes
    language: int
    misc_flags: int
    original_trainer_name: bytes
    markings: int
    data: PokemonData

    HEADER_FORMAT = "<II10sBB7sBHH"

    def serialize(self, file: BinaryFileLike) -> None:
        file.write(struct.pack(
            self.HEADER_FORMAT,
            self.personality_value,
            self.original_trainer_id,
            self.nickname,
            self.language,
            self.misc_flags,
            self.original_trainer_name,
            self.markings,
            self.data.checksum(),
            0,
        ))
        self.data.serialize(file, self.original_trainer_id, self.personality_value)

    @classmethod
    def serialize_empty(cls, file: BinaryFileLike) -> None:
        file.write(b"\0"*80)

    @classmethod
    def deserialize(cls, file: BinaryFileLike) -> None | Self:
        pv, otid, nick, lang, flags, otname, marks, chck, _ = struct.unpack(
            cls.HEADER_FORMAT,
            file.read(struct.calcsize(cls.HEADER_FORMAT))
        )

        # bit 1 explicitly used to check for "empty spaces"
        if flags & 0b0000_0010 == 0:
            return None

        data = PokemonData.deserialize(file, otid, pv)

        if data.checksum() != chck:
            raise InvalidSave("Pokemon checksum does not match")

        return cls(pv, otid, nick, lang, flags, otname, marks, data)


@dataclass
class PCBuffer:
    pokemon: dict[int, None | Pokemon]
    _sections: list[Section]

    def serialize(self, file: BinaryFileLike) -> list[Section]:
        virt_file = SectionedBinaryFileLike(file, self._sections)

        start = 0x0004
        for i, pokemon in self.pokemon.items():
            virt_file.seek(start + i * 80)
            if pokemon is None:
                Pokemon.serialize_empty(virt_file)
            else:
                pokemon.serialize(virt_file)

        return self._sections

    @classmethod
    def deserialize(cls, file: BinaryFileLike, sections: list[Section]) -> Self:
        virt_file = SectionedBinaryFileLike(file, sections)

        pokemon: dict[int, None | Pokemon] = {}
        start = 0x0004
        for i in range(420):
            virt_file.seek(start + i * 80)
            pokemon[i] = Pokemon.deserialize(virt_file)

        return cls(pokemon, sections)


@dataclass
class Section:
    offset: int
    section_id: int
    index: int

    SECTION_CHECKSUM_SIZE = {
        0: 3884,
        1: 3968,
        2: 3968,
        3: 3968,
        4: 3848,
        5: 3968,
        6: 3968,
        7: 3968,
        8: 3968,
        9: 3968,
        10: 3968,
        11: 3968,
        12: 3968,
        13: 2000,
    }

    def size(self) -> int:
        return self.SECTION_CHECKSUM_SIZE[self.section_id]

    @classmethod
    def _compute_checksum(cls, offset: int, section_id: int, file: BinaryFileLike) -> int:
        file.seek(offset)

        if section_id not in cls.SECTION_CHECKSUM_SIZE:
            raise InvalidSave(f"invalid section id {section_id}")

        size = cls.SECTION_CHECKSUM_SIZE[section_id]
        chunks = size // 4

        res = 0
        for _ in range(chunks):
            res += struct.unpack(f"<I", file.read(4))[0]
            res &= 0xFFFF_FFFF

        return ((res >> 16) + (res & 0xFFFF)) & 0xFFFF

    def serialize(self, file: BinaryFileLike) -> None:
        checksum = self._compute_checksum(self.offset, self.section_id, file)
        file.seek(self.offset + 0x0FF6)
        file.write(struct.pack("<H", checksum))

    @classmethod
    def deserialize(cls, file: BinaryFileLike) -> Self:
        offset = file.tell()

        file.seek(0x0FF4, 1)
        section_id, checksum, signature, index = struct.unpack("<2H2I", file.read(2*2 + 2*4))

        if signature != 0x08012025:
            raise InvalidSave("Section signature does not match")

        actual_checksum = cls._compute_checksum(offset, section_id, file)
        if checksum != actual_checksum:
            raise InvalidSave("Section checksum does not match")

        return cls(offset, section_id, index)


@dataclass
class SaveSlot:
    first_section: int
    index: int
    pc_buffer: PCBuffer

    def serialize(self, file: BinaryFileLike) -> None:
        sections = self.pc_buffer.serialize(file)
        shifted_sections = sections[self.first_section:] + sections[:self.first_section]
        for section in shifted_sections:
            section.serialize(file)

    @classmethod
    def deserialize(cls, file: BinaryFileLike) -> Self:
        start = file.tell()

        sections: list[Section] = []
        for i in range(14):
            file.seek(start + i * 0x1000)
            section = Section.deserialize(file)
            sections.append(section)

        first_section = sections[0].section_id
        index = sections[-1].index

        section_zero_index = None
        for i, section in enumerate(sections):
            if section.section_id == 0:
                section_zero_index = i
                break
        if section_zero_index is None:
            raise InvalidSave("Missing section zero")

        sorted_sections = sections[section_zero_index:] + sections[:section_zero_index]

        if [s.section_id for s in sorted_sections] != list(range(14)):
            raise InvalidSave("Invalid section ids")
        if len(set(s.index for s in sorted_sections)) != 1:
            raise InvalidSave("Inconsistent save indices")

        pc_buffer = PCBuffer.deserialize(file, sorted_sections[5:])
        return cls(first_section, index, pc_buffer)


class SaveSlotEnum(IntEnum):
    SLOT_1 = 1
    SLOT_2 = 2


@dataclass
class PkmnSave:
    inner: SaveSlot
    slot: SaveSlotEnum

    def serialize(self, file: BinaryFileLike) -> None:
        if self.slot == SaveSlotEnum.SLOT_1:
            file.seek(0x000000)
        elif self.slot == SaveSlotEnum.SLOT_2:
            file.seek(0x00E000)

        self.inner.serialize(file)

    @classmethod
    def _get_valid_slot(cls, file: BinaryFileLike) -> tuple[SaveSlot, SaveSlotEnum]:
        errs: list[InvalidSave] = []

        slot1: None | SaveSlot = None
        try:
            file.seek(0x000000)
            slot1 = SaveSlot.deserialize(file)
        except InvalidSave as e:
            errs.append(e)

        slot2: None | SaveSlot = None
        try:
            file.seek(0x00E000)
            slot2 = SaveSlot.deserialize(file)
        except InvalidSave as e:
            errs.append(e)

        if slot1 is None and slot2 is None:
            raise InvalidSave("Savefile is corrupted.") from ExceptionGroup("Savefile is corrupted.", errs)
        if slot1 is None:
            return cast(SaveSlot, slot2), SaveSlotEnum.SLOT_2
        if slot2 is None:
            return cast(SaveSlot, slot1), SaveSlotEnum.SLOT_1

        if slot1.index > slot2.index:
            return slot1, SaveSlotEnum.SLOT_1
        return slot2, SaveSlotEnum.SLOT_2

    @classmethod
    def deserialize(cls, file: BinaryFileLike) -> Self:
        slot, which = cls._get_valid_slot(file)
        return cls(slot, which)

def load(file: str) -> PkmnSave:
    with open(file, 'rb') as f:
        return PkmnSave.deserialize(f)

def save(file: str, save: PkmnSave) -> None:
    with open(file, 'wb') as f:
        save.serialize(f)

def main():
    args = get_parsed_args()
    with open(args.savefile, 'rb') as f:
        data = f.read()

    dataio = BytesIO(data)
    savefile = PkmnSave.deserialize(dataio)
    assert data == dataio.getvalue()

    savefile.serialize(dataio)
    try:
        assert data == dataio.getvalue()
    except:
        with open(args.savefile.with_suffix(".roundtrip"), "wb") as f:
            f.write(dataio.getvalue())
        raise


if __name__ == '__main__':
    exit(main())
