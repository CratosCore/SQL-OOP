from abc import ABC, abstractmethod


class BaseRecord(ABC):
    total_records = 0

    def __init__(self, record_id, student_id, name, group_name, subject, grade, exam_date, status):
        # приватный атрибут с __
        self.__id = record_id
        # защищённые атрибуты с _
        self._name = name
        self._status = status
        self._grade = grade

        self.student_id = student_id
        self.group_name = group_name
        self.subject = subject
        self.exam_date = exam_date
        BaseRecord.total_records += 1

    # геттеры, безопасное обращение к строкам

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def grade(self):
        return self._grade

    # фабричный метод - создает объекты из строк БД

    @classmethod
    def from_db_row(cls, db_row):
        return cls(
            db_row["id"],
            db_row["student_id"],
            db_row["name"],
            db_row["group_name"],
            db_row["subject"],
            db_row["grade"],
            db_row["exam_date"],
            db_row["status"]
        )

    # абстрактный метод

    @abstractmethod
    def process_info(self):
        pass


# стандартная запись, полиморфизм

class StandardRecord(BaseRecord):

    def process_info(self):
        return (
            f"Студент: {self.name} "
            f"Предмет: {self.subject} "
            f"Оценка: {self.grade} "
            f"Статус: {self.status} "
        )


# специальная запись
class SpecialRecord(BaseRecord):

    def process_info(self):
        return (
            f"ВНИМАНИЕ!!! "
            f"{self.name.upper()} "
            f"{self.subject.upper()} "
            f"ОЦЕНКА: {self.grade} "
            f"СТАТУС: {self.status.upper()} "
        )


# Mixins

class LogMixin:

    def log_action(self, action):
        print(f"[LOG] {self.name}: {action}")


class ExportMixin:

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "group_name": self.group_name,
            "subject": self.subject,
            "grade": self.grade,
            "exam_date": self.exam_date,
            "status": self.status
        }


# VIP запись


class VIPRecord(
    SpecialRecord,
    LogMixin,
    ExportMixin
):
    pass
