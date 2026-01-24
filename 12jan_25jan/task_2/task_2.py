from pathlib import Path
from collections import defaultdict


FILE_PATH = Path(__file__).parent / "access.log"


def reading_loog(filename):
    method_count = {
        "GET": 0,
        "POST": 0,
        "PUT": 0,
        "DELETE": 0,
        "PATCH": 0,
        "HEAD": 0,
        "OPTIONS": 0,
        "CONNECT": 0,
        "TRACE": 0,
    }  # Да знаю, много, но что поделать
    ip_adress = defaultdict(int)
    responce_time = []
    errors_codes = defaultdict(int)

    with open(
        filename, "r", encoding="utf-8"
    ) as file:  # TODO Написать коменты к каждой строчке
        for method in file.readlines():
            m = method.split()
            method_count[m[4].replace('"', "")] += 1
            ip_adress[m[0]] += 1
            if m[7].startswith(("4", "5")):
                errors_codes[m[7]] += 1
            responce_time.append(int(m[8]))

    sorted_ip_adress = sorted(
        ip_adress.items(), key=lambda x: x[1], reverse=True
    )  #  * Отортировал по убыванию и буду брать только первые 10
    top_ip_adress = "\n\t".join(
        [f"ip {key}: кол-во раз {value}" for key, value in sorted_ip_adress[:10]]
    )

    if len(responce_time) == 0:  # Если список пустой, будет ошибка
        raise ZeroDivisionError("Список пустой, на ноль делить нельзя")
    else:
        average_responce_time = sum(responce_time) / len(responce_time)

    final_method_count = "\n\t".join(
        [f"{key}: {value}" for key, value in method_count.items()]
    )
    final_errors_code = "\n\t".join(
        [
            f"статус {key}: количество ошибок {value}"
            for key, value in errors_codes.items()
        ]
    )

    return f"""
    Количество запросов:\n\t{final_method_count}\n
    ТОП IP-адресов:\n\t{top_ip_adress}\n
    Список ошибок:\n\t{final_errors_code}\n
    Среднее время ответа = {average_responce_time}\n
    """


print(reading_loog(FILE_PATH))
