import csv
import os

FILE_NAME = 'data_file.csv'
LIST_FIELD_NAMES = ["num_row", "last_name", "first_name", "patronymic", "name_org", "phone_work", "phone_personal"]


def print_menu() -> str:
    """Вывод меню на экран"""

    print("""Меню программы:
            1 - Вывод постранично записей из справочника на экран
            2 - Добавление новой записи в справочник
            3 - Редактирование записей в справочнике
            4 - Поиск записей по одной или нескольким характеристикам 
            0 - Выход            
-------------------------------------------------------------------------------            
            """)


def get_num(mess) -> int:
    """Считать номер страницы/строки с экрана"""

    while True:
        try:
            n = int(input(mess))
            return n
        except ValueError as e:
            print(e)


def save_to_file(data):
    """Запись данных в файл"""

    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w', newline='', encoding='utf-8') as write_file:
                writer = csv.DictWriter(write_file,
                                        fieldnames=data.keys(),
                                        dialect='excel', )
                writer.writeheader()

        with open(FILE_NAME, 'r+', newline='', encoding='utf-8') as write_file:
            count_row = sum(1 for _ in write_file)
            data['num_row'] = (count_row if count_row > 0 else count_row + 1)

            writer = csv.DictWriter(write_file,
                                    fieldnames=data.keys(),
                                    dialect='excel',
                                    quoting=csv.QUOTE_NONNUMERIC,
                                    delimiter=",",
                                    )

            if count_row == 0:
                writer.writeheader()
            writer.writerow(data)
    except TypeError as e:
        print(e)


def add_data():
    """Добавление записи в справочник"""

    last_name = input('>Введите фамилию: ').strip()
    first_name = input('>Введите имя: ').strip()
    patronymic = input('>Введите отчество: ').strip()
    name_org = input('>Введите название организации: ').strip()
    phone_work = input('>Введите телефон рабочий: ').strip()
    phone_personal = input('>Введите телефон личный (сотовый): ').strip()

    data = {
        'num_row': 0,
        'last_name': last_name,
        'first_name': first_name,
        'patronymic': patronymic,
        'name_org': name_org,
        'phone_work': phone_work,
        'phone_personal': phone_personal,
    }

    save_to_file(data)


def get_data(i_begin, i_end):
    """Получить и вывести на экран записи из справочника по заданному диапазону"""

    try:
        # прочитать
        with open(FILE_NAME, 'r', encoding='utf-8') as read_file:
            list_spr = []
            reader = csv.DictReader(read_file, delimiter=",")
            for row in reader:
                list_spr.append(row)

            str_header = ''
            for el in reader.fieldnames:
                str_header += el.upper() + ' '

        # вывести на экран
        print(str_header)
        for row in list_spr[i_begin:i_end]:
            str_row = ' '.join(list(row.values()))

            print(str_row)
    except FileNotFoundError:
        print(f'Файл {FILE_NAME} не найден')
    except KeyError as e:
        print(f'Ошибка {e}')
    except Exception as e:
        print(e)


def read_data():
    """Вывод записей из справочник по определенной странице"""

    num_page = get_num('Введите номер страницы: ')
    count_row = 4  # количество записей на странице

    # вычислить диапаон записей
    i_begin = (num_page - 1) * count_row
    i_end = num_page * count_row

    get_data(i_begin, i_end)


def update_data():
    """Редактирование записи в справочнике"""

    num_row = get_num('Введите номер строки для редактирования: ')

    # ---- CSV ----
    try:
        # 1
        # спросить что менять
        str_field_names = ', '.join(LIST_FIELD_NAMES[1:])

        print(f'Доступные поля для для редактирования: {str_field_names}')

        field_user = input('Введите поля для редактирования через пробел: ').strip()
        list_field_user = field_user.split(' ')

        # проверить что ввели корректные названия полей
        for field_user in list_field_user:
            if field_user not in LIST_FIELD_NAMES:
                raise ValueError(f'Введено некоректное название поля {field_user}')

        # ввести новые данные для замены
        data_upd = {}
        for field in list_field_user:
            data_upd[field] = input(f'{field}: ').strip()

        # 2 прочитать файл
        list_spr = []
        with open(FILE_NAME, 'r', encoding='utf-8') as read_file:
            reader = csv.DictReader(read_file, delimiter=",")
            for row in reader:
                list_spr.append(row)

        # 3 заменить данные
        for dict_data in list_spr:
            if int(dict_data['num_row']) == num_row:
                dict_data.update(data_upd)
                break
        else:
            raise ValueError('Не найден номер строки!')

        # 4 перезаписать данные в файл
        with open(FILE_NAME, 'w', newline='', encoding='utf-8') as write_file:
            writer = csv.DictWriter(write_file,
                                    fieldnames=LIST_FIELD_NAMES,
                                    dialect='excel',
                                    quoting=csv.QUOTE_NONNUMERIC,
                                    )

            writer.writeheader()
            for row in list_spr:
                writer.writerow(row)

        # 5 сообщить об успехе
        print('Данные успешно обновлены')
    except FileNotFoundError:
        print(f'Файл {FILE_NAME} не найден')
    except KeyError as e:
        print(f'Ошибка! {e}')
    except ValueError as e:
        print(f'Ошибка! {e}')
    except TypeError as e:
        print(e)


def search_data():
    """Поиск записей в справочнике по определенным полям"""

    # прочитать
    try:
        # 1 спросить что ищем
        str_field_names = ', '.join(LIST_FIELD_NAMES)
        print(f'Поля для поиска: {str_field_names}')

        field_user = input('Введите поля для поиска через пробел: ')
        list_field_user = field_user.strip().split(' ')

        # проверить что ввели корректные названия полей
        for field_user in list_field_user:
            if field_user not in LIST_FIELD_NAMES:
                raise ValueError(f'Введено некоректное название поля {field_user}')

        # ввести данные для поиска
        dict_field = {}
        for field in list_field_user:
            dict_field[field] = input(f'{field}: ')

        # 2 прочитать
        list_spr = []
        with open(FILE_NAME, 'r', encoding='utf-8') as read_file:
            reader = csv.DictReader(read_file, delimiter=",")
            for row in reader:
                list_spr.append(row)

        # 3 поиск
        list_search = []
        for row in list_spr:
            is_search = False
            for field in list_field_user:
                if row[field] == dict_field[field]:
                    is_search = True
                else:
                    is_search = False
                    break

            if is_search:
                list_search.append(row)

        # 4 отобразить результат поиска
        if not list_search:
            print('Нет данных')
        else:
            print(str_field_names)
            for row in list_search:
                print(' '.join(list(row.values())))
    except FileNotFoundError:
        print(f'Файл {FILE_NAME} не найден')
    except KeyError as e:
        print(f'Ошибка! {e}')
    except ValueError as e:
        print(f'Ошибка! {e}')
    except TypeError as e:
        print(e)


# ===========================================
if __name__ == '__main__':
    print_menu()

    while True:
        try:
            par = int(input('===>Выберите пункт меню: '))

            if par not in range(0, 5):
                raise ValueError('Значение не входит в список допустимых занчений')
        except ValueError:
            print('Ошибка! Неверное значение меню')
            continue

        if par == 0:
            print('Выход...')
            break
        elif par == 1:
            print('Вывод постранично записей из справочника на экран')
            read_data()
        elif par == 2:
            print('Добавление новой записи в справочник')
            add_data()
        elif par == 3:
            print('Редактирование записей в справочнике')
            update_data()
        elif par == 4:
            print('Поиск записей по одной или нескольким характеристикам')
            search_data()
