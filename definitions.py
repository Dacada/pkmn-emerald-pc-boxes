from enum import Enum, auto, nonmember, IntEnum
from typing import Self, Generic, overload, TypeVar

T = TypeVar("T", bound=int)
class Bits(Generic[T]):
    def __init__(self, width: int, type_: type[T]):
        self.width = width
        self.offset = 0  # initialized by owner class
        self.type = type_

    @overload
    def __get__(self, instance: None, _: type) -> Self: ...

    @overload
    def __get__(self, instance: int, _: type) -> T: ...

    def __get__(self, instance, _):
        if instance is None:
            return self

        mask = (1 << self.width) - 1
        value = (int(instance) >> self.offset) & mask
        return self.type(value)


class Bitfield(int):
    width = None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.width is None:
            raise ValueError("width must be defined")

        offset = 0
        fields = {}
        for name, field in cls.__dict__.items():
            if isinstance(field, Bits):
                field.offset = offset
                fields[name] = field
                offset += field.width

        if offset > cls.width:
            raise ValueError("fields do not fit in width")

        cls._fields = fields

    def __new__(cls, value=0, **kwargs):
        if kwargs:
            value = int(value)

            for name, field_value in kwargs.items():
                if name not in cls._fields:
                    raise TypeError(f"Unknown field: {name}")

                field = cls._fields[name]
                mask = (1 << field.width) - 1

                if not 0 <= field_value <= mask:
                    raise ValueError(f"{name} out of range")

                value = (
                    (value & ~(mask << field.offset))
                    | (field_value << field.offset)
                )

        if cls.width is not None and not 0 <= value < (1 << cls.width):
            raise ValueError("Integer exceeds bitfield width")

        return super().__new__(cls, value)

    def replace(self, **kwargs):
        return type(self)(int(self), **kwargs)

    def __repr__(self):
        fields = ", ".join(
            f"{name}={getattr(self, name)!r}"
            for name in self._fields
        )
        return f"{type(self).__name__}({fields})"


class PkmnSpecies(IntEnum):
    BULBASAUR = 0x001
    IVYSAUR = 0x002
    VENUSAUR = 0x003
    CHARMANDER = 0x004
    CHARMELEON = 0x005
    CHARIZARD = 0x006
    SQUIRTLE = 0x007
    WARTORTLE = 0x008
    BLASTOISE = 0x009
    CATERPIE = 0x00A
    METAPOD = 0x00B
    BUTTERFREE = 0x00C
    WEEDLE = 0x00D
    KAKUNA = 0x00E
    BEEDRILL = 0x00F
    PIDGEY = 0x010
    PIDGEOTTO = 0x011
    PIDGEOT = 0x012
    RATTATA = 0x013
    RATICATE = 0x014
    SPEAROW = 0x015
    FEAROW = 0x016
    EKANS = 0x017
    ARBOK = 0x018
    PIKACHU = 0x019
    RAICHU = 0x01A
    SANDSHREW = 0x01B
    SANDSLASH = 0x01C
    NIDORAN_M = 0x01D
    NIDORINA = 0x01E
    NIDOQUEEN = 0x01F
    NIDORAN_F = 0x020
    NIDORINO = 0x021
    NIDOKING = 0x022
    CLEFAIRY = 0x023
    CLEFABLE = 0x024
    VULPIX = 0x025
    NINETALES = 0x026
    JIGGLYPUFF = 0x027
    WIGGLYTUFF = 0x028
    ZUBAT = 0x029
    GOLBAT = 0x02A
    ODDISH = 0x02B
    GLOOM = 0x02C
    VILEPLUME = 0x02D
    PARAS = 0x02E
    PARASECT = 0x02F
    VENONAT = 0x030
    VENOMOTH = 0x031
    DIGLETT = 0x032
    DUGTRIO = 0x033
    MEOWTH = 0x034
    PERSIAN = 0x035
    PSYDUCK = 0x036
    GOLDUCK = 0x037
    MANKEY = 0x038
    PRIMEAPE = 0x039
    GROWLITHE = 0x03A
    ARCANINE = 0x03B
    POLIWAG = 0x03C
    POLIWHIRL = 0x03D
    POLIWRATH = 0x03E
    ABRA = 0x03F
    KADABRA = 0x040
    ALAKAZAM = 0x041
    MACHOP = 0x042
    MACHOKE = 0x043
    MACHAMP = 0x044
    BELLSPROUT = 0x045
    WEEPINBELL = 0x046
    VICTREEBEL = 0x047
    TENTACOOL = 0x048
    TENTACRUEL = 0x049
    GEODUDE = 0x04A
    GRAVELER = 0x04B
    GOLEM = 0x04C
    PONYTA = 0x04D
    RAPIDASH = 0x04E
    SLOWPOKE = 0x04F
    SLOWBRO = 0x050
    MAGNEMITE = 0x051
    MAGNETON = 0x052
    FARFETCHD = 0x053
    DODUO = 0x054
    DODRIO = 0x055
    SEEL = 0x056
    DEWGONG = 0x057
    GRIMER = 0x058
    MUK = 0x059
    SHELLDER = 0x05A
    CLOYSTER = 0x05B
    GASTLY = 0x05C
    HAUNTER = 0x05D
    GENGAR = 0x05E
    ONIX = 0x05F
    DROWZEE = 0x060
    HYPNO = 0x061
    KRABBY = 0x062
    KINGLER = 0x063
    VOLTORB = 0x064
    ELECTRODE = 0x065
    EXEGGCUTE = 0x066
    EXEGGUTOR = 0x067
    CUBONE = 0x068
    MAROWAK = 0x069
    HITMONLEE = 0x06A
    HITMONCHAN = 0x06B
    LICKITUNG = 0x06C
    KOFFING = 0x06D
    WEEZING = 0x06E
    RHYHORN = 0x06F
    RHYDON = 0x070
    CHANSEY = 0x071
    TANGELA = 0x072
    KANGASKHAN = 0x073
    HORSEA = 0x074
    SEADRA = 0x075
    GOLDEEN = 0x076
    SEAKING = 0x077
    STARYU = 0x078
    STARMIE = 0x079
    MRMIME = 0x07A
    SCYTHER = 0x07B
    JYNX = 0x07C
    ELECTABUZZ = 0x07D
    MAGMAR = 0x07E
    PINSIR = 0x07F
    TAUROS = 0x080
    MAGIKARP = 0x081
    GYARADOS = 0x082
    LAPRAS = 0x083
    DITTO = 0x084
    EEVEE = 0x085
    VAPOREON = 0x086
    JOLTEON = 0x087
    FLAREON = 0x088
    PORYGON = 0x089
    OMANYTE = 0x08A
    OMASTAR = 0x08B
    KABUTO = 0x08C
    KABUTOPS = 0x08D
    AERODACTYL = 0x08E
    SNORLAX = 0x08F
    ARTICUNO = 0x090
    ZAPDOS = 0x091
    MOLTRES = 0x092
    DRATINI = 0x093
    DRAGONAIR = 0x094
    DRAGONITE = 0x095
    MEWTWO = 0x096
    MEW = 0x097
    CHIKORITA = 0x098
    BAYLEEF = 0x099
    MEGANIUM = 0x09A
    CYNDAQUIL = 0x09B
    QUILAVA = 0x09C
    TYPHLOSION = 0x09D
    TOTODILE = 0x09E
    CROCONAW = 0x09F
    FERALIGATR = 0x0A0
    SENTRET = 0x0A1
    FURRET = 0x0A2
    HOOTHOOT = 0x0A3
    NOCTOWL = 0x0A4
    LEDYBA = 0x0A5
    LEDIAN = 0x0A6
    SPINARAK = 0x0A7
    ARIADOS = 0x0A8
    CROBAT = 0x0A9
    CHINCHOU = 0x0AA
    LANTURN = 0x0AB
    PICHU = 0x0AC
    CLEFFA = 0x0AD
    IGGLYBUFF = 0x0AE
    TOGEPI = 0x0AF
    TOGETIC = 0x0B0
    NATU = 0x0B1
    XATU = 0x0B2
    MAREEP = 0x0B3
    FLAAFFY = 0x0B4
    AMPHAROS = 0x0B5
    BELLOSSOM = 0x0B6
    MARILL = 0x0B7
    AZUMARILL = 0x0B8
    SUDOWOODO = 0x0B9
    POLITOED = 0x0BA
    HOPPIP = 0x0BB
    SKIPLOOM = 0x0BC
    JUMPLUFF = 0x0BD
    AIPOM = 0x0BE
    SUNKERN = 0x0BF
    SUNFLORA = 0x0C0
    YANMA = 0x0C1
    WOOPER = 0x0C2
    QUAGSIRE = 0x0C3
    ESPEON = 0x0C4
    UMBREON = 0x0C5
    MURKROW = 0x0C6
    SLOWKING = 0x0C7
    MISDREAVUS = 0x0C8
    UNOWN = 0x0C9
    WOBBUFFET = 0x0CA
    GIRAFARIG = 0x0CB
    PINECO = 0x0CC
    FORRETRESS = 0x0CD
    DUNSPARCE = 0x0CE
    GLIGAR = 0x0CF
    STEELIX = 0x0D0
    SNUBBULL = 0x0D1
    GRANBULL = 0x0D2
    QWILFISH = 0x0D3
    SCIZOR = 0x0D4
    SHUCKLE = 0x0D5
    HERACROSS = 0x0D6
    SNEASEL = 0x0D7
    TEDDIURSA = 0x0D8
    URSARING = 0x0D9
    SLUGMA = 0x0DA
    MAGCARGO = 0x0DB
    SWINUB = 0x0DC
    PILOSWINE = 0x0DD
    CORSOLA = 0x0DE
    REMORAID = 0x0DF
    OCTILLERY = 0x0E0
    DELIBIRD = 0x0E1
    MANTINE = 0x0E2
    SKARMORY = 0x0E3
    HOUNDOUR = 0x0E4
    HOUNDOOM = 0x0E5
    KINGDRA = 0x0E6
    PHANPY = 0x0E7
    DONPHAN = 0x0E8
    PORYGON2 = 0x0E9
    STANTLER = 0x0EA
    SMEARGLE = 0x0EB
    TYROGUE = 0x0EC
    HITMONTOP = 0x0ED
    SMOOCHUM = 0x0EE
    ELEKID = 0x0EF
    MAGBY = 0x0F0
    MILTANK = 0x0F1
    BLISSEY = 0x0F2
    RAIKOU = 0x0F3
    ENTEI = 0x0F4
    SUICUNE = 0x0F5
    LARVITAR = 0x0F6
    PUPITAR = 0x0F7
    TYRANITAR = 0x0F8
    LUGIA = 0x0F9
    HOOH = 0x0FA
    CELEBI = 0x0FB
    TREECKO = 0x115
    GROVYLE = 0x116
    SCEPTILE = 0x117
    TORCHIC = 0x118
    COMBUSKEN = 0x119
    BLAZIKEN = 0x11A
    MUDKIP = 0x11B
    MARSHTOMP = 0x11C
    SWAMPERT = 0x11D
    POOCHYENA = 0x11E
    MIGHTYENA = 0x11F
    ZIGZAGOON = 0x120
    LINOONE = 0x121
    WURMPLE = 0x122
    SILCOON = 0x123
    BEAUTIFLY = 0x124
    CASCOON = 0x125
    DUSTOX = 0x126
    LOTAD = 0x127
    LOMBRE = 0x128
    LUDICOLO = 0x129
    SEEDOT = 0x12A
    NUZLEAF = 0x12B
    SHIFTRY = 0x12C
    NINCADA = 0x12D
    NINJASK = 0x12E
    SHEDINJA = 0x12F
    TAILLOW = 0x130
    SWELLOW = 0x131
    SHROOMISH = 0x132
    BRELOOM = 0x133
    SPINDA = 0x134
    WINGULL = 0x135
    PELIPPER = 0x136
    SURSKIT = 0x137
    MASQUERAIN = 0x138
    WAILMER = 0x139
    WAILORD = 0x13A
    SKITTY = 0x13B
    DELCATTY = 0x13C
    KECLEON = 0x13D
    BALTOY = 0x13E
    CLAYDOL = 0x13F
    NOSEPASS = 0x140
    TORKOAL = 0x141
    SABLEYE = 0x142
    BARBOACH = 0x143
    WHISCASH = 0x144
    LUVDISC = 0x145
    CORPHISH = 0x146
    CRAWDAUNT = 0x147
    FEEBAS = 0x148
    MILOTIC = 0x149
    CARVANHA = 0x14A
    SHARPEDO = 0x14B
    TRAPINCH = 0x14C
    VIBRAVA = 0x14D
    FLYGON = 0x14E
    MAKUHITA = 0x14F
    HARIYAMA = 0x150
    ELECTRIKE = 0x151
    MANECTRIC = 0x152
    NUMEL = 0x153
    CAMERUPT = 0x154
    SPHEAL = 0x155
    SEALEO = 0x156
    WALREIN = 0x157
    CACNEA = 0x158
    CACTURNE = 0x159
    SNORUNT = 0x15A
    GLALIE = 0x15B
    LUNATONE = 0x15C
    SOLROCK = 0x15D
    AZURILL = 0x15E
    SPOINK = 0x15F
    GRUMPIG = 0x160
    PLUSLE = 0x161
    MINUN = 0x162
    MAWILE = 0x163
    MEDITITE = 0x164
    MEDICHAM = 0x165
    SWABLU = 0x166
    ALTARIA = 0x167
    WYNAUT = 0x168
    DUSKULL = 0x169
    DUSCLOPS = 0x16A
    ROSELIA = 0x16B
    SLAKOTH = 0x16C
    VIGOROTH = 0x16D
    SLAKING = 0x16E
    GULPIN = 0x16F
    SWALOT = 0x170
    TROPIUS = 0x171
    WHISMUR = 0x172
    LOUDRED = 0x173
    EXPLOUD = 0x174
    CLAMPERL = 0x175
    HUNTAIL = 0x176
    GOREBYSS = 0x177
    ABSOL = 0x178
    SHUPPET = 0x179
    BANETTE = 0x17A
    SEVIPER = 0x17B
    ZANGOOSE = 0x17C
    RELICANTH = 0x17D
    ARON = 0x17E
    LAIRON = 0x17F
    AGGRON = 0x180
    CASTFORM = 0x181
    VOLBEAT = 0x182
    ILLUMISE = 0x183
    LILEEP = 0x184
    CRADILY = 0x185
    ANORITH = 0x186
    ARMALDO = 0x187
    RALTS = 0x188
    KIRLIA = 0x189
    GARDEVOIR = 0x18A
    BAGON = 0x18B
    SHELGON = 0x18C
    SALAMENCE = 0x18D
    BELDUM = 0x18E
    METANG = 0x18F
    METAGROSS = 0x190
    REGIROCK = 0x191
    REGICE = 0x192
    REGISTEEL = 0x193
    KYOGRE = 0x194
    GROUDON = 0x195
    RAYQUAZA = 0x196
    LATIAS = 0x197
    LATIOS = 0x198
    JIRACHI = 0x199
    DEOXYS = 0x19A
    CHIMECHO = 0x19B
    EGG = 0x19C


class PkmnItem(IntEnum):
    NOTHING = 0x0000
    MASTER_BALL = 0x0001
    ULTRA_BALL = 0x0002
    GREAT_BALL = 0x0003
    POKE_BALL = 0x0004
    SAFARI_BALL = 0x0005
    NET_BALL = 0x0006
    DIVE_BALL = 0x0007
    NEST_BALL = 0x0008
    REPEAT_BALL = 0x0009
    TIMER_BALL = 0x000A
    LUXURY_BALL = 0x000B
    PREMIER_BALL = 0x000C
    POTION = 0x000D
    ANTIDOTE = 0x000E
    BURN_HEAL = 0x000F
    ICE_HEAL = 0x0010
    AWAKENING = 0x0011
    PARLYZ_HEAL = 0x0012
    FULL_RESTORE = 0x0013
    MAX_POTION = 0x0014
    HYPER_POTION = 0x0015
    SUPER_POTION = 0x0016
    FULL_HEAL = 0x0017
    REVIVE = 0x0018
    MAX_REVIVE = 0x0019
    FRESH_WATER = 0x001A
    SODA_POP = 0x001B
    LEMONADE = 0x001C
    MOOMOO_MILK = 0x001D
    ENERGYPOWDER = 0x001E
    ENERGY_ROOT = 0x001F
    HEAL_POWDER = 0x0020
    REVIVAL_HERB = 0x0021
    ETHER = 0x0022
    MAX_ETHER = 0x0023
    ELIXIR = 0x0024
    MAX_ELIXIR = 0x0025
    LAVA_COOKIE = 0x0026
    BLUE_FLUTE = 0x0027
    YELLOW_FLUTE = 0x0028
    RED_FLUTE = 0x0029
    BLACK_FLUTE = 0x002A
    WHITE_FLUTE = 0x002B
    BERRY_JUICE = 0x002C
    SACRED_ASH = 0x002D
    SHOAL_SALT = 0x002E
    SHOAL_SHELL = 0x002F
    RED_SHARD = 0x0030
    BLUE_SHARD = 0x0031
    YELLOW_SHARD = 0x0032
    GREEN_SHARD = 0x0033
    HP_UP = 0x003F
    PROTEIN = 0x0040
    IRON = 0x0041
    CARBOS = 0x0042
    CALCIUM = 0x0043
    RARE_CANDY = 0x0044
    PP_UP = 0x0045
    ZINC = 0x0046
    PP_MAX = 0x0047
    GUARD_SPEC = 0x0049
    DIRE_HIT = 0x004A
    X_ATTACK = 0x004B
    X_DEFEND = 0x004C
    X_SPEED = 0x004D
    X_ACCURACY = 0x004E
    X_SPECIAL = 0x004F
    POKE_DOLL = 0x0050
    FLUFFY_TAIL = 0x0051
    SUPER_REPEL = 0x0053
    MAX_REPEL = 0x0054
    ESCAPE_ROPE = 0x0055
    REPEL = 0x0056
    SUN_STONE = 0x005D
    MOON_STONE = 0x005E
    FIRE_STONE = 0x005F
    THUNDERSTONE = 0x0060
    WATER_STONE = 0x0061
    LEAF_STONE = 0x0062
    TINYMUSHROOM = 0x0067
    BIG_MUSHROOM = 0x0068
    PEARL = 0x006A
    BIG_PEARL = 0x006B
    STARDUST = 0x006C
    STAR_PIECE = 0x006D
    NUGGET = 0x006E
    HEART_SCALE = 0x006F
    ORANGE_MAIL = 0x0079
    HARBOR_MAIL = 0x007A
    GLITTER_MAIL = 0x007B
    MECH_MAIL = 0x007C
    WOOD_MAIL = 0x007D
    WAVE_MAIL = 0x007E
    BEAD_MAIL = 0x007F
    SHADOW_MAIL = 0x0080
    TROPIC_MAIL = 0x0081
    DREAM_MAIL = 0x0082
    FAB_MAIL = 0x0083
    RETRO_MAIL = 0x0084
    CHERI_BERRY = 0x0085
    CHESTO_BERRY = 0x0086
    PECHA_BERRY = 0x0087
    RAWST_BERRY = 0x0088
    ASPEAR_BERRY = 0x0089
    LEPPA_BERRY = 0x008A
    ORAN_BERRY = 0x008B
    PERSIM_BERRY = 0x008C
    LUM_BERRY = 0x008D
    SITRUS_BERRY = 0x008E
    FIGY_BERRY = 0x008F
    WIKI_BERRY = 0x0090
    MAGO_BERRY = 0x0091
    AGUAV_BERRY = 0x0092
    IAPAPA_BERRY = 0x0093
    RAZZ_BERRY = 0x0094
    BLUK_BERRY = 0x0095
    NANAB_BERRY = 0x0096
    WEPEAR_BERRY = 0x0097
    PINAP_BERRY = 0x0098
    POMEG_BERRY = 0x0099
    KELPSY_BERRY = 0x009A
    QUALOT_BERRY = 0x009B
    HONDEW_BERRY = 0x009C
    GREPA_BERRY = 0x009D
    TAMATO_BERRY = 0x009E
    CORNN_BERRY = 0x009F
    MAGOST_BERRY = 0x00A0
    RABUTA_BERRY = 0x00A1
    NOMEL_BERRY = 0x00A2
    SPELON_BERRY = 0x00A3
    PAMTRE_BERRY = 0x00A4
    WATMEL_BERRY = 0x00A5
    DURIN_BERRY = 0x00A6
    BELUE_BERRY = 0x00A7
    LIECHI_BERRY = 0x00A8
    GANLON_BERRY = 0x00A9
    SALAC_BERRY = 0x00AA
    PETAYA_BERRY = 0x00AB
    APICOT_BERRY = 0x00AC
    LANSAT_BERRY = 0x00AD
    STARF_BERRY = 0x00AE
    ENIGMA_BERRY = 0x00AF
    BRIGHTPOWDER = 0x00B3
    WHITE_HERB = 0x00B4
    MACHO_BRACE = 0x00B5
    EXP_SHARE = 0x00B6
    QUICK_CLAW = 0x00B7
    SOOTHE_BELL = 0x00B8
    MENTAL_HERB = 0x00B9
    CHOICE_BAND = 0x00BA
    KINGS_ROCK = 0x00BB
    SILVERPOWDER = 0x00BC
    AMULET_COIN = 0x00BD
    CLEANSE_TAG = 0x00BE
    SOUL_DEW = 0x00BF
    DEEPSEATOOTH = 0x00C0
    DEEPSEASCALE = 0x00C1
    SMOKE_BALL = 0x00C2
    EVERSTONE = 0x00C3
    FOCUS_BAND = 0x00C4
    LUCKY_EGG = 0x00C5
    SCOPE_LENS = 0x00C6
    METAL_COAT = 0x00C7
    LEFTOVERS = 0x00C8
    DRAGON_SCALE = 0x00C9
    LIGHT_BALL = 0x00CA
    SOFT_SAND = 0x00CB
    HARD_STONE = 0x00CC
    MIRACLE_SEED = 0x00CD
    BLACKGLASSES = 0x00CE
    BLACK_BELT = 0x00CF
    MAGNET = 0x00D0
    MYSTIC_WATER = 0x00D1
    SHARP_BEAK = 0x00D2
    POISON_BARB = 0x00D3
    NEVERMELTICE = 0x00D4
    SPELL_TAG = 0x00D5
    TWISTEDSPOON = 0x00D6
    CHARCOAL = 0x00D7
    DRAGON_FANG = 0x00D8
    SILK_SCARF = 0x00D9
    UP_GRADE = 0x00DA
    SHELL_BELL = 0x00DB
    SEA_INCENSE = 0x00DC
    LAX_INCENSE = 0x00DD
    LUCKY_PUNCH = 0x00DE
    METAL_POWDER = 0x00DF
    THICK_CLUB = 0x00E0
    STICK = 0x00E1
    RED_SCARF = 0x00FE
    BLUE_SCARF = 0x00FF
    PINK_SCARF = 0x0100
    GREEN_SCARF = 0x0101
    YELLOW_SCARF = 0x0102
    MACH_BIKE = 0x0103
    COIN_CASE = 0x0104
    ITEMFINDER = 0x0105
    OLD_ROD = 0x0106
    GOOD_ROD = 0x0107
    SUPER_ROD = 0x0108
    SS_TICKET = 0x0109
    CONTEST_PASS = 0x010A
    WAILMER_PAIL = 0x010C
    DEVON_GOODS = 0x010D
    SOOT_SACK = 0x010E
    BASEMENT_KEY = 0x010F
    ACRO_BIKE = 0x0110
    POKEBLOCK_CASE = 0x0111
    LETTER = 0x0112
    EON_TICKET = 0x0113
    RED_ORB = 0x0114
    BLUE_ORB = 0x0115
    SCANNER = 0x0116
    GO_GOGGLES = 0x0117
    METEORITE = 0x0118
    RM_1_KEY = 0x0119
    RM_2_KEY = 0x011A
    RM_4_KEY = 0x011B
    RM_6_KEY = 0x011C
    STORAGE_KEY = 0x011D
    ROOT_FOSSIL = 0x011E
    CLAW_FOSSIL = 0x011F
    DEVON_SCOPE = 0x0120
    TM01 = 0x0121
    TM02 = 0x0122
    TM03 = 0x0123
    TM04 = 0x0124
    TM05 = 0x0125
    TM06 = 0x0126
    TM07 = 0x0127
    TM08 = 0x0128
    TM09 = 0x0129
    TM10 = 0x012A
    TM11 = 0x012B
    TM12 = 0x012C
    TM13 = 0x012D
    TM14 = 0x012E
    TM15 = 0x012F
    TM16 = 0x0130
    TM17 = 0x0131
    TM18 = 0x0132
    TM19 = 0x0133
    TM20 = 0x0134
    TM21 = 0x0135
    TM22 = 0x0136
    TM23 = 0x0137
    TM24 = 0x0138
    TM25 = 0x0139
    TM26 = 0x013A
    TM27 = 0x013B
    TM28 = 0x013C
    TM29 = 0x013D
    TM30 = 0x013E
    TM31 = 0x013F
    TM32 = 0x0140
    TM33 = 0x0141
    TM34 = 0x0142
    TM35 = 0x0143
    TM36 = 0x0144
    TM37 = 0x0145
    TM38 = 0x0146
    TM39 = 0x0147
    TM40 = 0x0148
    TM41 = 0x0149
    TM42 = 0x014A
    TM43 = 0x014B
    TM44 = 0x014C
    TM45 = 0x014D
    TM46 = 0x014E
    TM47 = 0x014F
    TM48 = 0x0150
    TM49 = 0x0151
    TM50 = 0x0152
    HM01 = 0x0153
    HM02 = 0x0154
    HM03 = 0x0155
    HM04 = 0x0156
    HM05 = 0x0157
    HM06 = 0x0158
    HM07 = 0x0159
    HM08 = 0x015A
    OAKS_PARCEL = 0x015D
    POKE_FLUTE = 0x015E
    SECRET_KEY = 0x015F
    BIKE_VOUCHER = 0x0160
    GOLD_TEETH = 0x0161
    OLD_AMBER = 0x0162
    CARD_KEY = 0x0163
    LIFT_KEY = 0x0164
    HELIX_FOSSIL = 0x0165
    DOME_FOSSIL = 0x0166
    SILPH_SCOPE = 0x0167
    BICYCLE = 0x0168
    TOWN_MAP = 0x0169
    VS_SEEKER = 0x016A
    FAME_CHECKER = 0x016B
    TM_CASE = 0x016C
    BERRY_POUCH = 0x016D
    TEACHY_TV = 0x016E
    TRI_PASS = 0x016F
    RAINBOW_PASS = 0x0170
    TEA = 0x0171
    MYSTICTICKET = 0x0172
    AURORATICKET = 0x0173
    POWDER_JAR = 0x0174
    RUBY = 0x0175
    SAPPHIRE = 0x0176
    MAGMA_EMBLEM = 0x0177
    OLD_SEA_MAP = 0x0178


class PkmnMove(IntEnum):
    NO_MOVE = 0
    POUND = 1
    KARATE_CHOP = 2
    DOUBLE_SLAP = 3
    COMET_PUNCH = 4
    MEGA_PUNCH = 5
    PAY_DAY = 6
    FIRE_PUNCH = 7
    ICE_PUNCH = 8
    THUNDER_PUNCH = 9
    SCRATCH = 10
    VISE_GRIP = 11
    GUILLOTINE = 12
    RAZOR_WIND = 13
    SWORDS_DANCE = 14
    CUT = 15
    GUST = 16
    WING_ATTACK = 17
    WHIRLWIND = 18
    FLY = 19
    BIND = 20
    SLAM = 21
    VINE_WHIP = 22
    STOMP = 23
    DOUBLE_KICK = 24
    MEGA_KICK = 25
    JUMP_KICK = 26
    ROLLING_KICK = 27
    SAND_ATTACK = 28
    HEADBUTT = 29
    HORN_ATTACK = 30
    FURY_ATTACK = 31
    HORN_DRILL = 32
    TACKLE = 33
    BODY_SLAM = 34
    WRAP = 35
    TAKE_DOWN = 36
    THRASH = 37
    DOUBLE_EDGE = 38
    TAIL_WHIP = 39
    POISON_STING = 40
    TWINEEDLE = 41
    PIN_MISSILE = 42
    LEER = 43
    BITE = 44
    GROWL = 45
    ROAR = 46
    SING = 47
    SUPERSONIC = 48
    SONIC_BOOM = 49
    DISABLE = 50
    ACID = 51
    EMBER = 52
    FLAMETHROWER = 53
    MIST = 54
    WATER_GUN = 55
    HYDRO_PUMP = 56
    SURF = 57
    ICE_BEAM = 58
    BLIZZARD = 59
    PSYBEAM = 60
    BUBBLE_BEAM = 61
    AURORA_BEAM = 62
    HYPER_BEAM = 63
    PECK = 64
    DRILL_PECK = 65
    SUBMISSION = 66
    LOW_KICK = 67
    COUNTER = 68
    SEISMIC_TOSS = 69
    STRENGTH = 70
    ABSORB = 71
    MEGA_DRAIN = 72
    LEECH_SEED = 73
    GROWTH = 74
    RAZOR_LEAF = 75
    SOLAR_BEAM = 76
    POISON_POWDER = 77
    STUN_SPORE = 78
    SLEEP_POWDER = 79
    PETAL_DANCE = 80
    STRING_SHOT = 81
    DRAGON_RAGE = 82
    FIRE_SPIN = 83
    THUNDER_SHOCK = 84
    THUNDERBOLT = 85
    THUNDER_WAVE = 86
    THUNDER = 87
    ROCK_THROW = 88
    EARTHQUAKE = 89
    FISSURE = 90
    DIG = 91
    TOXIC = 92
    CONFUSION = 93
    PSYCHIC = 94
    HYPNOSIS = 95
    MEDITATE = 96
    AGILITY = 97
    QUICK_ATTACK = 98
    RAGE = 99
    TELEPORT = 100
    NIGHT_SHADE = 101
    MIMIC = 102
    SCREECH = 103
    DOUBLE_TEAM = 104
    RECOVER = 105
    HARDEN = 106
    MINIMIZE = 107
    SMOKESCREEN = 108
    CONFUSE_RAY = 109
    WITHDRAW = 110
    DEFENSE_CURL = 111
    BARRIER = 112
    LIGHT_SCREEN = 113
    HAZE = 114
    REFLECT = 115
    FOCUS_ENERGY = 116
    BIDE = 117
    METRONOME = 118
    MIRROR_MOVE = 119
    SELF_DESTRUCT = 120
    EGG_BOMB = 121
    LICK = 122
    SMOG = 123
    SLUDGE = 124
    BONE_CLUB = 125
    FIRE_BLAST = 126
    WATERFALL = 127
    CLAMP = 128
    SWIFT = 129
    SKULL_BASH = 130
    SPIKE_CANNON = 131
    CONSTRICT = 132
    AMNESIA = 133
    KINESIS = 134
    SOFT_BOILED = 135
    HIGH_JUMP_KICK = 136
    GLARE = 137
    DREAM_EATER = 138
    POISON_GAS = 139
    BARRAGE = 140
    LEECH_LIFE = 141
    LOVELY_KISS = 142
    SKY_ATTACK = 143
    TRANSFORM = 144
    BUBBLE = 145
    DIZZY_PUNCH = 146
    SPORE = 147
    FLASH = 148
    PSYWAVE = 149
    SPLASH = 150
    ACID_ARMOR = 151
    CRABHAMMER = 152
    EXPLOSION = 153
    FURY_SWIPES = 154
    BONEMERANG = 155
    REST = 156
    ROCK_SLIDE = 157
    HYPER_FANG = 158
    SHARPEN = 159
    CONVERSION = 160
    TRI_ATTACK = 161
    SUPER_FANG = 162
    SLASH = 163
    SUBSTITUTE = 164
    STRUGGLE = 165
    SKETCH = 166
    TRIPLE_KICK = 167
    THIEF = 168
    SPIDER_WEB = 169
    MIND_READER = 170
    NIGHTMARE = 171
    FLAME_WHEEL = 172
    SNORE = 173
    CURSE = 174
    FLAIL = 175
    CONVERSION_2 = 176
    AEROBLAST = 177
    COTTON_SPORE = 178
    REVERSAL = 179
    SPITE = 180
    POWDER_SNOW = 181
    PROTECT = 182
    MACH_PUNCH = 183
    SCARY_FACE = 184
    FEINT_ATTACK = 185
    SWEET_KISS = 186
    BELLY_DRUM = 187
    SLUDGE_BOMB = 188
    MUD_SLAP = 189
    OCTAZOOKA = 190
    SPIKES = 191
    ZAP_CANNON = 192
    FORESIGHT = 193
    DESTINY_BOND = 194
    PERISH_SONG = 195
    ICY_WIND = 196
    DETECT = 197
    BONE_RUSH = 198
    LOCK_ON = 199
    OUTRAGE = 200
    SANDSTORM = 201
    GIGA_DRAIN = 202
    ENDURE = 203
    CHARM = 204
    ROLLOUT = 205
    FALSE_SWIPE = 206
    SWAGGER = 207
    MILK_DRINK = 208
    SPARK = 209
    FURY_CUTTER = 210
    STEEL_WING = 211
    MEAN_LOOK = 212
    ATTRACT = 213
    SLEEP_TALK = 214
    HEAL_BELL = 215
    RETURN = 216
    PRESENT = 217
    FRUSTRATION = 218
    SAFEGUARD = 219
    PAIN_SPLIT = 220
    SACRED_FIRE = 221
    MAGNITUDE = 222
    DYNAMIC_PUNCH = 223
    MEGAHORN = 224
    DRAGON_BREATH = 225
    BATON_PASS = 226
    ENCORE = 227
    PURSUIT = 228
    RAPID_SPIN = 229
    SWEET_SCENT = 230
    IRON_TAIL = 231
    METAL_CLAW = 232
    VITAL_THROW = 233
    MORNING_SUN = 234
    SYNTHESIS = 235
    MOONLIGHT = 236
    HIDDEN_POWER = 237
    CROSS_CHOP = 238
    TWISTER = 239
    RAIN_DANCE = 240
    SUNNY_DAY = 241
    CRUNCH = 242
    MIRROR_COAT = 243
    PSYCH_UP = 244
    EXTREME_SPEED = 245
    ANCIENT_POWER = 246
    SHADOW_BALL = 247
    FUTURE_SIGHT = 248
    ROCK_SMASH = 249
    WHIRLPOOL = 250
    BEAT_UP = 251
    FAKE_OUT = 252
    UPROAR = 253
    STOCKPILE = 254
    SPIT_UP = 255
    SWALLOW = 256
    HEAT_WAVE = 257
    HAIL = 258
    TORMENT = 259
    FLATTER = 260
    WILL_O_WISP = 261
    MEMENTO = 262
    FACADE = 263
    FOCUS_PUNCH = 264
    SMELLING_SALTS = 265
    FOLLOW_ME = 266
    NATURE_POWER = 267
    CHARGE = 268
    TAUNT = 269
    HELPING_HAND = 270
    TRICK = 271
    ROLE_PLAY = 272
    WISH = 273
    ASSIST = 274
    INGRAIN = 275
    SUPERPOWER = 276
    MAGIC_COAT = 277
    RECYCLE = 278
    REVENGE = 279
    BRICK_BREAK = 280
    YAWN = 281
    KNOCK_OFF = 282
    ENDEAVOR = 283
    ERUPTION = 284
    SKILL_SWAP = 285
    IMPRISON = 286
    REFRESH = 287
    GRUDGE = 288
    SNATCH = 289
    SECRET_POWER = 290
    DIVE = 291
    ARM_THRUST = 292
    CAMOUFLAGE = 293
    TAIL_GLOW = 294
    LUSTER_PURGE = 295
    MIST_BALL = 296
    FEATHER_DANCE = 297
    TEETER_DANCE = 298
    BLAZE_KICK = 299
    MUD_SPORT = 300
    ICE_BALL = 301
    NEEDLE_ARM = 302
    SLACK_OFF = 303
    HYPER_VOICE = 304
    POISON_FANG = 305
    CRUSH_CLAW = 306
    BLAST_BURN = 307
    HYDRO_CANNON = 308
    METEOR_MASH = 309
    ASTONISH = 310
    WEATHER_BALL = 311
    AROMATHERAPY = 312
    FAKE_TEARS = 313
    AIR_CUTTER = 314
    OVERHEAT = 315
    ODOR_SLEUTH = 316
    ROCK_TOMB = 317
    SILVER_WIND = 318
    METAL_SOUND = 319
    GRASS_WHISTLE = 320
    TICKLE = 321
    COSMIC_POWER = 322
    WATER_SPOUT = 323
    SIGNAL_BEAM = 324
    SHADOW_PUNCH = 325
    EXTRASENSORY = 326
    SKY_UPPERCUT = 327
    SAND_TOMB = 328
    SHEER_COLD = 329
    MUDDY_WATER = 330
    BULLET_SEED = 331
    AERIAL_ACE = 332
    ICICLE_SPEAR = 333
    IRON_DEFENSE = 334
    BLOCK = 335
    HOWL = 336
    DRAGON_CLAW = 337
    FRENZY_PLANT = 338
    BULK_UP = 339
    BOUNCE = 340
    MUD_SHOT = 341
    POISON_TAIL = 342
    COVET = 343
    VOLT_TACKLE = 344
    MAGICAL_LEAF = 345
    WATER_SPORT = 346
    CALM_MIND = 347
    LEAF_BLADE = 348
    DRAGON_DANCE = 349
    ROCK_BLAST = 350
    SHOCK_WAVE = 351
    WATER_PULSE = 352
    DOOM_DESIRE = 353
    PSYCHO_BOOST = 354


class PkmnLocation(IntEnum):
    LITTLEROOT_TOWN = 0x00
    OLDALE_TOWN = 0x01
    DEWFORD_TOWN = 0x02
    LAVARIDGE_TOWN = 0x03
    FALLARBOR_TOWN = 0x04
    VERDANTURF_TOWN = 0x05
    PACIFIDLOG_TOWN = 0x06
    PETALBURG_CITY = 0x07
    SLATEPORT_CITY = 0x08
    MAUVILLE_CITY = 0x09
    RUSTBORO_CITY = 0x0A
    FORTREE_CITY = 0x0B
    LILYCOVE_CITY = 0x0C
    MOSSDEEP_CITY = 0x0D
    SOOTOPOLIS_CITY = 0x0E
    EVER_GRANDE_CITY = 0x0F
    ROUTE_101 = 0x10
    ROUTE_102 = 0x11
    ROUTE_103 = 0x12
    ROUTE_104 = 0x13
    ROUTE_105 = 0x14
    ROUTE_106 = 0x15
    ROUTE_107 = 0x16
    ROUTE_108 = 0x17
    ROUTE_109 = 0x18
    ROUTE_110 = 0x19
    ROUTE_111 = 0x1A
    ROUTE_112 = 0x1B
    ROUTE_113 = 0x1C
    ROUTE_114 = 0x1D
    ROUTE_115 = 0x1E
    ROUTE_116 = 0x1F
    ROUTE_117 = 0x20
    ROUTE_118 = 0x21
    ROUTE_119 = 0x22
    ROUTE_120 = 0x23
    ROUTE_121 = 0x24
    ROUTE_122 = 0x25
    ROUTE_123 = 0x26
    ROUTE_124 = 0x27
    ROUTE_125 = 0x28
    ROUTE_126 = 0x29
    ROUTE_127 = 0x2A
    ROUTE_128 = 0x2B
    ROUTE_129 = 0x2C
    ROUTE_130 = 0x2D
    ROUTE_131 = 0x2E
    ROUTE_132 = 0x2F
    ROUTE_133 = 0x30
    ROUTE_134 = 0x31
    UNDERWATER_ROUTE_124 = 0x32
    UNDERWATER_ROUTE_126 = 0x33
    UNDERWATER_ROUTE_127 = 0x34
    UNDERWATER_ROUTE_128 = 0x35
    UNDERWATER_SOOTOPOLIS_CITY = 0x36
    GRANITE_CAVE = 0x37
    MT_CHIMNEY = 0x38
    SAFARI_ZONE_GEN3 = 0x39
    BATTLE_FRONTIER = 0x3A
    PETALBURG_WOODS = 0x3B
    RUSTURF_TUNNEL = 0x3C
    ABANDONED_SHIP = 0x3D
    NEW_MAUVILLE = 0x3E
    METEOR_FALLS = 0x3F
    METEOR_FALLS_UNUSED = 0x40
    MT_PYRE = 0x41
    MAGMA_AQUA_HIDEOUT = 0x42
    SHOAL_CAVE = 0x43
    SEAFLOOR_CAVERN = 0x44
    UNDERWATER_SEAFLOOR_CAVERN = 0x45
    VICTORY_ROAD_GEN3 = 0x46
    MIRAGE_ISLAND = 0x47
    CAVE_OF_ORIGIN = 0x48
    SOUTHERN_ISLAND = 0x49
    FIERY_PATH = 0x4A
    FIERY_PATH_UNUSED = 0x4B
    JAGGED_PASS = 0x4C
    JAGGED_PASS_UNUSED = 0x4D
    SEALED_CHAMBER = 0x4E
    UNDERWATER_ROUTE_134 = 0x4F
    SCORCHED_SLAB = 0x50
    ISLAND_CAVE = 0x51
    DESERT_RUINS = 0x52
    ANCIENT_TOMB = 0x53
    INSIDE_OF_TRUCK = 0x54
    SKY_PILLAR = 0x55
    SECRET_BASE = 0x56
    FERRY = 0x57
    PALLET_TOWN = 0x58
    VIRIDIAN_CITY = 0x59
    PEWTER_CITY = 0x5A
    CERULEAN_CITY = 0x5B
    LAVENDER_TOWN = 0x5C
    VERMILION_CITY = 0x5D
    CELADON_CITY = 0x5E
    FUCHSIA_CITY = 0x5F
    CINNABAR_ISLAND = 0x60
    INDIGO_PLATEAU = 0x61
    SAFFRON_CITY = 0x62
    ROUTE_4_POKEMON_CENTER = 0x63
    ROUTE_10_POKEMON_CENTER = 0x64
    ROUTE_1 = 0x65
    ROUTE_2 = 0x66
    ROUTE_3 = 0x67
    ROUTE_4 = 0x68
    ROUTE_5 = 0x69
    ROUTE_6 = 0x6A
    ROUTE_7 = 0x6B
    ROUTE_8 = 0x6C
    ROUTE_9 = 0x6D
    ROUTE_10 = 0x6E
    ROUTE_11 = 0x6F
    ROUTE_12 = 0x70
    ROUTE_13 = 0x71
    ROUTE_14 = 0x72
    ROUTE_15 = 0x73
    ROUTE_16 = 0x74
    ROUTE_17 = 0x75
    ROUTE_18 = 0x76
    ROUTE_19 = 0x77
    ROUTE_20 = 0x78
    ROUTE_21 = 0x79
    ROUTE_22 = 0x7A
    ROUTE_23 = 0x7B
    ROUTE_24 = 0x7C
    ROUTE_25 = 0x7D
    VIRIDIAN_FOREST = 0x7E
    MT_MOON = 0x7F
    SS_ANNE = 0x80
    UNDERGROUND_PATH_ROUTES_5_6 = 0x81
    UNDERGROUND_PATH_ROUTES_7_8 = 0x82
    DIGLETT_CAVE = 0x83
    VICTORY_ROAD_GEN1 = 0x84
    ROCKET_HIDEOUT = 0x85
    SILPH_CO = 0x86
    POKEMON_MANSION = 0x87
    SAFARI_ZONE_GEN1 = 0x88
    POKEMON_LEAGUE = 0x89
    ROCK_TUNNEL = 0x8A
    SEAFOAM_ISLANDS = 0x8B
    POKEMON_TOWER = 0x8C
    CERULEAN_CAVE = 0x8D
    POWER_PLANT = 0x8E
    ONE_ISLAND = 0x8F
    TWO_ISLAND = 0x90
    THREE_ISLAND = 0x91
    FOUR_ISLAND = 0x92
    FIVE_ISLAND = 0x93
    SEVEN_ISLAND = 0x94
    SIX_ISLAND = 0x95
    KINDLE_ROAD = 0x96
    TREASURE_BEACH = 0x97
    CAPE_BRINK = 0x98
    BOND_BRIDGE = 0x99
    THREE_ISLE_PORT = 0x9A
    SEVII_ISLE_6 = 0x9B
    SEVII_ISLE_7 = 0x9C
    SEVII_ISLE_8 = 0x9D
    SEVII_ISLE_9 = 0x9E
    RESORT_GORGEOUS = 0x9F
    WATER_LABYRINTH = 0xA0
    FIVE_ISLE_MEADOW = 0xA1
    MEMORIAL_PILLAR = 0xA2
    OUTCAST_ISLAND = 0xA3
    GREEN_PATH = 0xA4
    WATER_PATH = 0xA5
    RUIN_VALLEY = 0xA6
    TRAINER_TOWER_EXTERIOR = 0xA7
    CANYON_ENTRANCE = 0xA8
    SEVAULT_CANYON = 0xA9
    TANOBY_RUINS = 0xAA
    SEVII_ISLE_22 = 0xAB
    SEVII_ISLE_23 = 0xAC
    SEVII_ISLE_24 = 0xAD
    NAVEL_ROCK_GEN1 = 0xAE
    MT_EMBER = 0xAF
    BERRY_FOREST = 0xB0
    ICEFALL_CAVE = 0xB1
    ROCKET_WAREHOUSE = 0xB2
    TRAINER_TOWER = 0xB3
    DOTTED_HOLE = 0xB4
    LOST_CAVE = 0xB5
    PATTERN_BUSH = 0xB6
    ALTERING_CAVE_GEN1 = 0xB7
    TANOBY_CHAMBERS = 0xB8
    THREE_ISLE_PATH = 0xB9
    TANOBY_KEY = 0xBA
    BIRTH_ISLAND_GEN1 = 0xBB
    MONEAN_CHAMBER = 0xBC
    LIPTOO_CHAMBER = 0xBD
    WEEPTH_CHAMBER = 0xBE
    DILFORD_CHAMBER = 0xBF
    SCUFIB_CHAMBER = 0xC0
    RIXY_CHAMBER = 0xC1
    VIAPOIS_CHAMBER = 0xC2
    EMBER_SPA = 0xC3
    SPECIAL_AREAE = 0xC4
    AQUA_HIDEOUT = 0xC5
    MAGMA_HIDEOUT = 0xC6
    MIRAGE_TOWER = 0xC7
    BIRTH_ISLAND_GEN3 = 0xC8
    FARAWAY_ISLAND = 0xC9
    ARTISAN_CAVE = 0xCA
    MARINE_CAVE = 0xCB
    UNDERWATER_MARINE_CAVE = 0xCC
    TERRA_CAVE = 0xCD
    UNDERWATER_ROUTE_105 = 0xCE
    UNDERWATER_ROUTE_125 = 0xCF
    UNDERWATER_ROUTE_129 = 0xD0
    DESERT_UNDERPASS = 0xD1
    ALTERING_CAVE_GEN3 = 0xD2
    NAVEL_ROCK_GEN3 = 0xD3
    TRAINER_HILL = 0xD4
    GIFT_EGG = 0xFD
    IN_GAME_TRADE = 0xFE
    FATEFUL_ENCOUNTER = 0xFF


class PkmnPPBonus(Bitfield):
    width = 8

    move_1 = Bits(2, int)
    move_2 = Bits(2, int)
    move_3 = Bits(2, int)
    move_4 = Bits(2, int)


class PkmnPokerus(Bitfield):
    width = 8

    days_left = Bits(4, int)
    strain = Bits(4, int)


class PkmnGame(IntEnum):
    SAPPHIRE = 1
    RUBY = 2
    EMERALD = 3
    FIRE_RED = 4
    LEAF_GREEN = 5
    COLOSSEUM_XD = 15


class PkmnBall(IntEnum):
    MASTER_BALL = 1
    ULTRA_BALL = 2
    GREAT_BALL = 3
    POKE_BALL = 4
    SAFARI_BALL = 5
    NET_BALL = 6
    DIVE_BALL = 7
    NEST_BALL = 8
    REPEAT_BALL = 9
    TIMER_BALL = 10
    LUXURY_BALL = 11
    PREMIER_BALL = 12


class PkmnTrainerGender(IntEnum):
    MALE = 0
    FEMALE = 1


class PkmnOrigins(Bitfield):
    width = 16

    level_met = Bits(7, int)
    game = Bits(4, PkmnGame)
    ball = Bits(4, PkmnBall)
    trainer_gender = Bits(1, PkmnTrainerGender)


class PkmnIVsEggAbility(Bitfield):
    width = 32

    hp = Bits(5, int)
    attack = Bits(5, int)
    defense = Bits(5, int)
    speed = Bits(5, int)
    sp_attack = Bits(5, int)
    sp_defense = Bits(5, int)
    is_egg = Bits(1, bool)
    ability = Bits(1, int)


class PkmnRibbonsObedience(Bitfield):
    width = 32

    cool = Bits(3, int)
    beauty = Bits(3, int)
    cute = Bits(3, int)
    smart = Bits(3, int)
    tough = Bits(3, int)

    champion = Bits(1, bool)
    winning = Bits(1, bool)
    victory = Bits(1, bool)
    artist = Bits(1, bool)
    effort = Bits(1, bool)

    battle_champion = Bits(1, bool)
    regional_champion = Bits(1, bool)
    national_champion = Bits(1, bool)
    country = Bits(1, bool)
    national = Bits(1, bool)
    earth = Bits(1, bool)
    world = Bits(1, bool)

    unused = Bits(4, int)

    obedience = Bits(1, bool)


class ExpGroup(Enum):
    MEDIUM_FAST_SPECIES = nonmember({
        PkmnSpecies.ARBOK,
        PkmnSpecies.BALTOY,
        PkmnSpecies.BARBOACH,
        PkmnSpecies.BEAUTIFLY,
        PkmnSpecies.BEEDRILL,
        PkmnSpecies.BUTTERFREE,
        PkmnSpecies.CAMERUPT,
        PkmnSpecies.CASCOON,
        PkmnSpecies.CASTFORM,
        PkmnSpecies.CATERPIE,
        PkmnSpecies.CLAYDOL,
        PkmnSpecies.CROBAT,
        PkmnSpecies.CUBONE,
        PkmnSpecies.DEWGONG,
        PkmnSpecies.DIGLETT,
        PkmnSpecies.DITTO,
        PkmnSpecies.DODRIO,
        PkmnSpecies.DODUO,
        PkmnSpecies.DONPHAN,
        PkmnSpecies.DROWZEE,
        PkmnSpecies.DUGTRIO,
        PkmnSpecies.DUNSPARCE,
        PkmnSpecies.DUSTOX,
        PkmnSpecies.EEVEE,
        PkmnSpecies.EKANS,
        PkmnSpecies.ELECTABUZZ,
        PkmnSpecies.ELECTRODE,
        PkmnSpecies.ELEKID,
        PkmnSpecies.ESPEON,
        PkmnSpecies.FARFETCHD,
        PkmnSpecies.FEAROW,
        PkmnSpecies.FLAREON,
        PkmnSpecies.FORRETRESS,
        PkmnSpecies.FURRET,
        PkmnSpecies.GIRAFARIG,
        PkmnSpecies.GLALIE,
        PkmnSpecies.GOLBAT,
        PkmnSpecies.GOLDEEN,
        PkmnSpecies.GOLDUCK,
        PkmnSpecies.GRIMER,
        PkmnSpecies.HITMONCHAN,
        PkmnSpecies.HITMONLEE,
        PkmnSpecies.HITMONTOP,
        PkmnSpecies.HOOTHOOT,
        PkmnSpecies.HORSEA,
        PkmnSpecies.HYPNO,
        PkmnSpecies.JOLTEON,
        PkmnSpecies.JYNX,
        PkmnSpecies.KABUTO,
        PkmnSpecies.KABUTOPS,
        PkmnSpecies.KAKUNA,
        PkmnSpecies.KANGASKHAN,
        PkmnSpecies.KINGDRA,
        PkmnSpecies.KINGLER,
        PkmnSpecies.KOFFING,
        PkmnSpecies.KRABBY,
        PkmnSpecies.LICKITUNG,
        PkmnSpecies.LINOONE,
        PkmnSpecies.MAGBY,
        PkmnSpecies.MAGCARGO,
        PkmnSpecies.MAGMAR,
        PkmnSpecies.MAGNEMITE,
        PkmnSpecies.MAGNETON,
        PkmnSpecies.MANKEY,
        PkmnSpecies.MAROWAK,
        PkmnSpecies.MASQUERAIN,
        PkmnSpecies.MEDICHAM,
        PkmnSpecies.MEDITITE,
        PkmnSpecies.MEOWTH,
        PkmnSpecies.METAPOD,
        PkmnSpecies.MIGHTYENA,
        PkmnSpecies.MINUN,
        PkmnSpecies.MUK,
        PkmnSpecies.NATU,
        PkmnSpecies.NINETALES,
        PkmnSpecies.NOCTOWL,
        PkmnSpecies.NOSEPASS,
        PkmnSpecies.NUMEL,
        PkmnSpecies.OCTILLERY,
        PkmnSpecies.OMANYTE,
        PkmnSpecies.OMASTAR,
        PkmnSpecies.ONIX,
        PkmnSpecies.PARAS,
        PkmnSpecies.PARASECT,
        PkmnSpecies.PELIPPER,
        PkmnSpecies.PERSIAN,
        PkmnSpecies.PHANPY,
        PkmnSpecies.PICHU,
        PkmnSpecies.PIKACHU,
        PkmnSpecies.PINECO,
        PkmnSpecies.PLUSLE,
        PkmnSpecies.PONYTA,
        PkmnSpecies.POOCHYENA,
        PkmnSpecies.PORYGON,
        PkmnSpecies.PORYGON2,
        PkmnSpecies.PRIMEAPE,
        PkmnSpecies.PSYDUCK,
        PkmnSpecies.QUAGSIRE,
        PkmnSpecies.QWILFISH,
        PkmnSpecies.RAICHU,
        PkmnSpecies.RAPIDASH,
        PkmnSpecies.RATICATE,
        PkmnSpecies.RATTATA,
        PkmnSpecies.REMORAID,
        PkmnSpecies.SANDSHREW,
        PkmnSpecies.SANDSLASH,
        PkmnSpecies.SCIZOR,
        PkmnSpecies.SCYTHER,
        PkmnSpecies.SEADRA,
        PkmnSpecies.SEAKING,
        PkmnSpecies.SEEL,
        PkmnSpecies.SENTRET,
        PkmnSpecies.SILCOON,
        PkmnSpecies.SLOWBRO,
        PkmnSpecies.SLOWKING,
        PkmnSpecies.SLOWPOKE,
        PkmnSpecies.SLUGMA,
        PkmnSpecies.SMOOCHUM,
        PkmnSpecies.SNORUNT,
        PkmnSpecies.SPEAROW,
        PkmnSpecies.STEELIX,
        PkmnSpecies.SUDOWOODO,
        PkmnSpecies.SURSKIT,
        PkmnSpecies.TANGELA,
        PkmnSpecies.TEDDIURSA,
        PkmnSpecies.TORKOAL,
        PkmnSpecies.TYROGUE,
        PkmnSpecies.UMBREON,
        PkmnSpecies.UNOWN,
        PkmnSpecies.URSARING,
        PkmnSpecies.VAPOREON,
        PkmnSpecies.VENOMOTH,
        PkmnSpecies.VENONAT,
        PkmnSpecies.VOLTORB,
        PkmnSpecies.VULPIX,
        PkmnSpecies.WEEDLE,
        PkmnSpecies.WEEZING,
        PkmnSpecies.WHISCASH,
        PkmnSpecies.WINGULL,
        PkmnSpecies.WOBBUFFET,
        PkmnSpecies.WOOPER,
        PkmnSpecies.WURMPLE,
        PkmnSpecies.WYNAUT,
        PkmnSpecies.XATU,
        PkmnSpecies.YANMA,
        PkmnSpecies.ZIGZAGOON,
        PkmnSpecies.ZUBAT,
    })

    ERRATIC_SPECIES = nonmember({
        PkmnSpecies.ALTARIA,
        PkmnSpecies.ANORITH,
        PkmnSpecies.ARMALDO,
        PkmnSpecies.CLAMPERL,
        PkmnSpecies.CRADILY,
        PkmnSpecies.FEEBAS,
        PkmnSpecies.GOREBYSS,
        PkmnSpecies.HUNTAIL,
        PkmnSpecies.LILEEP,
        PkmnSpecies.MILOTIC,
        PkmnSpecies.NINCADA,
        PkmnSpecies.NINJASK,
        PkmnSpecies.SHEDINJA,
        PkmnSpecies.SWABLU,
        PkmnSpecies.VOLBEAT,
        PkmnSpecies.ZANGOOSE,
    })

    FLUCTUATING_SPECIES = nonmember({
        PkmnSpecies.BRELOOM,
        PkmnSpecies.CORPHISH,
        PkmnSpecies.CRAWDAUNT,
        PkmnSpecies.GULPIN,
        PkmnSpecies.HARIYAMA,
        PkmnSpecies.ILLUMISE,
        PkmnSpecies.MAKUHITA,
        PkmnSpecies.SEVIPER,
        PkmnSpecies.SHROOMISH,
        PkmnSpecies.SWALOT,
        PkmnSpecies.WAILMER,
        PkmnSpecies.WAILORD,
    })

    MEDIUM_SLOW_SPECIES = nonmember({
        PkmnSpecies.ABRA,
        PkmnSpecies.ABSOL,
        PkmnSpecies.ALAKAZAM,
        PkmnSpecies.AMPHAROS,
        PkmnSpecies.BAYLEEF,
        PkmnSpecies.BELLOSSOM,
        PkmnSpecies.BELLSPROUT,
        PkmnSpecies.BLASTOISE,
        PkmnSpecies.BLAZIKEN,
        PkmnSpecies.BULBASAUR,
        PkmnSpecies.CACNEA,
        PkmnSpecies.CACTURNE,
        PkmnSpecies.CELEBI,
        PkmnSpecies.CHARIZARD,
        PkmnSpecies.CHARMANDER,
        PkmnSpecies.CHARMELEON,
        PkmnSpecies.CHIKORITA,
        PkmnSpecies.COMBUSKEN,
        PkmnSpecies.CROCONAW,
        PkmnSpecies.CYNDAQUIL,
        PkmnSpecies.EXPLOUD,
        PkmnSpecies.FERALIGATR,
        PkmnSpecies.FLAAFFY,
        PkmnSpecies.FLYGON,
        PkmnSpecies.GASTLY,
        PkmnSpecies.GENGAR,
        PkmnSpecies.GEODUDE,
        PkmnSpecies.GLIGAR,
        PkmnSpecies.GLOOM,
        PkmnSpecies.GOLEM,
        PkmnSpecies.GRAVELER,
        PkmnSpecies.GROVYLE,
        PkmnSpecies.HAUNTER,
        PkmnSpecies.HOPPIP,
        PkmnSpecies.IVYSAUR,
        PkmnSpecies.JUMPLUFF,
        PkmnSpecies.KADABRA,
        PkmnSpecies.KECLEON,
        PkmnSpecies.LOMBRE,
        PkmnSpecies.LOTAD,
        PkmnSpecies.LOUDRED,
        PkmnSpecies.LUDICOLO,
        PkmnSpecies.MACHAMP,
        PkmnSpecies.MACHOKE,
        PkmnSpecies.MACHOP,
        PkmnSpecies.MAREEP,
        PkmnSpecies.MARSHTOMP,
        PkmnSpecies.MEGANIUM,
        PkmnSpecies.MEW,
        PkmnSpecies.MUDKIP,
        PkmnSpecies.MURKROW,
        PkmnSpecies.NIDOKING,
        PkmnSpecies.NIDOQUEEN,
        PkmnSpecies.NIDORINA,
        PkmnSpecies.NIDORINO,
        PkmnSpecies.NUZLEAF,
        PkmnSpecies.ODDISH,
        PkmnSpecies.PIDGEOT,
        PkmnSpecies.PIDGEOTTO,
        PkmnSpecies.PIDGEY,
        PkmnSpecies.POLITOED,
        PkmnSpecies.POLIWAG,
        PkmnSpecies.POLIWHIRL,
        PkmnSpecies.POLIWRATH,
        PkmnSpecies.QUILAVA,
        PkmnSpecies.ROSELIA,
        PkmnSpecies.SABLEYE,
        PkmnSpecies.SCEPTILE,
        PkmnSpecies.SEALEO,
        PkmnSpecies.SEEDOT,
        PkmnSpecies.SHIFTRY,
        PkmnSpecies.SHUCKLE,
        PkmnSpecies.SKIPLOOM,
        PkmnSpecies.SNEASEL,
        PkmnSpecies.SPHEAL,
        PkmnSpecies.SQUIRTLE,
        PkmnSpecies.SUNFLORA,
        PkmnSpecies.SUNKERN,
        PkmnSpecies.SWAMPERT,
        PkmnSpecies.SWELLOW,
        PkmnSpecies.TAILLOW,
        PkmnSpecies.TORCHIC,
        PkmnSpecies.TOTODILE,
        PkmnSpecies.TRAPINCH,
        PkmnSpecies.TREECKO,
        PkmnSpecies.TYPHLOSION,
        PkmnSpecies.VENUSAUR,
        PkmnSpecies.VIBRAVA,
        PkmnSpecies.VICTREEBEL,
        PkmnSpecies.VILEPLUME,
        PkmnSpecies.WALREIN,
        PkmnSpecies.WARTORTLE,
        PkmnSpecies.WEEPINBELL,
        PkmnSpecies.WHISMUR,
    })

    FAST_SPECIES = nonmember({
        PkmnSpecies.AIPOM,
        PkmnSpecies.ARIADOS,
        PkmnSpecies.AZUMARILL,
        PkmnSpecies.AZURILL,
        PkmnSpecies.BANETTE,
        PkmnSpecies.BLISSEY,
        PkmnSpecies.CHANSEY,
        PkmnSpecies.CHIMECHO,
        PkmnSpecies.CLEFABLE,
        PkmnSpecies.CLEFAIRY,
        PkmnSpecies.CLEFFA,
        PkmnSpecies.CORSOLA,
        PkmnSpecies.DELCATTY,
        PkmnSpecies.DELIBIRD,
        PkmnSpecies.DUSCLOPS,
        PkmnSpecies.DUSKULL,
        PkmnSpecies.GRANBULL,
        PkmnSpecies.GRUMPIG,
        PkmnSpecies.IGGLYBUFF,
        PkmnSpecies.JIGGLYPUFF,
        PkmnSpecies.LEDIAN,
        PkmnSpecies.LEDYBA,
        PkmnSpecies.LUNATONE,
        PkmnSpecies.LUVDISC,
        PkmnSpecies.MARILL,
        PkmnSpecies.MAWILE,
        PkmnSpecies.MISDREAVUS,
        PkmnSpecies.SHUPPET,
        PkmnSpecies.SKITTY,
        PkmnSpecies.SMEARGLE,
        PkmnSpecies.SNUBBULL,
        PkmnSpecies.SOLROCK,
        PkmnSpecies.SPINARAK,
        PkmnSpecies.SPINDA,
        PkmnSpecies.SPOINK,
        PkmnSpecies.TOGEPI,
        PkmnSpecies.TOGETIC,
        PkmnSpecies.WIGGLYTUFF,
    })

    SLOW_SPECIES = nonmember({
        PkmnSpecies.AERODACTYL,
        PkmnSpecies.AGGRON,
        PkmnSpecies.ARCANINE,
        PkmnSpecies.ARON,
        PkmnSpecies.ARTICUNO,
        PkmnSpecies.BAGON,
        PkmnSpecies.BELDUM,
        PkmnSpecies.CARVANHA,
        PkmnSpecies.CHINCHOU,
        PkmnSpecies.CLOYSTER,
        PkmnSpecies.DEOXYS,
        PkmnSpecies.DRAGONAIR,
        PkmnSpecies.DRAGONITE,
        PkmnSpecies.DRATINI,
        PkmnSpecies.ELECTRIKE,
        PkmnSpecies.ENTEI,
        PkmnSpecies.EXEGGCUTE,
        PkmnSpecies.EXEGGUTOR,
        PkmnSpecies.GARDEVOIR,
        PkmnSpecies.GROUDON,
        PkmnSpecies.GROWLITHE,
        PkmnSpecies.GYARADOS,
        PkmnSpecies.HERACROSS,
        PkmnSpecies.HOUNDOOM,
        PkmnSpecies.HOUNDOUR,
        PkmnSpecies.JIRACHI,
        PkmnSpecies.KIRLIA,
        PkmnSpecies.KYOGRE,
        PkmnSpecies.LAIRON,
        PkmnSpecies.LANTURN,
        PkmnSpecies.LAPRAS,
        PkmnSpecies.LARVITAR,
        PkmnSpecies.LATIAS,
        PkmnSpecies.LATIOS,
        PkmnSpecies.LUGIA,
        PkmnSpecies.MAGIKARP,
        PkmnSpecies.MANECTRIC,
        PkmnSpecies.MANTINE,
        PkmnSpecies.METAGROSS,
        PkmnSpecies.METANG,
        PkmnSpecies.MEWTWO,
        PkmnSpecies.MILTANK,
        PkmnSpecies.MOLTRES,
        PkmnSpecies.PILOSWINE,
        PkmnSpecies.PINSIR,
        PkmnSpecies.PUPITAR,
        PkmnSpecies.RAIKOU,
        PkmnSpecies.RALTS,
        PkmnSpecies.RAYQUAZA,
        PkmnSpecies.REGICE,
        PkmnSpecies.REGIROCK,
        PkmnSpecies.REGISTEEL,
        PkmnSpecies.RELICANTH,
        PkmnSpecies.RHYDON,
        PkmnSpecies.RHYHORN,
        PkmnSpecies.SALAMENCE,
        PkmnSpecies.SHARPEDO,
        PkmnSpecies.SHELGON,
        PkmnSpecies.SHELLDER,
        PkmnSpecies.SKARMORY,
        PkmnSpecies.SLAKING,
        PkmnSpecies.SLAKOTH,
        PkmnSpecies.SNORLAX,
        PkmnSpecies.STANTLER,
        PkmnSpecies.STARMIE,
        PkmnSpecies.STARYU,
        PkmnSpecies.SUICUNE,
        PkmnSpecies.SWINUB,
        PkmnSpecies.TAUROS,
        PkmnSpecies.TENTACOOL,
        PkmnSpecies.TENTACRUEL,
        PkmnSpecies.TROPIUS,
        PkmnSpecies.TYRANITAR,
        PkmnSpecies.VIGOROTH,
        PkmnSpecies.ZAPDOS,
    })

    ERRATIC = auto()
    FAST = auto()
    MEDIUM_FAST = auto()
    MEDIUM_SLOW = auto()
    SLOW = auto()
    FLUCTUATING = auto()

    @classmethod
    def from_species(cls, species: PkmnSpecies) -> Self:
        if species in cls.MEDIUM_FAST_SPECIES:
            return cls(cls.MEDIUM_FAST)
        elif species in cls.ERRATIC_SPECIES:
            return cls(cls.ERRATIC)
        elif species in cls.MEDIUM_SLOW_SPECIES:
            return cls(cls.MEDIUM_SLOW)
        elif species in cls.FAST_SPECIES:
            return cls(cls.FAST)
        elif species in cls.SLOW_SPECIES:
            return cls(cls.SLOW)
        raise ValueError("Invalid species")



class LevelHelper:
    @staticmethod
    def exp2lvl(exp: int, species: PkmnSpecies) -> int:
        for lvl in range(1, 101):
            actual_exp = LevelHelper.lvl2exp(lvl, species)
            if actual_exp > exp:
                return lvl - 1
        return 100

    _lvl2exp = {
        ExpGroup.ERRATIC: [0, 15, 52, 122, 237, 406, 637, 942, 1326, 1800, 2369, 3041, 3822, 4719, 5737, 6881, 8155, 9564, 11111, 12800, 14632, 16610, 18737, 21012, 23437, 26012, 28737, 31610, 34632, 37800, 41111, 44564, 48155, 51881, 55737, 59719, 63822, 68041, 72369, 76800, 81326, 85942, 90637, 95406, 100237, 105122, 110052, 115015, 120001, 125000, 131324, 137795, 144410, 151165, 158056, 165079, 172229, 179503, 186894, 194400, 202013, 209728, 217540, 225443, 233431, 241496, 249633, 257834, 267406, 276458, 286328, 296358, 305767, 316074, 326531, 336255, 346965, 357812, 367807, 378880, 390077, 400293, 411686, 423190, 433572, 445239, 457001, 467489, 479378, 491346, 501878, 513934, 526049, 536557, 548720, 560922, 571333, 583539, 591882, 600000],
        ExpGroup.FAST: [0, 6, 21, 51, 100, 172, 274, 409, 583, 800, 1064, 1382, 1757, 2195, 2700, 3276, 3930, 4665, 5487, 6400, 7408, 8518, 9733, 11059, 12500, 14060, 15746, 17561, 19511, 21600, 23832, 26214, 28749, 31443, 34300, 37324, 40522, 43897, 47455, 51200, 55136, 59270, 63605, 68147, 72900, 77868, 83058, 88473, 94119, 100000, 106120, 112486, 119101, 125971, 133100, 140492, 148154, 156089, 164303, 172800, 181584, 190662, 200037, 209715, 219700, 229996, 240610, 251545, 262807, 274400, 286328, 298598, 311213, 324179, 337500, 351180, 365226, 379641, 394431, 409600, 425152, 441094, 457429, 474163, 491300, 508844, 526802, 545177, 563975, 583200, 602856, 622950, 643485, 664467, 685900, 707788, 730138, 752953, 776239, 800000],
        ExpGroup.MEDIUM_FAST: [0, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744, 3375, 4096, 4913, 5832, 6859, 8000, 9261, 10648, 12167, 13824, 15625, 17576, 19683, 21952, 24389, 27000, 29791, 32768, 35937, 39304, 42875, 46656, 50653, 54872, 59319, 64000, 68921, 74088, 79507, 85184, 91125, 97336, 103823, 110592, 117649, 125000, 132651, 140608, 148877, 157464, 166375, 175616, 185193, 195112, 205379, 216000, 226981, 238328, 250047, 262144, 274625, 287496, 300763, 314432, 328509, 343000, 357911, 373248, 389017, 405224, 421875, 438976, 456533, 474552, 493039, 512000, 531441, 551368, 571787, 592704, 614125, 636056, 658503, 681472, 704969, 729000, 753571, 778688, 804357, 830584, 857375, 884736, 912673, 941192, 970299, 1000000],
        ExpGroup.MEDIUM_SLOW: [0, 9, 57, 96, 135, 179, 236, 314, 419, 560, 742, 973, 1261, 1612, 2035, 2535, 3120, 3798, 4575, 5460, 6458, 7577, 8825, 10208, 11735, 13411, 15244, 17242, 19411, 21760, 24294, 27021, 29949, 33084, 36435, 40007, 43808, 47846, 52127, 56660, 61450, 66505, 71833, 77440, 83335, 89523, 96012, 102810, 109923, 117360, 125126, 133229, 141677, 150476, 159635, 169159, 179056, 189334, 199999, 211060, 222522, 234393, 246681, 259392, 272535, 286115, 300140, 314618, 329555, 344960, 360838, 377197, 394045, 411388, 429235, 447591, 466464, 485862, 505791, 526260, 547274, 568841, 590969, 613664, 636935, 660787, 685228, 710266, 735907, 762160, 789030, 816525, 844653, 873420, 902835, 932903, 963632, 995030, 1027103, 1059860],
        ExpGroup.SLOW: [0, 10, 33, 80, 156, 270, 428, 640, 911, 1250, 1663, 2160, 2746, 3430, 4218, 5120, 6141, 7290, 8573, 10000, 11576, 13310, 15208, 17280, 19531, 21970, 24603, 27440, 30486, 33750, 37238, 40960, 44921, 49130, 53593, 58320, 63316, 68590, 74148, 80000, 86151, 92610, 99383, 106480, 113906, 121670, 129778, 138240, 147061, 156250, 165813, 175760, 186096, 196830, 207968, 219520, 231491, 243890, 256723, 270000, 283726, 297910, 312558, 327680, 343281, 359370, 375953, 393040, 410636, 428750, 447388, 466560, 486271, 506530, 527343, 548720, 570666, 593190, 616298, 640000, 664301, 689210, 714733, 740880, 767656, 795070, 823128, 851840, 881211, 911250, 941963, 973360, 1005446, 1038230, 1071718, 1105920, 1140841, 1176490, 1212873, 1250000],
        ExpGroup.FLUCTUATING: [0, 4, 13, 32, 65, 112, 178, 276, 393, 540, 745, 967, 1230, 1591, 1957, 2457, 3046, 3732, 4526, 5440, 6482, 7666, 9003, 10506, 12187, 14060, 16140, 18439, 20974, 23760, 26811, 30146, 33780, 37731, 42017, 46656, 50653, 55969, 60505, 66560, 71677, 78533, 84277, 91998, 98415, 107069, 114205, 123863, 131766, 142500, 151222, 163105, 172697, 185807, 196322, 210739, 222231, 238036, 250562, 267840, 281456, 300293, 315059, 335544, 351520, 373744, 390991, 415050, 433631, 459620, 479600, 507617, 529063, 559209, 582187, 614566, 639146, 673863, 700115, 737280, 765275, 804997, 834809, 877201, 908905, 954084, 987754, 1035837, 1071552, 1122660, 1160499, 1214753, 1254796, 1312322, 1354652, 1415577, 1460276, 1524731, 1571884, 1640000],
    }

    @staticmethod
    def lvl2exp(lvl: int, species: PkmnSpecies) -> int:
        group = ExpGroup.from_species(species)
        return LevelHelper._lvl2exp[group][lvl-1]
