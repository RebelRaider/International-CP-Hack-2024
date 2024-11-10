import subprocess
import tempfile

import librosa
import pandas as pd
import torch
from catboost import Pool
from imagebind.model import ModalityType
from imagebind.utils import data
from loguru import logger

from ml.lifespan import whisper_model, device, imagebind_model, catboost_models, bert_tokenizer, bert_model
from ml.constants import LABEL_NAMES, EMBEDDING_FEATURES


class MlService:
    def __init__(self):
        self._whisper_model = whisper_model
        self._imagebind_model = imagebind_model

        self._catboost_models = catboost_models
        self._label_names = LABEL_NAMES
        self._embedding_features = EMBEDDING_FEATURES

        self._bert_tokenizer = bert_tokenizer
        self._bert_model = bert_model

        self.device = device

    def transcript_video(self, video: bytes) -> str:
        """
        Расшифровывает видео и возвращает текстовую транскрипцию.

        Параметры
        ----------
        video : bytes
            Видео в формате байтов, представляющее содержимое видеофайла для расшифровки.

        Возвращает
        -------
        str
            Текстовая транскрипция содержимого видео.

        Примечания
        ---------
        - Функция сохраняет видео во временный файл формата MP4 для передачи его
          в модель распознавания речи.
        - Используется предварительно обученная модель для транскрипции.
        - После обработки временный файл сохраняется, но может быть удалён после использования.
        """
        logger.debug("ML - Service - transcribe")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_audio:
            temp_audio.write(video)
            temp_audio_path = temp_audio.name
            result = self._whisper_model.transcribe(temp_audio_path)

            transcribe = result["text"]

        return transcribe

    def get_ocean(self, video: bytes, transcript: str) -> dict[str, float]:
        """
        Извлекает аудио- и текстовые признаки из входных данных и предсказывает значения OCEAN (черты личности) с помощью предобученных моделей CatBoost.

        Параметры
        ----------
        video : bytes
            Видео файл в байтовом формате, из которого будет извлечена аудиодорожка для последующего анализа.
        transcript : str
            Строка с текстовой расшифровкой речи из видео для извлечения текстовых признаков.

        Возвращает
        -------
        dict[str, float]
            Словарь, где ключами являются названия черт личности (OCEAN), а значениями — предсказанные модели результаты для каждой черты.

        Примечания
        ---------
        1. Метод использует временный файл для хранения аудиоданных, которые затем обрабатываются с целью извлечения признаков.
        2. Для каждого признака (аудио и текстового) создается объединенный словарь, который используется в качестве входных данных для моделей CatBoost.
        3. Прогнозы делаются по каждому имени метки из списка `_label_names`, и результаты сохраняются в словаре `answer`.

        Примеры
        --------
        >>> video_bytes = b'...\x00\x01\x02...'  # Пример байтового содержимого видео
        >>> transcript_text = "Текстовая расшифровка"
        >>> result = instance.get_ocean(video_bytes, transcript_text)
        >>> print(result)
        {'Openness': 0.75, 'Conscientiousness': 0.82, 'Extraversion': 0.65, 'Agreeableness': 0.78, 'Neuroticism': 0.54}
        """
        logger.debug("ML - Service - get_ocean")
        answer = {}

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_audio:
            temp_audio.write(video)

            audio, sr, audio_embeddings = self._extract_audio_embedding(temp_audio.name)

        text_embedding = self._extract_text_embedding(transcript)

        x = pd.DataFrame({
            "audio_embedding": [audio_embeddings.squeeze().cpu().tolist()],
            "text_embedding": [text_embedding.squeeze().cpu().tolist()]
        })

        for label_name in self._label_names:
            model = self._catboost_models[label_name]

            sample_pool = Pool(data=x, embedding_features=self._embedding_features)

            y_pred = model.predict(sample_pool)[0]

            answer[label_name] = y_pred

        return answer

    def _extract_audio_embedding(self, video_path):
        """
        Извлекает аудиовектор из видео.

        Параметры
        ----------
        video_path : str
            Путь к видеофайлу, из которого необходимо извлечь аудиодорожку.

        Возвращаемое значение
        ----------------------
        tuple
            Кортеж, содержащий:
            - audio : numpy.ndarray
                Массив, представляющий аудиоданные, загруженные из временного файла.
            - sr : int
                Частота дискретизации аудиоданных.
            - audio_embeddings : torch.Tensor
                Векторное представление аудиоданных, извлеченное моделью ImageBind.

        Описание
        ---------
        Данная функция использует библиотеку ffmpeg для извлечения аудиодорожки из
        видеофайла и сохранения её во временном WAV-файле. Затем с помощью библиотеки
        librosa аудиоданные загружаются и преобразуются в массив. После этого аудиоданные
        обрабатываются моделью ImageBind, чтобы получить векторное представление аудио.
        Функция возвращает массив аудиоданных, частоту дискретизации и среднее значение
        векторных представлений аудио.

        Исключения
        ----------
        - subprocess.CalledProcessError
            Генерируется, если выполнение команды ffmpeg завершилось с ошибкой.
        - FileNotFoundError
            Генерируется, если ffmpeg или необходимые библиотеки не установлены.
        """
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
            temp_audio_path = temp_audio_file.name
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    video_path,
                    temp_audio_path,
                    "-loglevel",
                    "error",
                ],
                check=True,
            )
            audio, sr = librosa.load(temp_audio_path, sr=None)

            inputs = {
                ModalityType.AUDIO: data.load_and_transform_audio_data(
                    [temp_audio_path], self.device
                )
            }
            with torch.inference_mode():
                audio_embeddings = self._imagebind_model(inputs)[
                    ModalityType.AUDIO
                ].mean(dim=0)

            return audio, sr, audio_embeddings

    def _extract_text_embedding(self, text) -> torch.Tensor:
        """
        Извлекает эмбеддинг для текста.

        Параметры
        ----------
        text : str
            Входной текст для извлечения эмбеддинга. Если строка пустая или не является строкой,
            будет использовано значение по умолчанию "<UNK>".

        Возвращает
        -------
        torch.Tensor
            Эмбеддинг текста, полученный с помощью модели ImageBind.

        Примечания
        ---------
        Функция использует метод `load_and_transform_text` для предварительной обработки текста,
        приводя его в формат, подходящий для обработки моделью. Затем эмбеддинг извлекается
        в режиме inference, что позволяет выполнять вычисления без сохранения промежуточных
        данных для обучения.

        Исключения
        ---------
        Проверка типа входных данных выполняется с целью обеспечения безопасности и предотвращения
        ошибок при передаче некорректного формата. Если переданный текст не соответствует
        ожидаемому типу, используется placeholder "<UNK>".
        """
        if not isinstance(text, str) or not text:
            text = "<UNK>"
        inputs = {ModalityType.TEXT: data.load_and_transform_text([text], self.device)}
        with torch.inference_mode():
            text_embedding = self._imagebind_model(inputs)[ModalityType.TEXT]
        return text_embedding

    def _generate_prompt(self, traits: dict) -> str:
        """
        Создает текстовый промпт на основе личностных показателей.

        Параметры
        ----------
        traits : dict
            Словарь с ключами, представляющими личностные характеристики (например,
            'extraversion', 'neuroticism', 'agreeableness', 'conscientiousness',
            'openness'), и значениями, описывающими степень выраженности каждой
            характеристики.

        Возвращает
        -------
        str
            Сформированный текстовый промпт, содержащий описание личностных черт и
            запрос на перечисление подходящих профессий для кандидата.

        Примечания
        ---------
        - Функция создает текстовый шаблон, который впоследствии используется для
          генерации рекомендаций на основе входных данных.
        - Включенные в шаблон характеристики помогают модели лучше понимать запрос
          и формировать релевантные результаты.
        """
        prompt = (
            f"У кандидата следующие показатели личности:\n"
            f"- Экстраверсия: {traits['extraversion']}\n"
            f"- Нейротизм: {traits['neuroticism']}\n"
            f"- Доброжелательность: {traits['agreeableness']}\n"
            f"- Сознательность: {traits['conscientiousness']}\n"
            f"- Открытость опыту: {traits['openness']}\n\n"
            f"На основе этих показателей перечислите наиболее подходящие профессии для кандидата. "
            f"Ответьте кратко, перечислив не более трех профессий."
        )
        return prompt

    def generate_advice(self, traits, max_length=150) -> str:
        """
        Генерирует краткие рекомендации по работе на основе личностных показателей.

        Параметры
        ----------
        traits : list
            Список строк, представляющих личностные характеристики или черты,
            которые будут использоваться для создания текста рекомендации.
        max_length : int, optional
            Максимальная длина генерируемого текста в символах (по умолчанию 150).

        Возвращает
        -------
        str
            Сгенерированный текст с рекомендацией, содержащий описание действий
            или советов, основанных на личностных характеристиках. Текст возвращается
            в виде строки без специальных токенов, только основная часть.

        Примечания
        ---------
        - Для генерации текста используется предварительно обученная модель языковой
          генерации.
        - Функция обрабатывает промпт с помощью токенизатора и модели, которая
          генерирует текст по заданным параметрам.
        - Выходной текст очищается от исходного промпта и возвращается только
          сгенерированная часть.
        """
        prompt = self._generate_prompt(traits)
        input_ids = self._bert_tokenizer.encode(prompt, return_tensors='pt').to(device)

        output = self._bert_model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=10,
            top_p=0.8,
            temperature=0.5,
            eos_token_id=self._bert_tokenizer.eos_token_id,
            pad_token_id=self._bert_tokenizer.pad_token_id
        )

        generated_text = self._bert_tokenizer.decode(output[0], skip_special_tokens=True)
        # Удаляем исходный промпт из сгенерированного текста
        advice = generated_text[len(prompt):].strip()
        # Оставляем только первую часть до точки или переноса строки
        return advice
