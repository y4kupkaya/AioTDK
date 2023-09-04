import asyncio
import json
import urllib.parse
from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from aiohttp import ClientSession

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
MeaningProperties = namedtuple(
    "MeaningProperties", ["id", "kind", "full_name", "short_name", "number"]
)


REMOTE_AUTOCOMPLETE_INDEX = "autocomplete.json"
REMOTE_UPDATED_TURKISH_DICTIONARY = "gts"
REMOTE_UPDATED_TURKISH_DICTIONARY_ID_ENDPOINT = "gts_id"
REMOTE_SUGGESTIONS_DICTIONARY = "oneri"
REMOTE_GENERAL_SEARCH_PARAMETER_MEDIATOR = "?ara="
REMOTE_SUGGESTIONS_SEARCH_PARAMETER_MEDIATOR = "?soz="
REMOTE_ID_MEDIATOR = "?id="

HOST = "https://sozluk.gov.tr/"


def general_search(term: str):
    return (
        f"{HOST}"
        f"{REMOTE_UPDATED_TURKISH_DICTIONARY}"
        f"{REMOTE_GENERAL_SEARCH_PARAMETER_MEDIATOR}"
        f"{urllib.parse.quote(term)}"
    )


_lookup_table = {}


class MeaningPropertyKind(Enum):
    FIELD = 1
    PART_OF_SPEECH = 3
    TONE = 4


class MeaningProperty(Enum):
    EXCLAMATION = MeaningProperties(
        18, MeaningPropertyKind.PART_OF_SPEECH, "ünlem", "ünl.", 29
    )
    NOUN = MeaningProperties(19, MeaningPropertyKind.PART_OF_SPEECH, "isim", "a.", 30)
    ADJECTIVE = MeaningProperties(
        20, MeaningPropertyKind.PART_OF_SPEECH, "sıfat", "sf.", 31
    )
    DATIVE = MeaningProperties(21, MeaningPropertyKind.PART_OF_SPEECH, "-e", "-e", 32)
    ACCUSATIVE = MeaningProperties(
        22, MeaningPropertyKind.PART_OF_SPEECH, "-i", "-i", 33
    )
    INTRANSITIVE = MeaningProperties(
        23, MeaningPropertyKind.PART_OF_SPEECH, "nesnesiz", "nsz.", 34
    )
    ADVERB = MeaningProperties(
        24, MeaningPropertyKind.PART_OF_SPEECH, "zarf", "zf.", 35
    )
    BY = MeaningProperties(25, MeaningPropertyKind.PART_OF_SPEECH, "-le", "-le", 36)
    ABLATIVE = MeaningProperties(
        26, MeaningPropertyKind.PART_OF_SPEECH, "-den", "-den", 37
    )
    PARTICLE = MeaningProperties(
        27, MeaningPropertyKind.PART_OF_SPEECH, "edat", "e.", 38
    )
    CONJUNCTION = MeaningProperties(
        28, MeaningPropertyKind.PART_OF_SPEECH, "bağlaç", "bağ.", 39
    )
    PRONOUN = MeaningProperties(
        29, MeaningPropertyKind.PART_OF_SPEECH, "zamir", "zm.", 40
    )
    SLANG = MeaningProperties(30, MeaningPropertyKind.TONE, "argo", "argo", 41)
    OBSOLETE = MeaningProperties(31, MeaningPropertyKind.TONE, "eskimiş", "esk.", 42)
    METAPHOR = MeaningProperties(32, MeaningPropertyKind.TONE, "mecaz", "mec.", 43)
    LAY = MeaningProperties(33, MeaningPropertyKind.TONE, "halk ağzında", "hlk.", 44)
    COLLOQUIAL = MeaningProperties(
        34, MeaningPropertyKind.TONE, "teklifsiz konuşmada", "tkz.", 45
    )
    SATIRIC = MeaningProperties(35, MeaningPropertyKind.TONE, "alay yollu", "alay", 46)
    VULGAR = MeaningProperties(
        36, MeaningPropertyKind.TONE, "kaba konuşmada", "kaba", 47
    )
    JOCULAR = MeaningProperties(37, MeaningPropertyKind.TONE, "şaka yollu", "şaka", 48)
    INVECTIVE = MeaningProperties(
        38, MeaningPropertyKind.TONE, "hakaret yollu", "hkr.", 49
    )
    MUSIC = MeaningProperties(39, MeaningPropertyKind.FIELD, "müzik", "müz.", 88)
    SPORTS = MeaningProperties(40, MeaningPropertyKind.FIELD, "spor", "sp.", 89)
    BOTANY = MeaningProperties(
        41, MeaningPropertyKind.FIELD, "bitki bilimi", "bit. b.", 90
    )
    NAVAL = MeaningProperties(42, MeaningPropertyKind.FIELD, "denizcilik", "den.", 91)
    HISTORY = MeaningProperties(43, MeaningPropertyKind.FIELD, "tarih", "tar.", 92)
    ASTRONOMY = MeaningProperties(
        44, MeaningPropertyKind.FIELD, "gök bilimi", "gök b.", 93
    )
    GEOGRAPHY = MeaningProperties(45, MeaningPropertyKind.FIELD, "coğrafya", "coğ.", 94)
    GRAMMAR = MeaningProperties(46, MeaningPropertyKind.FIELD, "dil bilgisi", "db.", 95)
    PSYCHOLOGY = MeaningProperties(
        47, MeaningPropertyKind.FIELD, "ruh bilimi", "ruh b.", 96
    )
    CHEMISTRY = MeaningProperties(48, MeaningPropertyKind.FIELD, "kimya", "kim.", 97)
    ANATOMY = MeaningProperties(49, MeaningPropertyKind.FIELD, "anatomi", "anat.", 98)
    COMMERCE = MeaningProperties(50, MeaningPropertyKind.FIELD, "ticaret", "tic.", 99)
    LAW = MeaningProperties(51, MeaningPropertyKind.FIELD, "hukuk", "huk.", 100)
    MATHEMATICS = MeaningProperties(
        52, MeaningPropertyKind.FIELD, "matematik", "mat.", 101
    )
    ZOOLOGY = MeaningProperties(
        53, MeaningPropertyKind.FIELD, "hayvan bilimi", "hay. b.", 102
    )
    LITERATURE = MeaningProperties(
        54, MeaningPropertyKind.FIELD, "edebiyat", "ed.", 103
    )
    CINEMA = MeaningProperties(55, MeaningPropertyKind.FIELD, "sinema", "sin.", 104)
    BIOLOGY = MeaningProperties(56, MeaningPropertyKind.FIELD, "biyoloji", "biy.", 105)
    PHILOSOPHY = MeaningProperties(
        57, MeaningPropertyKind.FIELD, "felsefe", "fel.", 106
    )
    PHYSICS = MeaningProperties(58, MeaningPropertyKind.FIELD, "fizik", "fiz.", 108)
    THEATRICAL = MeaningProperties(
        59, MeaningPropertyKind.FIELD, "tiyatro", "tiy.", 109
    )
    GEOLOGY = MeaningProperties(60, MeaningPropertyKind.FIELD, "jeoloji", "jeol.", 110)
    TECHNICAL = MeaningProperties(61, MeaningPropertyKind.FIELD, "teknik", "tek.", 112)
    SOCIOLOGY = MeaningProperties(
        62, MeaningPropertyKind.FIELD, "toplum bilimi", "top. b.", 113
    )
    PHYSIOLOGY = MeaningProperties(
        63, MeaningPropertyKind.FIELD, "fizyoloji", "fizy.", 114
    )
    METEOROLOGY = MeaningProperties(
        64, MeaningPropertyKind.FIELD, "meteoroloji", "meteor.", 115
    )
    LOGIC = MeaningProperties(65, MeaningPropertyKind.FIELD, "mantık", "man.", 116)
    ECONOMY = MeaningProperties(66, MeaningPropertyKind.FIELD, "ekonomi", "ekon.", 117)
    ARCHITECTURE = MeaningProperties(
        67, MeaningPropertyKind.FIELD, "mimarlık", "mim.", 118
    )
    MINERALOGY = MeaningProperties(
        68, MeaningPropertyKind.FIELD, "mineraloji", "min.", 119
    )
    PEDAGOGY = MeaningProperties(
        69, MeaningPropertyKind.FIELD, "eğitim bilimi", "eğt.", 120
    )
    MILITARY = MeaningProperties(73, MeaningPropertyKind.FIELD, "askerlik", "ask.", 124)
    GEOMETRY = MeaningProperties(
        80, MeaningPropertyKind.FIELD, "geometri", "geom.", 253
    )
    TECHNOLOGY = MeaningProperties(
        81, MeaningPropertyKind.FIELD, "teknoloji", "tekno.", 264
    )
    AUXILIARY_VERB = MeaningProperties(
        82, MeaningPropertyKind.PART_OF_SPEECH, "yardımcı  fiil", "yar.", 271
    )
    LOCATIVE = MeaningProperties(
        83, MeaningPropertyKind.PART_OF_SPEECH, "-de", "-de", 274
    )
    LINGUISTICS = MeaningProperties(
        84, MeaningPropertyKind.FIELD, "dil bilimi", "dil b.", 289
    )
    MEDICINE = MeaningProperties(85, MeaningPropertyKind.FIELD, "tıp", "tıp", 307)
    TELEVISION = MeaningProperties(
        87, MeaningPropertyKind.FIELD, "televizyon", "TV", 325
    )
    RELIGION = MeaningProperties(
        88, MeaningPropertyKind.FIELD, "din bilgisi", "din b.", 326
    )
    MINING = MeaningProperties(96, MeaningPropertyKind.FIELD, "madencilik", "mdn.", 364)
    I_T = MeaningProperties(98, MeaningPropertyKind.FIELD, "bilişim", "bl.", 368)
    MYTHOLOGY = MeaningProperties(99, MeaningPropertyKind.FIELD, "mit.", "mit.", 376)
    ANTHROPOLOGY = MeaningProperties(
        105, MeaningPropertyKind.FIELD, "antropoloji", "ant.", 404
    )

    @staticmethod
    def get(arg):
        if isinstance(arg, dict):
            return _lookup_table[int(arg["ozellik_id"])]
        return _lookup_table[arg]


class TdkModel:
    def as_dict(self):
        def serialize(obj):
            if isinstance(obj, list):
                if len(obj) == 0:
                    return []
                return list(map(serialize, obj))
            elif isinstance(obj, TdkModel):
                return serialize(obj.as_dict())
            elif isinstance(obj, MeaningProperty):
                return serialize(obj.value.id)
            elif isinstance(obj, Enum):
                return serialize(obj.value)
            return obj

        return {k: serialize(v) for k, v in self.__dict__.items()}


@dataclass
class Writer(TdkModel):
    tdk_id: int
    full_name: str
    short_name: str

    def __str__(self) -> str:
        return self.full_name

    @staticmethod
    def parse(writer: dict) -> "Writer":
        return Writer(
            tdk_id=int(writer["yazar_id"]),
            full_name=writer["tam_adi"],
            short_name=writer["kisa_adi"],
        )


@dataclass
class MeaningExample(TdkModel):
    tdk_id: int
    meaning_id: int
    order: int
    example: str
    writer: Writer or None = None

    def __str__(self):
        return self.example

    @staticmethod
    def parse(example: dict) -> "MeaningExample":
        writer_parser = Writer.parse
        return MeaningExample(
            tdk_id=int(example["ornek_id"]),
            meaning_id=int(example["anlam_id"]),
            order=int(example["ornek_sira"]),
            example=example["ornek"],
            writer=writer_parser(example["yazar"][0]) if "yazar" in example else None,
        )


@dataclass
class Proverb(TdkModel):
    tdk_id: int
    proverb: str
    prefix: str or None = None

    def __str__(self):
        return self.proverb

    @staticmethod
    def parse(proverb: dict) -> "Proverb":
        return Proverb(
            tdk_id=int(proverb["madde_id"]),
            proverb=proverb["madde"],
            prefix=proverb["on_taki"],
        )


@dataclass
class Meaning(TdkModel):
    meaning: str
    tdk_id: int
    order: int
    is_verb: bool
    entry_id: int
    examples: List[MeaningExample]
    properties: List[MeaningProperty]

    def __str__(self):
        return self.meaning

    @staticmethod
    def parse(meaning: dict) -> "Meaning":
        example_parser = MeaningExample.parse
        example_property_parser = MeaningProperty.get
        return Meaning(
            meaning=meaning["anlam"],
            tdk_id=int(meaning["anlam_id"]),
            order=int(meaning["anlam_sira"]),
            is_verb=bool(int(meaning["fiil"])),
            entry_id=int(meaning["madde_id"]),
            examples=list(map(example_parser, meaning.get("orneklerListe", []))),
            properties=list(
                map(example_property_parser, meaning.get("ozelliklerListe", []))
            ),
        )


class OriginLanguage(Enum):
    ORIGINAL = 0
    COMPOUND = 19

    ARABIC = 11
    PERSIAN = 12
    FRENCH = 13
    ITALIAN = 14
    GREEK = 15
    LATIN = 16
    ENGLISH = 18
    SPANISH = 20
    ARMENIAN = 21
    RUSSIAN = 22
    GERMAN = 23
    SLAVIC = 24
    HEBREW = 25
    HUNGARIAN = 26
    BULGARIAN = 27
    PORTUGUESE = 28
    JAPANESE = 346
    ALBANIAN = 348

    MONGOLIAN = 354
    MONGOLIAN_2 = 153

    FINNISH = 392
    ROMAIC = 393
    SOGDIAN = 395
    SERBIAN = 486
    KOREAN = 420


@dataclass
class Entry(TdkModel):
    tdk_id: int
    order: int
    entry: str
    plural: bool
    proper: bool
    origin_language: OriginLanguage
    original: str
    entry_normalized: str or None = None
    meanings: List[Meaning] = field(default_factory=list)
    proverbs: List[Proverb] = field(default_factory=list)
    pronunciation: str or None = None
    prefix: str or None = None
    suffix: str or None = None

    def __str__(self):
        return self.entry

    @staticmethod
    def parse(entry: dict) -> "Entry":
        meaning_parser = Meaning.parse
        proverb_parser = Proverb.parse
        return Entry(
            tdk_id=int(entry["madde_id"]),
            order=int(entry["kac"]),
            entry=entry["madde"],
            plural=bool(int(entry["cogul_mu"])),
            proper=bool(int(entry["ozel_mi"])),
            origin_language=OriginLanguage(int(entry["lisan_kodu"])),
            original=entry["lisan"],
            entry_normalized=entry["madde_duz"],
            meanings=list(map(meaning_parser, entry.get("anlamlarListe", []))),
            proverbs=list(map(proverb_parser, entry.get("atasozu", []))),
            pronunciation=entry["telaffuz"],
            prefix=entry["on_taki"],
            suffix=entry["taki"],
        )


def lowercase(
    word: str,
    alphabet: str = ALPHABET,
    remove_unknown_characters=True,
    remove_circumflex=True,
) -> str:
    """Removes all whitespace and punctuation from word and lowercase it.

    >>> lowercase("geçti Bor'un pazarı (sür eşeğini Niğde'ye)")
    "geçtiborunpazarısüreşeğininiğdeye"

    :return: A lowercase string without any whitespace or punctuation.
    """

    a_circumflex_replacement = "a" if remove_circumflex else "â"
    i_circumflex_replacement = "i" if remove_circumflex else "î"
    u_circumflex_replacement = "u" if remove_circumflex else "û"

    reconstructed_word = ""
    for letter in word:
        lower_letter = letter.lower()
        if letter == "I":
            reconstructed_word = f"{reconstructed_word}ı"
        elif letter == "İ":
            reconstructed_word = f"{reconstructed_word}i"
        elif letter in ["â", "Â"]:
            reconstructed_word = f"{reconstructed_word}{a_circumflex_replacement}"
        elif letter in ["î", "Î"]:
            reconstructed_word = f"{reconstructed_word}{i_circumflex_replacement}"
        elif letter in ["û", "Û"]:
            reconstructed_word = f"{reconstructed_word}{u_circumflex_replacement}"
        elif lower_letter in alphabet or not remove_unknown_characters:
            reconstructed_word = f"{reconstructed_word}{lower_letter}"
    return reconstructed_word


for enum_value in MeaningProperty:
    _lookup_table = {
        **_lookup_table,
        enum_value.value.id: enum_value,
        enum_value.value.full_name: enum_value,
        enum_value.value.short_name: enum_value,
    }
