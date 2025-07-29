from dataclasses import dataclass
from typing import TypeAlias, Optional
from enum import Enum
from urllib.parse import urlparse, parse_qs, urlencode

MeaningId: TypeAlias = int

class PartOfSpeechCode(Enum):  # Available code
    def __init__(self, en, ru, ru_brief):
        self.en = en
        self.ru = ru
        self.ru_brief = ru_brief

    n = ("noun", "существительное", "сущ.")
    v = ("verb", "глагол", "гл.")
    j = ("adjective", "прилагательное", "прил.")
    r = ("adverb", "наречие", "нар.")
    prp = ("preposition", "предлог", "предлог")
    prn = ("pronoun", "местоимение", "мест.")
    crd = ("cardinal number", "количественное числительное", "кол. числ.")
    cjc = ("conjunction", "союз", "союз")
    exc = ("interjection", "междометие", "межд.")
    det = ("article", "артикль", "артикль")
    abb = ("abbreviation", "сокращение", "сокращ.")
    x = ("particle", "частица", "частица")
    ord = ("ordinal number", "порядковое числительное", "поряд. числ.")
    md = ("modal verb", "модальный глагол", "мод. гл.")
    ph = ("phrase", "фраза", "фраза")
    phi = ("idiom", "идиома", "идиома")


@dataclass
class Translation:
    text: Optional[str]  # A text of a translation.
    note: Optional[str]  # A note about translation.


class Language(Enum):
    en = 'english'
    ru = 'russian'

class Pronunciation:
    '''
    handler link with own params
    example: https://vimbox-tts.skyeng.ru/api/v1/tts?text=Lacking+ease+or+grace.&lang=en&voice=male_2'
    '''
    def __init__(self, url: str, language: Language):
        __parse_result = urlparse(url)
        self.__scheme = __parse_result.scheme
        self.__netloc = __parse_result.netloc
        self.__path = __parse_result.path
        __params = parse_qs(__parse_result.query)
        __text = __params.get('text')[0]
        __lang = language.name
        self.__assembly_params_dict = {'text': __text,
                                       'lang': __lang,
                                       'voice': 'male_1'}
        if __params.get('isSsml') is not None:
            __is_ssml = __params.get('isSsml')[0]
            self.__assembly_params_dict['isSsml'] = __is_ssml

    @property
    def british_male(self):
        self.__assembly_params_dict['voice'] = 'male_1'
        params = urlencode(self.__assembly_params_dict)
        return f'{self.__scheme}://{self.__netloc}{self.__path}?{params}'

    @property
    def american_male(self):
        self.__assembly_params_dict['voice'] = 'male_2'
        params = urlencode(self.__assembly_params_dict)
        return f'{self.__scheme}://{self.__netloc}{self.__path}?{params}'

    @property
    def british_female(self):
        self.__assembly_params_dict['voice'] = 'female_1'
        params = urlencode(self.__assembly_params_dict)
        return f'{self.__scheme}://{self.__netloc}{self.__path}?{params}'

    @property
    def american_female(self):
        self.__assembly_params_dict['voice'] = 'female_2'
        params = urlencode(self.__assembly_params_dict)
        return f'{self.__scheme}://{self.__netloc}{self.__path}?{params}'

    def __repr__(self):
        return self.british_male

    def __str__(self):
        return self.british_male


@dataclass
class BriefMeaning:  # Meaning2
    id: MeaningId  # MeaningId.
    part_of_speech_code: Optional[PartOfSpeechCode]
    translation: Optional[str]
    translation_note: Optional[str]
    image_url: Optional[str]  #
    transcription: Optional[str]  #
    sound_url: Optional[Pronunciation]
    text: Optional[str]


@dataclass
class Properties:
    collocation: Optional[bool] #
    not_gradable: Optional[bool]
    irregular: Optional[bool] #
    past_tense: Optional[str] # "found",
    past_participle: Optional[str] # "found",
    transitivity: Optional[str] # "t", "i" "ti"
    countability: Optional[str]  # "c", cu
    plurality: Optional[str] # s , sp
    plural: Optional[str]
    irregular_plural: Optional[str]
    phrasal_verb: Optional[bool] # false,
    linking_verb: Optional[bool] #
    linking_type: Optional[str] # 'L + noun, L + adjective'
    sound_url: Optional[Pronunciation]  #
    false_friends: Optional[list]  #


@dataclass  #
class Definition:  #
    text: Optional[str]  #
    sound_url: Optional[Pronunciation]  #


@dataclass
class Example:
    text: Optional[str]  #
    sound_url: Optional[Pronunciation]  #


@dataclass
class MeaningWithSimilarTranslation:
    meaning_id: Optional[int] #
    frequency_percent: Optional[float]  #
    part_of_speech_abbreviation: Optional[str]  # часть речи на русском напрм: "гл."
    translation: Optional[str]  #
    translation_note: Optional[str]


@dataclass
class AlternativeTranslation:  #
    text: Optional[str]   #
    translation: Optional[str]   #
    translation_note: Optional[str]


@dataclass
class Meaning:
    id: MeaningId  # Meaning id.
    word_id: int  # Word is a group of meanings. We combine meanings by word entity.
    difficulty_level: Optional[int]  # There are 6 difficultyLevels: 1, 2, 3, 4, 5, 6.
    part_of_speech_code: PartOfSpeechCode  # String representation of a part of speech.
    prefix: Optional[str]  # Infinitive particle (to) or articles (a, the).
    text: Optional[str]  # Meaning text.
    sound_url: Optional[Pronunciation]  # URL to meaning sound.
    transcription: Optional[str]  # IPA phonetic transcription.
    properties: Properties  #
    updated_at: Optional[str]  #
    mnemonics: Optional[str]  #
    translation: Optional[str]  #
    translation_note: Optional[str]
    images_url: list[Optional[str]]  # A collection of an images.
    images_id: list[Optional[str]]
    definition: Optional[str]  #
    definition_sound_url: Optional[Pronunciation]
    examples: Optional[list[Example]] # Usage examples
    meanings_with_similar_translation: (
        Optional[list[MeaningWithSimilarTranslation]]) # Collection of meanings with similar translations.
    alternative_translations: (
        Optional[list[AlternativeTranslation]])  # Collection of alternative translations.


@dataclass
class Word:
    id: Optional[int]  #
    text: Optional[str]  #
    meanings: Optional[list[BriefMeaning]]  #