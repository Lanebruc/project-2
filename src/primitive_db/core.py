# src/primitive_db/core.py

def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в метаданных.
    
    Args:
        metadata (dict): Текущие метаданные базы данных
        table_name (str): Имя создаваемой таблицы
        columns (list): Список столбцов в формате [("column_name", "type"), ...]
        
    Returns:
        dict: Обновленные метаданные или исходные метаданные в случае ошибки
    """
    # Проверяем, существует ли уже таблица с таким именем
    if "tables" in metadata and table_name in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' уже существует")
        return metadata
    
    # Проверяем корректность типов данных
    allowed_types = {"int", "str", "bool"}
    for column_name, column_type in columns:
        if column_type not in allowed_types:
            error_msg = (
                f"Ошибка: Недопустимый тип '{column_type}' "
                f"для столбца '{column_name}'. "
                f"Допустимые типы: {', '.join(allowed_types)}"
            )
            print(error_msg)
            return metadata
    
    # Добавляем столбец ID:int в начало списка столбцов
    columns_with_id = [("ID", "int")] + columns
    
    # Инициализируем структуру таблицы в метаданных
    if "tables" not in metadata:
        metadata["tables"] = {}
    
    # Создаем запись о таблице
    metadata["tables"][table_name] = {
        "columns": columns_with_id,
        "data": []  # Будущие данные таблицы
    }
    
    print(f"Таблица '{table_name}' успешно создана")
    print(f"Столбцы: {[col[0] for col in columns_with_id]}")
    
    return metadata


def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных.
    
    Args:
        metadata (dict): Текущие метаданные базы данных
        table_name (str): Имя таблицы для удаления
        
    Returns:
        dict: Обновленные метаданные или исходные метаданные в случае ошибки
    """
    # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        print(f"Ошибка: Таблица '{table_name}' не существует")
        return metadata
    
    # Удаляем таблицу из метаданных
    del metadata["tables"][table_name]
    print(f"Таблица '{table_name}' успешно удалена")
    
    # Если таблиц не осталось, удаляем пустой словарь tables
    if not metadata["tables"]:
        del metadata["tables"]
    
    return metadata