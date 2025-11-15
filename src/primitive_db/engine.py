# src/primitive_db/engine.py
import shlex

from .core import create_table, drop_table
from .utils import load_metadata, save_metadata


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def list_tables(metadata):
    """Показывает список всех таблиц."""
    if "tables" not in metadata or not metadata["tables"]:
        print("Таблицы не найдены")
        return
    
    print("\nСписок таблиц:")
    for table_name, table_info in metadata["tables"].items():
        columns = [f"{col[0]}:{col[1]}" for col in table_info["columns"]]
        print(f"  {table_name}: {', '.join(columns)}")


def run():
    """Главная функция с основным циклом программы."""
    print("Добро пожаловать в примитивную базу данных!")
    print_help()
    
    while True:
        # Загружаем актуальные метаданные
        metadata = load_metadata("database.json")
        
        try:
            # Запрашиваем ввод у пользователя
            user_input = input("Введите команду: ").strip()
            
            # Разбираем введенную строку на команду и аргументы
            args = shlex.split(user_input)
            if not args:
                continue
                
            command = args[0].lower()
            
            # Обрабатываем команды
            if command == "exit":
                print("Выход из программы...")
                break
                
            elif command == "help":
                print_help()
                
            elif command == "create_table":
                if len(args) < 3:
                    print(
                        "Ошибка: Используйте: create_table <имя_таблицы> "
                        "<столбец1:тип> [столбец2:тип ...]"
                    )
                    continue
                
                table_name = args[1]
                columns = []
                
                for col_arg in args[2:]:
                    if ":" not in col_arg:
                        print(
                            f"Ошибка: Неверный формат столбца '{col_arg}'. "
                            "Используйте: имя:тип"
                        )
                        break
                    col_name, col_type = col_arg.split(":", 1)
                    columns.append((col_name.strip(), col_type.strip().lower()))
                else:
                    # Все столбцы успешно разобраны
                    metadata = create_table(metadata, table_name, columns)
                    save_metadata("database.json", metadata)
                    
            elif command == "list_tables":
                list_tables(metadata)
                
            elif command == "drop_table":
                if len(args) < 2:
                    print("Ошибка: Используйте: drop_table <имя_таблицы>")
                    continue
                
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata("database.json", metadata)
                
            else:
                print(f"Неизвестная команда: {command}")
                print("Введите 'help' для справки")
                
        except KeyboardInterrupt:
            print("\nВыход из программы...")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")