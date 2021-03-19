"""
Какова сложность вашего алгоритма?

Предположу, что array.index('0') использует линейный поиск, т.е. O (n).
Аналогично '0 in array', только вместо возврата булева значения возвращаю индекс '0'.

(c) https://wiki.python.org/moin/TimeComplexity
"""


def task(array: str) -> str:
    """Функция возвращает индекс последней '1' и первого '0' в строке."""
    if '0' in array and '1' in array:
        last_one_digit_index = (len(array) - 1) - array[::-1].index('1')
        first_zero_digit_index = array.index('0')
        result = f'Последняя единица под индексом {last_one_digit_index}, ' \
                 f'нули начинаются с индекса {first_zero_digit_index}.'
    else:
        result = 'Некорректный массив: отсутствуют 0 или 1.'
    return result


if __name__ == '__main__':
    array = '111111111111111111111111100000000'
    print(task(array))
