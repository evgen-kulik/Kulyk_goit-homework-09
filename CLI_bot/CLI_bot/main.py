import re

information = 'Бот приймає команди:\n' \
              '"add ...". Бот зберігає у пам\'яті новий контакт. Замість ... користувач вводить ім\'я та номер ' \
              'телефону, обов\'язково через пробіл.\n' \
              '"change ..." Бот зберігає в пам\'яті новий номер телефону існуючого контакту. Замість ... користувач ' \
              'вводить ім\'я та номер телефону, обов\'язково через пробіл.\n' \
              '"phone ...." Бот виводить у консоль номер телефону для зазначеного контакту. Замість ... ' \
              'користувач вводить ім\'я контакту, чий номер треба показати.\n' \
              '"show all". Бот виводить всі збереженні контакти з номерами телефонів у консоль.\n' \
              '"good bye", "close", "exit" по будь-якій з цих команд бот завершує свою роботу після того, як виведе ' \
              'у консоль "Good bye!".'


def input_error(func):
    def inner(string):
        text = str
        result = func(string)
        if result == {'command': 'wrong date'}:
            text = "Ви ввели невірні дані. Дані вводяться відповідно до інструкції."
            print(text)
        return result
    return inner


@input_error
def parser_dct(string):
    """Визначає і повертає команду, ім'я та номер телефону, які увів користувач"""

    str_low = string.lower()
    dictionary = {}
    global command, name, tel_number
    lst = str_low.split()
    if str_low == 'show all':
        command = 'show all'
        dictionary['command'] = command
    elif str_low == 'good bye' or str_low == 'close' or str_low == 'exit':
        command = 'exit'
        dictionary['command'] = command
    elif 2 <= len(lst) <= 3:
        if lst[0] == 'add' and len(lst) == 3:
            command = 'add'
            name = lst[1].title()
            tel_number = lst[2]
            dictionary['command'] = command
            dictionary['name'] = name
            dictionary['tel_number'] = tel_number
        elif lst[0] == 'change' and len(lst) == 3:
            command = 'change'
            name = lst[1].title()
            tel_number = lst[2]
            dictionary['command'] = command
            dictionary['name'] = name
            dictionary['tel_number'] = tel_number
        elif lst[0] == 'phone' and len(lst) == 2:
            command = 'phone'
            name = lst[1].title()
            dictionary['command'] = command
            dictionary['name'] = name
        else:
            command = 'wrong date'
            dictionary['command'] = command
    else:
        command = 'wrong date'
        dictionary['command'] = command
    return dictionary


def add_new_contact(dct):
    """Додає новий контакт у файл telephone_numbers.txt"""

    with open('telephone_numbers.txt', 'a') as fh:
        fh.write(dct['name'] + ': ' + dct['tel_number'] + '\n')


def change_contact(dct):
    """Змінює існуючий контакт у файлі telephone_numbers.txt"""

    with open('telephone_numbers.txt', 'r') as fh:
        lines = fh.readlines()
    counter = 0
    for i in lines:
        name = re.findall(r"[A-Za-z]+", i)
        if dct['name'] == name[0]:
            counter += 1
            lines.remove(i)
            lines.append(dct['name'] + ': ' + dct['tel_number'] + '\n')
            with open('telephone_numbers.txt', 'w') as fh:
                fh.write(''.join(lines))
    if counter != 0:
        return 'Зміни успішно внесено.'
    else:
        return 'Такого імені нема в телефонній книзі.'

def phone_by_name(dct):
    """Повертає телефон з файлу telephone_numbers.txt для введеного імені"""

    with open('telephone_numbers.txt', 'r') as fh:
        lines = fh.readlines()
    dct_n_ph = {}
    for i in lines:
        name = re.findall(r"[A-Za-z]+", i)
        telephone_number = re.findall(r"[+]?\d{1,12}", i)
        if len(name) > 0 and len(telephone_number) > 0:
            dct_n_ph[name[0]] = telephone_number[0]
    if dct['name'] in dct_n_ph:
        tel_n = dct_n_ph[dct['name']]
        return f'Телефонний номер для цього імені {tel_n}'
    else:
        return "Введене ім'я відсутнє у телефонній книзі."


def show_all_contacts():
    """Повертає список імен з номерами телефонів з файлу telephone_numbers.txt"""

    with open('telephone_numbers.txt', 'r') as fh:
        lines = fh.readlines()
    return lines


def main():
    """ Опрацьовує команду користувача з телефонною книгою"""

    print(information)
    while True:
        string = input("Як я можу вам допомогти?\n")
        dct = parser_dct(string)
        command = dct['command']
        while True:
            if command == 'wrong date':
                string = input("Введіть коректні дані: \n")
                dct = parser_dct(string)
                command = dct['command']
            else:
                break
        if command == 'add':
            add_new_contact(dct)
            print("Дані успішно додано!")
        elif command == 'change':
            change_contact(dct)
            print(change_contact(dct))
        elif command == 'phone':
            result = phone_by_name(dct)
            print(result)
        elif command == 'show all':
            result = show_all_contacts()
            print('Повна телефонна книга:')
            for i in result:
                print(i, end='')
        elif command == 'exit':
            print("Good bye!")
            break


if __name__ == '__main__':
    main()