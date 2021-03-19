import time


def len_is_even(element: list) -> bool:
    """Службная функция для проверки интервалов на четность."""
    return len(element) % 2 == 0


def data_is_correct(data: dict) -> bool:
    """Службная функция для проверки переданных данных на корректность."""
    if len(data) != 3:
        return False

    for element in data:
        if not len_is_even(data[element]):
            return False

    return True


def split_intervals_list(intervals: list) -> list:
    """Служебная функция для разделения списка интервалов на пары."""
    return [interval for interval in range(len(intervals)) if interval % 2 == 0]


def attendance_in_lesson_time(lesson_start_time: int, lesson_end_time: int, intervals: list) -> list:
    """Функция проверяет интервалы присутствия и корректирует/отбрасывает интервалы вне времени урока."""
    attendance_intervals = []
    arrival_intervals = split_intervals_list(intervals)

    for interval in arrival_intervals:
        start_of_interval = intervals[interval]
        end_of_interval = intervals[interval + 1]

        if lesson_start_time <= lesson_end_time:

            if start_of_interval <= lesson_start_time < end_of_interval:
                attendance_intervals.append(lesson_start_time)
            elif lesson_start_time <= start_of_interval <= lesson_end_time:
                attendance_intervals.append(start_of_interval)

            if lesson_end_time >= end_of_interval > lesson_start_time:
                attendance_intervals.append(end_of_interval)
            elif end_of_interval > lesson_end_time > start_of_interval >= lesson_start_time:
                attendance_intervals.append(lesson_end_time)

        else:
            raise SystemExit(f'Некорректное время урока: время начала урока ({time.ctime(lesson_start_time)}) позже, '
                             f'чем время завершения урока ({time.ctime(lesson_end_time)}).')

    return attendance_intervals


def count_time_in_border(start_border: int, end_border: int, intervals_to_count: list) -> int:
    """Вспомогательная функция для поиска и сложения совпадающих интервалов присутствия."""
    total_time = 0
    arrival_intervals = split_intervals_list(intervals_to_count)

    for interval in arrival_intervals:
        start_of_interval = intervals_to_count[interval]
        end_of_interval = intervals_to_count[interval + 1]
        start_of_interval_to_count = 0
        end_of_interval_to_count = 0

        if start_of_interval <= start_border < end_of_interval:
            start_of_interval_to_count = start_border
        elif start_border <= start_of_interval <= end_border:
            start_of_interval_to_count = start_of_interval

        if end_border >= end_of_interval > start_border:
            end_of_interval_to_count = end_of_interval
        elif end_of_interval > end_border > start_of_interval >= start_border:
            end_of_interval_to_count = end_border

        total_time += (end_of_interval_to_count - start_of_interval_to_count)

    return total_time


def total_time_of_attendance_counter(pupil_intervals: list, tutor_intervals: list) -> int:
    """Функция подсчитывает общее время присутствия ученика и преподавателя."""
    total_time_of_attendance = 0
    tutor_intervals_index = split_intervals_list(tutor_intervals)

    for interval in tutor_intervals_index:
        tutor_start_of_interval = tutor_intervals[interval]
        tutor_end_of_interval = tutor_intervals[interval + 1]

        total_time_of_attendance += count_time_in_border(
            start_border=tutor_start_of_interval,
            end_border=tutor_end_of_interval,
            intervals_to_count=pupil_intervals
        )

    return total_time_of_attendance


def appearance(intervals: dict) -> int:
    """Функция-агрегатор принимает данные и возвращает общее время присутствия ученика и преподавателя в секундах."""
    if not data_is_correct(intervals):
        raise SystemExit('Переданные данные некорректны.')

    lesson_start_time = intervals['lesson'][0]
    lesson_end_time = intervals['lesson'][1]

    pupil_intervals = attendance_in_lesson_time(
        lesson_start_time=lesson_start_time,
        lesson_end_time=lesson_end_time,
        intervals=intervals['pupil']
    )
    tutor_intervals = attendance_in_lesson_time(
        lesson_start_time=lesson_start_time,
        lesson_end_time=lesson_end_time,
        intervals=intervals['tutor']
    )

    total_time_of_attendance = total_time_of_attendance_counter(
        pupil_intervals=pupil_intervals,
        tutor_intervals=tutor_intervals
    )

    return total_time_of_attendance


if __name__ == '__main__':
    data = {
        'lesson': [1594663200, 1594666800],
        'pupil': [1594663000, 1594663199, 1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
        'tutor': [1594663290, 1594663430, 1594663443, 1594666473, 1594666890, 1594666990]
    }
    print(appearance(data))
