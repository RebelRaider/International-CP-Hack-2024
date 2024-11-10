## Inference pipline
![Inference.png](.assets/Inference.png)


## Jupyter
- Советы кандидатам: [comment.ipynb](ml/jupyters/comment.ipynb)
- Тренировка модели [train.ipynb](ml/jupyters/train.ipynb)
- Генерация датасета [dataset.ipynb](ml/jupyters/dataset.ipynb)
- Конвенторы в различные модели типов личности [convertors.py](utils/convertors.py)
  Используемые статьи:
    - McCrae, R. R., & Costa, P. T. Jr. (1989).
      Reinterpreting the Myers-Briggs Type Indicator From the Perspective of the Five-Factor Model of Personality.
      Journal of Personality, 57(1), 17–40.

    - De Fruyt, F., & Mervielde, I. (1997).
      The Five-Factor Model of personality and Holland's RIASEC interest types.
      Personality and Individual Differences, 23(1), 87-103.

    - Liao, H.-Y., Armstrong, P. I., & Rounds, J. (2008).
      Development and initial validation of public domain basic interest scales and an elaborated taxonomy of interests.
      Journal of Vocational Behavior, 73(1), 159-183.

## Как запустить
### 1. Клонирование репозитория

Для начала клонируйте репозиторий на вашу локальную машину:

```bash
git https://github.com/Hackathon-Hitchhiking/International-CP-Hack-2024.git
cd International-CP-Hack-2024
```

### 2. Создание и настройка файла окружения для Docker

Скопируйте пример файла окружения `.docker/.env.example` в `.docker/.env` и заполните необходимые переменные:

```bash
cp .docker/.env.example .docker/.env
nano .docker/.env
```

### 3. Создание и настройка файла конфигурации

Аналогично, скопируйте пример файла конфигурации `configs/.env.example` в `configs/.env` и укажите соответствующие переменные:

```bash
cp configs/.env.example configs/.env
nano configs/.env
```

### 5. скачать веса
Скачать веса с [яндекс диска](https://disk.yandex.ru/d/0lHbXoMT_nrV4Q) и положить их в ml/models

### 4. Запуск Docker Compose

После настройки всех конфигурационных файлов запустите Docker Compose для сборки и запуска контейнеров:

```bash
docker compose up --build
```

Убедитесь, что все переменные окружения и конфигурационные файлы корректно настроены перед запуском команд. 
