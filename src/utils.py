import os
import json
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional

def save_json(data: Dict, filepath: str) -> None:
    """Сохраняет данные в JSON файл"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Данные сохранены в {filepath}")


def load_json(filepath: str) -> Dict:
    """Загружает данные из JSON файла"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_timestamp() -> str:
    """Возвращает текущую метку времени"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


class ProjectLogger:
    """Логгер для проекта"""
    
    def __init__(self, log_file: str = "project.log"):
        self.log_file = log_file
        
    def log(self, message: str, level: str = "INFO"):
        """Записывает сообщение в лог"""
        timestamp = get_timestamp()
        log_message = f"[{timestamp}] [{level}] {message}"
        
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")