"""
ПРИМЕР КОДА ДЛЯ ОБРАБОТКИ ДАННЫХ ПРОЕКТОВ БЛАГОУСТРОЙСТВА

ВАЖНО: Это демонстрационный код, показывающий логику работы с данными.
На реальных данных потребуется:
1. Адаптация под конкретные форматы файлов
2. Обработка ошибок и исключений
3. Интеграция с базой данных
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class ConstructionWork:
    """Класс для представления строительной работы"""
    name: str
    unit: str  # единица измерения (м2, шт, м3)
    amount: float  # объём работы
    man_hours_per_unit: float  # трудозатраты на единицу (чел-ч)
    dependencies: List[str]  # зависимости от других работ
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectAnalyzer:
    """Анализатор проекта благоустройства"""
    
    def __init__(self, workers_count: int = 2, workday_hours: int = 8):
        self.workers_count = workers_count
        self.workday_hours = workday_hours
        
    def calculate_duration(self, work: ConstructionWork) -> float:
        """Рассчитывает длительность работы в днях"""
        total_hours = work.man_hours_per_unit * work.amount
        return total_hours / (self.workday_hours * self.workers_count)
    
    def extract_from_estimate(self, estimate_data: Dict) -> List[ConstructionWork]:
        """
        Извлекает данные о работах из сметы
        В реальности эта функция будет парсить Excel/PDF файлы
        """
        works = []
        
        # Пример данных (в реальности извлекаются из файлов)
        sample_data = [
            {"name": "Устройство асфальтового покрытия", "unit": "м2", "amount": 500, "man_hours": 2.4, "deps": []},
            {"name": "Установка скамеек", "unit": "шт", "amount": 15, "man_hours": 20, "deps": ["Подготовка территории"]},
            {"name": "Посадка деревьев", "unit": "шт", "amount": 30, "man_hours": 8, "deps": ["Устройство покрытия"]},
            {"name": "Монтаж освещения", "unit": "шт", "amount": 20, "man_hours": 12, "deps": ["Устройство покрытия"]},
        ]
        
        for item in sample_data:
            work = ConstructionWork(
                name=item["name"],
                unit=item["unit"],
                amount=item["amount"],
                man_hours_per_unit=item["man_hours"],
                dependencies=item["deps"]
            )
            works.append(work)
            
        return works
    
    def create_gantt_chart(self, works: List[ConstructionWork], start_date: datetime) -> pd.DataFrame:
        """
        Создаёт таблицу диаграммы Ганта на основе рассчитанных длительностей
        Алгоритм:
        1. Рассчитать длительность каждой работы
        2. Учесть зависимости между работами
        3. Определить даты начала и окончания
        """
        
        # Рассчитываем длительности
        for work in works:
            work_duration = self.calculate_duration(work)
            work.start_date = start_date
            work.end_date = start_date + timedelta(days=work_duration)
            
            # Простая логика учёта зависимостей (в реальности сложнее)
            if work.dependencies:
                # Находим последнюю дату окончания зависимых работ
                max_end_date = start_date
                for dep_name in work.dependencies:
                    for dep_work in works:
                        if dep_work.name == dep_name and dep_work.end_date:
                            max_end_date = max(max_end_date, dep_work.end_date)
                
                work.start_date = max_end_date
                work.end_date = max_end_date + timedelta(days=work_duration)
        
        # Формируем DataFrame для наглядности
        gantt_data = []
        for work in works:
            gantt_data.append({
                "Работа": work.name,
                "Объём": f"{work.amount} {work.unit}",
                "Трудозатраты (чел-ч)": work.man_hours_per_unit * work.amount,
                "Длительность (дней)": round((work.end_date - work.start_date).days, 1),
                "Начало": work.start_date.strftime("%d.%m.%Y"),
                "Окончание": work.end_date.strftime("%d.%m.%Y"),
                "Зависимости": ", ".join(work.dependencies) if work.dependencies else "Нет"
            })
        
        return pd.DataFrame(gantt_data)
    
    def analyze_project_completeness(self, files_info: Dict[str, bool]) -> Dict:
        """
        Анализирует комплектность документов проекта
        Оценивает, каких данных не хватает для полного анализа
        """
        completeness_score = 0
        max_score = 4
        missing_docs = []
        
        # Критерии оценки
        criteria = {
            "has_technical_task": ("Техническое задание", 1),
            "has_estimate": ("Смета с трудозатратами", 2),
            "has_schedule": ("График работ", 1),
            "has_visual_plans": ("Визуальные планы", 0.5)
        }
        
        for criterion, (doc_name, weight) in criteria.items():
            if files_info.get(criterion, False):
                completeness_score += weight
            else:
                missing_docs.append(doc_name)
        
        return {
            "completeness_percent": (completeness_score / max_score) * 100,
            "missing_documents": missing_docs,
            "recommendations": self._generate_recommendations(missing_docs)
        }
    
    def _generate_recommendations(self, missing_docs: List[str]) -> List[str]:
        """Генерирует рекомендации по недостающим документам"""
        recommendations = []
        
        if "Техническое задание" in missing_docs:
            recommendations.append("Запросить ТЗ у заказчика или найти аналогичный проект")
        
        if "Смета с трудозатратами" in missing_docs:
            recommendations.append("Использовать средние трудозатраты по аналогичным работам")
            
        if "График работ" in missing_docs:
            recommendations.append("Восстановить график из сметы через расчёт трудозатрат")
            
        return recommendations

def demonstrate_workflow():
    """Демонстрация полного workflow обработки проекта"""
    
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ОБРАБОТКИ ПРОЕКТА БЛАГОУСТРОЙСТВА ДЛЯ СИСТЕМЫ 'ТОР'")
    print("=" * 70)
    
    # 1. Инициализация анализатора
    analyzer = ProjectAnalyzer(workers_count=2, workday_hours=8)
    
    # 2. Анализ комплектности документов
    print("\n1. АНАЛИЗ КОМПЛЕКТНОСТИ ДОКУМЕНТОВ:")
    project_files = {
        "has_technical_task": True,
        "has_estimate": True,
        "has_schedule": False,  # Графика нет - будем восстанавливать
        "has_visual_plans": False
    }
    
    completeness = analyzer.analyze_project_completeness(project_files)
    print(f"   Полнота данных: {completeness['completeness_percent']:.1f}%")
    print(f"   Отсутствуют: {', '.join(completeness['missing_documents'])}")
    print("   Рекомендации:")
    for rec in completeness['recommendations']:
        print(f"     - {rec}")
    
    # 3. Извлечение данных из сметы
    print("\n2. ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ СМЕТЫ:")
    works = analyzer.extract_from_estimate({})
    print(f"   Найдено работ: {len(works)}")
    for work in works:
        print(f"     - {work.name}: {work.amount} {work.unit}")
    
    # 4. Создание диаграммы Ганта
    print("\n3. СОЗДАНИЕ ДИАГРАММЫ ГАНТА ИЗ ТРУДОЗАТРАТ:")
    start_date = datetime(2024, 6, 1)
    gantt_df = analyzer.create_gantt_chart(works, start_date)
    
    print("\n   Результирующий график работ:")
    print("   " + "-" * 60)
    for _, row in gantt_df.iterrows():
        duration_bar = "█" * int(row["Длительность (дней)"] / 2)  # Визуализация
        print(f"   {row['Работа'][:20]:20} | {row['Начало']} - {row['Окончание']} | {duration_bar}")
    
    # 5. Анализ результатов
    print("\n4. АНАЛИТИКА ПРОЕКТА:")
    total_duration = gantt_df["Длительность (дней)"].sum()
    total_man_hours = gantt_df["Трудозатраты (чел-ч)"].sum()
    
    print(f"   Общая длительность проекта: {total_duration:.1f} дней")
    print(f"   Общие трудозатраты: {total_man_hours:.0f} чел-ч")
    print(f"   Количество работ: {len(works)}")
    
    # 6. Определение критического пути (упрощённо)
    print("\n5. ОПРЕДЕЛЕНИЕ КРИТИЧЕСКОГО ПУТИ:")
    
    # Работы без зависимостей или с минимальным запасом времени
    critical_works = [w for w in works if not w.dependencies]
    if critical_works:
        print("   Критические работы (определяют общий срок):")
        for work in critical_works[:3]:  # Показываем первые 3
            print(f"     - {work.name}")
    else:
        print("   Все работы имеют зависимости - требуется сложный анализ")
    
    print("\n" + "=" * 70)
    print("ВОЗМОЖНОСТИ ДЛЯ ИНТЕГРАЦИИ С СИСТЕМОЙ 'ТОР':")
    print("-" * 70)
    
    ml_cv_applications = [
        ("Прогнозирование сроков", "ML", "На основе исторических данных похожих проектов"),
        ("Оптимизация последовательности", "ML", "Генетические алгоритмы, RL"),
        ("Контроль соответствия планам", "CV", "Сравнение фото с чертежами"),
        ("Автоматический учёт работ", "CV+NLP", "Распознавание накладных, актов"),
        ("Мониторинг прогресса", "CV", "Анализ фото/видео с дронов, камер")
    ]
    
    for app_name, tech, description in ml_cv_applications:
        print(f"  {app_name:30} [{tech:4}] {description}")

def data_structure_example():
    """Пример структуры данных для хранения информации о проектах"""
    
    print("\n" + "=" * 70)
    print("ПРЕДЛАГАЕМАЯ СТРУКТУРА БАЗЫ ДАННЫХ ДЛЯ СИСТЕМЫ 'ТОР':")
    print("=" * 70)
    
    structure = {
        "projects": {
            "fields": ["id", "name", "location", "type", "start_date", "end_date", "status"],
            "example": {
                "id": "PROJ-2024-001",
                "name": "Благоустройство площади",
                "location": "Тюмень",
                "type": "городская_площадь",
                "status": "в_планировании"
            }
        },
        "documents": {
            "fields": ["id", "project_id", "doc_type", "format", "url", "parsed_status"],
            "doc_types": ["техническое_задание", "смета", "график_работ", "ситуационный_план", "чертежи"]
        },
        "works": {
            "fields": ["id", "project_id", "name", "category", "amount", "unit", "man_hours"],
            "categories": ["земляные", "дорожные", "озеленение", "маф", "освещение"]
        },
        "ml_models": {
            "fields": ["model_id", "purpose", "accuracy", "last_trained"],
            "purposes": ["сроки_прогноз", "стоимость_прогноз", "оптимизация_графика", "cv_детекция"]
        }
    }
    
    for table_name, table_info in structure.items():
        print(f"\n📊 {table_name.upper()}:")
        if "fields" in table_info:
            print(f"   Поля: {', '.join(table_info['fields'])}")
        if "example" in table_info:
            print(f"   Пример: {table_info['example']}")
    
    print("\n" + "=" * 70)
    print("СЛЕДУЮЩИЕ ШАГИ РАЗРАБОТКИ:")
    print("-" * 70)
    
    next_steps = [
        ("Парсинг PDF/Excel", "Извлечение структурированных данных из сканов"),
        ("Разметка данных", "Аннотация для обучения ML/CV моделей"),
        ("ML: Модель прогнозирования", "Gradient Boosting для сроков и стоимости"),
        ("CV: Детекция на планах", "YOLO/CNN для объектов благоустройства"),
        ("Интеграция", "REST API для доступа к моделям из основной системы")
    ]
    
    for i, (step, description) in enumerate(next_steps, 1):
        print(f"{i:2}. {step:30} - {description}")

if __name__ == "__main__":
    # Демонстрация всех возможностей
    demonstrate_workflow()
    data_structure_example()
    
    print("\n" + "=" * 70)
    print("ВАЖНОЕ ПРИМЕЧАНИЕ:")
    print("-" * 70)
    print("""
Данный код - КОНЦЕПТУАЛЬНАЯ ДЕМОНСТРАЦИЯ логики работы с данными.
    
Для реальной системы потребуется:
1. Разработка парсеров под конкретные форматы документов
2. Создание ML-моделей на реальных данных
3. Разработка CV-моделей для анализа визуальной информации
4. Интеграция с внешними системами (госзакупки, GIS, камеры)
5. Масштабируемая архитектура и API
""")