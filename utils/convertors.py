import pandas as pd
import numpy as np
from typing import Dict, Tuple


class PersonalityConverter:
    """
    Класс для расчёта типов личности MBTI и RIASEC на основе оценок OCEAN.

    Основано на следующих исследованиях:

    - McCrae, R. R., & Costa, P. T. Jr. (1989).
      Reinterpreting the Myers-Briggs Type Indicator From the Perspective of the Five-Factor Model of Personality.
      Journal of Personality, 57(1), 17–40.

    - De Fruyt, F., & Mervielde, I. (1997).
      The Five-Factor Model of personality and Holland's RIASEC interest types.
      Personality and Individual Differences, 23(1), 87-103.

    Attributes:
    -----------
    MBTI_CORRELATIONS : dict
        Коэффициенты корреляции для измерений MBTI из работы McCrae и Costa (1989).
    RIASEC_CORRELATIONS : dict
        Коэффициенты корреляции для типов RIASEC из работы De Fruyt и Mervielde (1997).
    data : pd.DataFrame
        DataFrame с оценками черт OCEAN.
    trait_means : dict
        Средние значения для каждой черты OCEAN.
    trait_stds : dict
        Стандартные отклонения для каждой черты OCEAN.
    """

    # Коэффициенты корреляции для MBTI (McCrae & Costa, 1989)
    MBTI_CORRELATIONS = {
        "IE": {"extraversion": 0.74, "neuroticism": -0.36},
        "SN": {"openness": 0.72},
        "TF": {"agreeableness": 0.44},
        "JP": {"conscientiousness": 0.49},
    }

    # Коэффициенты корреляции для RIASEC (De Fruyt & Mervielde, 1997)
    RIASEC_CORRELATIONS = {
        "R": {
            "extraversion": 0.09,
            "agreeableness": -0.04,
            "conscientiousness": 0.15,
            "neuroticism": -0.07,
            "openness": -0.05,
        },
        "I": {
            "extraversion": -0.08,
            "agreeableness": -0.08,
            "conscientiousness": 0.13,
            "neuroticism": 0.12,
            "openness": 0.29,
        },
        "A": {
            "extraversion": 0.10,
            "agreeableness": 0.04,
            "conscientiousness": -0.08,
            "neuroticism": 0.10,
            "openness": 0.45,
        },
        "S": {
            "extraversion": 0.35,
            "agreeableness": 0.39,
            "conscientiousness": 0.09,
            "neuroticism": 0.08,
            "openness": 0.14,
        },
        "E": {
            "extraversion": 0.45,
            "agreeableness": 0.18,
            "conscientiousness": 0.05,
            "neuroticism": -0.02,
            "openness": 0.02,
        },
        "C": {
            "extraversion": 0.11,
            "agreeableness": 0.23,
            "conscientiousness": 0.42,
            "neuroticism": -0.02,
            "openness": -0.19,
        },
    }

    def __init__(self, data: pd.DataFrame):
        """
        Инициализация PersonalityConverter с данными оценок OCEAN.

        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame с оценками черт OCEAN, содержащий столбцы:
            'extraversion', 'neuroticism', 'agreeableness', 'conscientiousness', 'openness'.
        """
        self.data = data[
            [
                "extraversion",
                "neuroticism",
                "agreeableness",
                "conscientiousness",
                "openness",
            ]
        ]
        self.trait_means, self.trait_stds = self._calculate_trait_statistics()

    def _calculate_trait_statistics(self) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Вычисляет средние значения и стандартные отклонения для каждой черты OCEAN."""
        means = self.data.mean().to_dict()
        stds = self.data.std(
            ddof=0
        ).to_dict()  # Стандартное отклонение по генеральной совокупности
        return means, stds

    def _standardize_scores(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        """Стандартизирует исходные оценки OCEAN до Z-оценок."""
        return {
            trait: (raw_scores[trait] - self.trait_means[trait])
            / self.trait_stds[trait]
            for trait in raw_scores
        }

    def _calculate_dimension_scores(
        self, z_scores: Dict[str, float], correlations: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """Рассчитывает баллы для каждого измерения на основе Z-оценок и коэффициентов корреляции."""
        return {
            dimension: sum(
                z_scores.get(trait, 0) * weight for trait, weight in traits.items()
            )
            for dimension, traits in correlations.items()
        }

    def _normalize_scores(self, dimension_scores: Dict[str, float]) -> Dict[str, float]:
        """Нормализует баллы измерений в диапазоне от 0 до 1 с использованием логистической функции."""
        return {
            dim: 1 / (1 + np.exp(-score)) for dim, score in dimension_scores.items()
        }

    def calculate_mbti(
        self, raw_scores: Dict[str, float]
    ) -> Tuple[str, Dict[str, float]]:
        """
        Вычисляет тип MBTI и нормализованные баллы измерений.

        Parameters:
        -----------
        raw_scores : dict
            Исходные оценки OCEAN для индивида.

        Returns:
        --------
        mbti_type : str
            Предполагаемый тип MBTI (например, 'INTJ', 'ESFP').
        normalized_scores : dict
            Нормализованные баллы измерений от 0 до 1.
        """
        z_scores = self._standardize_scores(raw_scores)
        dimension_scores = self._calculate_dimension_scores(
            z_scores, self.MBTI_CORRELATIONS
        )
        normalized_scores = self._normalize_scores(dimension_scores)
        mbti_type = self._assign_mbti_type(dimension_scores)
        return mbti_type, normalized_scores

    def _assign_mbti_type(self, dimension_scores: Dict[str, float]) -> str:
        """Присваивает тип MBTI на основе баллов измерений."""
        mbti = ""
        mbti += "E" if dimension_scores.get("IE", 0) >= 0 else "I"
        mbti += "N" if dimension_scores.get("SN", 0) >= 0 else "S"
        mbti += "F" if dimension_scores.get("TF", 0) >= 0 else "T"
        mbti += "J" if dimension_scores.get("JP", 0) >= 0 else "P"
        return mbti

    def calculate_riasec(
        self, raw_scores: Dict[str, float]
    ) -> Tuple[str, Dict[str, float]]:
        """
        Вычисляет код Холланда (RIASEC) и нормализованные баллы.

        Parameters:
        -----------
        raw_scores : dict
            Исходные оценки OCEAN для индивида.

        Returns:
        --------
        holland_code : str
            Код Холланда, состоящий из топ-3 типов RIASEC (например, 'SEC').
        normalized_scores : dict
            Нормализованные баллы для каждого типа RIASEC от 0 до 1.
        """
        z_scores = self._standardize_scores(raw_scores)
        riasec_scores = self._calculate_dimension_scores(
            z_scores, self.RIASEC_CORRELATIONS
        )
        normalized_scores = self._normalize_scores(riasec_scores)
        # Сортируем баллы по убыванию
        sorted_types = sorted(
            normalized_scores.items(), key=lambda item: item[1], reverse=True
        )
        # Формируем код Холланда из топ-3 типов
        holland_code = "".join([item[0] for item in sorted_types[:3]])
        return holland_code, normalized_scores


# Пример использования
if __name__ == "__main__":
    # Загрузка данных из CSV файла
    data = pd.read_csv("processed_data/train.csv")  # Замените на путь к вашему файлу

    # Проверка наличия необходимых столбцов в данных
    required_columns = {
        "extraversion",
        "neuroticism",
        "agreeableness",
        "conscientiousness",
        "openness",
    }
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Data must contain the following columns: {required_columns}")

    # Создание экземпляра PersonalityConverter
    converter = PersonalityConverter(data)

    # Пример оценок OCEAN для индивида
    ocean_scores = {
        "extraversion": 0.6448598130841123,
        "neuroticism": 0.59375,
        "agreeableness": 0.6153846153846153,
        "conscientiousness": 0.6407766990291262,
        "openness": 0.5555555555555555,
    }

    # Расчёт типа MBTI и нормализованных баллов
    mbti_type, mbti_scores = converter.calculate_mbti(ocean_scores)
    print(f"Предполагаемый тип MBTI: {mbti_type}")
    print("Нормализованные баллы измерений MBTI:")
    for dim, score in mbti_scores.items():
        print(f"{dim}: {score:.4f}")

    # Расчёт кода Холланда и баллов RIASEC
    holland_code, riasec_scores = converter.calculate_riasec(ocean_scores)
    print(f"\nКод Холланда (RIASEC): {holland_code}")
    print("Нормализованные баллы RIASEC:")
    for r_type, score in riasec_scores.items():
        print(f"{r_type}: {score:.4f}")
