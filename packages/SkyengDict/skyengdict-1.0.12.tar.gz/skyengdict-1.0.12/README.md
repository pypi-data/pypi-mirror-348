# SkyengDict: Асинхронная библиотека для работы с Dictionary API Skyeng  
  
## Описание  
  
**SkyengDict** — это асинхронная библиотека на Python, предоставляющая доступ к API словаря Skyeng. Она позволяет искать слова, получать их значения и обрабатывать лингвистические данные, такие как части речи, переводы и произношения.  
  
### Установка  
  
```bash  
pip install skyengdict
```  
  
### Пример использования  
  
```python  
import asyncio  
from skyengdict import Dictionary  
from skyengdict.types import Meaning, BriefMeaning

  async def main():    
    tasks = []    
    async with Dictionary() as dictionary:
     
        result_1 = await dictionary.words('любовь', pagesize=1)    
        for word in result_1:    
            print(f"{word.text} - {word.meanings[0].translation}")    
                
        result_2 = await dictionary.meaning(45)    
        for mean in result_2:    
            print(f"{mean.text} - {mean.translation}\n")    
    
    await asyncio.gather(*tasks)    
    
if __name__ == '__main__':    
    asyncio.run(main())  
```  
  
  
### Класс `Dictionary`  
  
  **Параметры**:    
    - `logging`: Логировать процесс получения данных. По умолчанию `False`  
    - `rising`: Возбуждать исключения, если не найдены слова (значения), либо возвращать пустой список. По умолчанию `True`  
  
Основной класс для взаимодействия с API Skyeng Dictionary. Он предоставляет методы для поиска слов и получения их значений.  
  
#### Методы:  
  
- **`words(word: str, page: int = 1, pagesize: int = 0) -> list[Word]`**    
Выполняет поиск слов по заданному запросу.    
  
  **Параметры**:    
    - `word`: Слово для поиска (либо на английском, либо на русском).    
    - `page`: Номер страницы для пагинации.    
    - `pagesize`: Количество результатов на странице (если значение 0, то выводит результат всех найденых объектов `Word` в списке).    
  
  **Возвращает**:    
  - Список объектов `Word`, представляющих найденные слова с краткими значениями.  
  
- **`meaning(ids: int | list[int], data: str = None) -> list[Meaning]`**    
Получает подробную информацию о значениях слов по их идентификаторам.    
  
  **Параметры**:    
    - `ids`: Один идентификатор значения или список идентификаторов.    
    - `data`: Дата в формате строки.    
  
  **Возвращает**:    
  - Список объектов `Meaning`, представляющих полную информацию о значениях.  
  
## Типы данных  
  
### `Word`  
  
Представляет слово и связанные с ним краткие значения.  
  
- **Атрибуты**:  
  - `id`: Уникальный идентификатор слова.  
  - `text`: Слово в текстовом виде.  
  - `meanings`: Список объектов `BriefMeaning`, представляющих краткие значения слова.  
  
### `BriefMeaning`  
  
Краткое описание значения слова.  
  
- **Атрибуты**:  
  - `id`: Уникальный идентификатор значения.  
  - `part_of_speech_code`: Часть речи, представляемая перечислением `PartOfSpeechCode`.  
  - `translation`: Перевод текста.  
  - `translation_note`: Примечания к переводу.  
  - `image_url`: URL изображения.  
  - `transcription`: Фонетическая транскрипция в формате IPA.  
  - `sound_url`: Объект `Pronunciation`, содержащий ссылку на произношение слова.  
  - `text`: Слово на английском.  
  
### `Meaning`  
  
Подробное описание значения слова на английском.  
  
- **Атрибуты**:  
  - `id`: Уникальный идентификатор значения.  
  - `word_id`: Идентификатор слова, к которому относится значение.  
  - `difficulty_level`: Уровень сложности (от 1 до 6).  
  - `part_of_speech_code`: Часть речи для данного значения.  
  - `prefix`: Приставка или артикли (например, "to" или "the").  
  - `text`: Слово на английском.  
  - `sound_url`: Объект `Pronunciation`, представляющий ссылку URL на произношение.  
  - `transcription`: Фонетическая транскрипция.  
  - `properties`: Объект `Properties`, содержащий грамматическую информацию.  
  - `updated_at`: Дата последнего обновления значения.  
  - `mnemonics`: Мнемоническая подсказка для значения.  
  - `translation`: Перевод текста значения.  
  - `translation_note`: Примечания к переводу (если есть).  
  - `images_url`: Список URL изображений.  
  - `images_id`: Список идентификаторов изображений.
  - `definition`: Описание значения.  
  - `definition_sound_url`: Ссылка на произношение описания.  
  - `examples`: Список объектов `Example`, содержащих примеры использования.  
  - `meanings_with_similar_translation`: Список объектов `MeaningWithSimilarTranslation`, представляющих значения с похожими переводами.  
  - `alternative_translations`: Список объектов `AlternativeTranslation`, представляющих альтернативные переводы.  
  
### `PartOfSpeechCode` (Enum)  
  
Перечисление, представляющее часть речи слова. Доступны следующие значения:  
  
- `n`: существительное    
- `v`: глагол    
- `j`: прилагательное    
- `r`: наречие    
- `prp`: предлог    
- `prn`: местоимение    
- `crd`: количественное числительное    
- `cjc`: союз    
- `exc`: междометие    
- `det`: артикль    
- `abb`: сокращение    
- `x`: частица    
- `ord`: порядковое числительное    
- `md`: модальный глагол    
- `ph`: фраза    
- `phi`: идиома  
  
### `Pronunciation`  
  
Возвращает URL-адрес на аудио-запись с определенным произношением. 
  
- **Методы**:  
  - `british_male`: Возвращает URL-адрес для мужского голоса c британским произношением.  
  - `amrican_male`: Возвращает URL-адрес для мужского голоса c американским произношением.  
  - `british_female`: Возвращает URL-адрес для женского голоса c британским произношением.  
  - `amrican_female`: Возвращает URL-адрес для женского голоса c американским произношением.  

пример использования:
```
from skyengdict.type import Pronunciation

url = "https://vimbox-tts.skyeng.ru/api/v1/tts?text=Hello&lang=en&voice=male_2"
pronunciation = Pronunciation(url)
print(pronunciation.male_1)
```
  
### `Properties`  
  
Грамматические свойства слова.  
  
- **Атрибуты**:  
  - `collocation`: Указывает, является ли слово коллокацией.  
  - `irregular`: Указывает, является ли слово неправильным.  
  - `past_tense`: Прошедшая форма глагола (если применимо).  
  - `past_participle`: Причастие прошедшего времени (если применимо).  
  - `transitivity`: Переходность глагола (если применимо).  
  - `phrasal_verb`: Указывает, является ли слово фразовым глаголом.  
  - `sound_url`: Объект `Pronunciation` для звукового сопровождения.  
  - `false_friends`: Список ложных друзей (если есть).  
  
### `Translation`  
  
Представляет перевод слова или фразы.  
  
- **Атрибуты**:  
  - `text`: Текст перевода.  
  - `note`: Примечания к переводу.  
  
### `Example`  
  
Представляет пример использования слова.  
  
- **Атрибуты**:  
  - `text`: Пример предложения.  
  - `sound_url`: Объект `Pronunciation` для произношения примера.  

## Исключения (Exceptions)

Библиотека предоставляет следующие пользовательские исключения:

### `SkyConnectorError`

Исключение, возникающее при отсутствии соединения с сервером.

```
from skyengdict.exceptions import SkyConnectorError

try:
    async with Dictionary() as dictionary:
        await dictionary.words("example")    
except SkyConnectorError:
    print("Ошибка соединения с сервером SkyEng.")
```

### `WordsNotFound`

Исключение, возникающее, если слово не найдено.

```
from skyengdict.exceptions import WordsNotFound

try:
    async with Dictionary() as dictionary:
        word = await dictionary.words("nonexistentword0101010")
except WordsNotFound:
    print("Слово не найдено.")
```

### `MeaningsNotFound`

Исключение, возникающее, если значения слова не найдены.

```
from skyengdict.exceptions import MeaningsNotFound

try:
    async with Dictionary() as dictionary:
        meaning = await dictionary.meaning(1000)
except MeaningsNotFound:
    print("Значения для слова не найдены.")
```

## Предложения

Присоединяйтесь к обсуждению и развитию проекта. Буду рад вашим предложениям и пулреквестам. Мои другие текущие проекты читайте в [моем Telegram-канале](https://t.me/crunch_brain). 

## Лицензия  
  
Эта библиотека лицензирована под лицензией MIT.