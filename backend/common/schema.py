from pydantic import BaseModel, ConfigDict, EmailStr, validate_email
from typing import Generic, Optional, TypeVar

CUSTOM_VALIDATION_ERROR_MESSAGES = {
    "arguments_type": "Ошибка при вводе типа параметра",
    "assertion_error": "Ошибка выполнения утверждения",
    "bool_parsing": "Ошибка анализа логического ввода",
    "bool_type": "Неправильный ввод логического типа значения",
    "bytes_too_long": "Слишком большая длина входного сигнала в байтах",
    "bytes_too_short": "Слишком короткая длина входного сигнала в байтах",
    "bytes_type": "Ошибка при вводе типа байта",
    "callable_type": "Ошибка ввода вызываемого типа объекта",
    "dataclass_exact_type": "Ошибка ввода типа экземпляра класса данных",
    "dataclass_type": "Ошибка ввода типа класса данных",
    "date_from_datetime_inexact": "Вход компонента даты отличен от нуля",
    "date_from_datetime_parsing": "Ошибка синтаксического анализа ввода даты",
    "date_future": "Дата вводится не в будущем времени",
    "date_parsing": "Ошибка проверки ввода даты",
    "date_past": "Дата вводится не в прошедшем времени",
    "date_type": "Ошибка при вводе типа даты",
    "datetime_future": "Дата и время указывают время, не относящееся к будущему",
    "datetime_object_invalid": "Недопустимый объект ввода даты и времени",
    "datetime_parsing": "Ошибка при разборе ввода даты и времени",
    "datetime_past": "Дата и время вводят не прошедшее время",
    "datetime_type": "Ошибка при вводе типа даты и времени",
    "decimal_max_digits": "Введено слишком много знаков после запятой",
    "decimal_max_places": "Неправильный ввод десятичных разрядов",
    "decimal_parsing": "Ошибка синтаксического анализа десятичных входных данных",
    "decimal_type": "Ошибка при вводе десятичного типа",
    "decimal_whole_digits": "Неправильный ввод десятичных разрядов",
    "dict_type": "Ошибка при вводе типа словаря",
    "enum": "Ошибка ввода элемента перечисления, допускающая {expected}",
    "extra_forbidden": "Запретить ввод дополнительных полей",
    "finite_number": "Ошибка ввода конечного значения",
    "float_parsing": "Ошибка синтаксического анализа входных данных с плавающей запятой",
    "float_type": "Ошибка при вводе типа числа с плавающей запятой",
    "frozen_field": "Ошибка при вводе в frozenset",
    "frozen_instance": "Заморозьте экземпляр и запретите внесение изменений",
    "frozen_set_type": "Тип frozenset запрещает ввод данных",
    "get_attribute_error": "Ошибка получения атрибута",
    "greater_than": "Входное значение слишком велико",
    "greater_than_equal": "Входное значение слишком велико или равно",
    "int_from_float": "Ошибка ввода целочисленного типа",
    "int_parsing": "Ошибка синтаксического анализа целочисленных входных данных",
    "int_parsing_size": "Ошибка при анализе длины входного целого числа",
    "int_type": "Ошибка при анализе длины входного целого числа",
    "invalid_key": "Неверное значение ключа",
    "is_instance_of": "Ошибка ввода экземпляра типа",
    "is_subclass_of": "Ошибка ввода подклассов типов",
    "iterable_type": "Повторяющаяся ошибка ввода типа",
    "iteration_error": "Ошибка при вводе значения итерации",
    "json_invalid": "JSON Ошибка при вводе строки",
    "json_type": "JSON Ошибка ввода типа",
    "less_than": "Входное значение слишком мало",
    "less_than_equal": "Входное значение слишком мало или равно",
    "list_type": "Ошибка ввода типа списка",
    "literal_error": "Ошибка буквального ввода",
    "mapping_type": "Ошибка ввода типа отображения",
    "missing": "Отсутствуют обязательные поля",
    "missing_argument": "Отсутствующие параметры",
    "missing_keyword_only_argument": "Отсутствующий параметр ключевого слова",
    "missing_positional_only_argument": "Отсутствующие позиционные параметры",
    "model_attributes_type": "Ошибка при вводе типа атрибута модели",
    "model_type": "Ошибка ввода экземпляра модели",
    "multiple_argument_values": "Введено слишком много значений параметров",
    "multiple_of": "Входное значение не является кратным",
    "no_such_attribute": "Присвоение недопустимого значения атрибута",
    "none_required": "Входное значение должно быть None",
    "recursion_loop": "Назначение входного контура",
    "set_type": "Ошибка при вводе типа коллекции",
    "string_pattern_mismatch": "Несоответствие введенного шаблона ограничения строки",
    "string_sub_type": "Ошибка ввода строкового подтипа (нестрогий экземпляр)",
    "string_too_long": "Строка слишком длинная",
    "string_too_short": "Строка слишком короткая",
    "string_type": "Ошибка при вводе строкового типа",
    "string_unicode": "字符串输入非 Unicode",
    "time_delta_parsing": "Ошибка синтаксического анализа ввода с разницей во времени",
    "time_delta_type": "Ошибка ввода типа разницы во времени",
    "time_parsing": "Ошибка синтаксического анализа ввода времени",
    "time_type": "Ошибка ввода типа времени",
    "timezone_aware": "Отсутствующая входная информация о часовом поясе",
    "timezone_naive": "Запретить ввод информации о часовом поясе",
    "too_long": "Ввод слишком длинный",
    "too_short": "Ввод слишком короткий",
    "tuple_type": "Ошибка при вводе типа кортежа",
    "unexpected_keyword_argument": "Неожиданные параметры ключевого слова",
    "unexpected_positional_argument": "Неожиданный позиционный аргумент",
    "union_tag_invalid": "Ошибка при вводе литерала типа union",
    "union_tag_not_found": "Входной параметр типа union не найден",
    "url_parsing": "URL Ошибка синтаксического анализа входных данных",
    "url_scheme": "URL Ошибка схемы ввода",
    "url_syntax_violation": "URL Синтаксическая ошибка ввода",
    "url_too_long": "URL Ввод слишком длинный",
    "url_type": "URL Ошибка ввода типа",
    "uuid_parsing": "UUID Ошибка синтаксического анализа входных данных",
    "uuid_type": "UUID Ошибка ввода типа",
    "uuid_version": "UUID Ошибка ввода типа версии",
    "value_error": "Ошибка при вводе значения",
}

CUSTOM_USAGE_ERROR_MESSAGES = {
    "class-not-fully-defined": "Тип атрибута класса определен не полностью",
    "custom-json-schema": "__modify_schema__ Этот метод устарел в версии V2",
    "decorator-missing-field": "Определен недопустимый валидатор полей",
    "discriminator-no-field": "Не все поля дискриминатора определены",
    "discriminator-alias-type": "Поля дискриминатора определяются с использованием нестроковых типов",
    "discriminator-needs-literal": "Поле дискриминатора должно быть определено с использованием буквального значения",
    "discriminator-alias": "Несогласованное определение псевдонимов полей дискриминатора",
    "discriminator-validator": "Поле дискриминатор запрещает определение поля валидатор",
    "model-field-overridden": "Ни одно поле определения типа не запрещает повторную запись",
    "model-field-missing-annotation": "Отсутствует определение типа поля",
    "config-both": "Повторное определение элементов конфигурации",
    "removed-kwargs": "Вызовите параметр конфигурации удаленного ключевого слова",
    "invalid-for-json-schema": "Существует недопустимый тип JSON",
    "base-model-instantiated": "Запретить создание экземпляров базовых моделей",
    "undefined-annotation": "Отсутствие определения типа",
    "schema-for-unknown-type": "Определение неизвестного типа",
    "create-model-field-definitions": "Ошибка определения поля",
    "create-model-config-base": "Ошибка в определении элемента конфигурации",
    "validator-no-fields": "Средство проверки полей не указывает поле",
    "validator-invalid-fields": "Ошибка определения поля валидатором поля",
    "validator-instance-method": "Средство проверки поля должно быть методом класса",
    "model-serializer-instance-method": "Сериализатор должен быть методом экземпляра",
    "validator-v1-signature": "Ошибка средства проверки полей версии V1 устарела",
    "validator-signature": "Ошибка подписи средства проверки полей",
    "field-serializer-signature": "Подпись сериализатора полей не распознается",
    "model-serializer-signature": "Сигнатура сериализатора модели не распознается",
    "multiple-field-serializers": "Сериализатор полей повторяет определение",
    "invalid_annotated_type": "Недопустимое определение типа",
    "type-adapter-config-unused": "Ошибка в определении элемента конфигурации адаптера типа",
    "root-model-extra": "Корневая модель запрещает определение дополнительных полей",
}


class CustomEmailStr(EmailStr):
    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return None if __input_value == "" else validate_email(__input_value)[1]


class SchemaBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)


class Links(BaseModel):
    first: str
    last: Optional[str] = None
    self: str
    next: Optional[str] = None
    prev: Optional[str] = None


T = TypeVar("T")


class PaginatedData(SchemaBase, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
    links: Links
