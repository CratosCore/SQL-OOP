from table_io import print_as_table
from data_validator import *
from CSV_loader import *
from db_manager import *
from lab3 import (
    BaseRecord,
    StandardRecord,
    VIPRecord
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
def main():
    logging.info("Запуск обработки данных")
    init_db()
    clear_table()
    headers, raw_lines = read_raw_lines("data.CSV")
    valid_data = []
    errors = 0
    for line in raw_lines:
        record = validate_row_structure(line, headers)
        if not record:
            errors += 1
            continue
        converted_record, error = convert_row_types(record)
        if error:
            errors += 1
            continue
        if not validate_semantic(converted_record):
            errors += 1
            continue
        valid_data.append(converted_record)
    inserted = insert_many_tours(valid_data)
    db_data = get_all_tours()
    objects_list = []

    for row in db_data:
        if row["grade"] == 5:
            obj = VIPRecord.from_db_row(row) #если оцена равна 5, то строка будет VIP
        else:
            obj = StandardRecord.from_db_row(row)
        objects_list.append(obj)

    print_as_table(db_data, headers)

    print("Полиморфизм:")

    for obj in objects_list:
        print(obj.process_info())
    print("Mixing:")
    for obj in objects_list:
        if isinstance(obj, VIPRecord):
            obj.log_action("Проверка VIP объекта")
            print(obj.to_dict())
            break

    analysis = get_analysis_results()
    print("Анализ:")
    print(f"Сдавшие студенты: {analysis.get('passed', 0)}")
    print("Средние оценки:")
    for subject, avg in analysis.get("averages", []):
        print(f"  {subject}: {avg:.2f}")
    if analysis.get("failed"):
        print("Не сдали:", ", ".join(analysis["failed"]))
    else:
        print("Все сдали")
    print(f"Обработано строк: {len(raw_lines)}")
    print(f"Ошибочных строк: {errors}")
    print(f"Сохранено в БД: {inserted}")
    print("VIPRecord:")
    print(VIPRecord.__mro__)

    print(f"Всего создано объектов: {BaseRecord.total_records}")


if __name__ == "__main__":
    main()