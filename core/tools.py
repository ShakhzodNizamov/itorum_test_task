from datetime import date
import calendar


def get_week_list(to_str=False):
    """
    Возвращает список недель этого месяца
    :param to_str: Если True, то дата возвращается в виде строки
    :return:
    """
    def get_date(day):
        return date.today().replace(day=day).strftime('%d. %m. %Y ') if to_str else date.today().replace(day=day)

    last_day_of_current_month = calendar.monthrange(date.today().year, date.today().month)[1]

    first_sunday = 0
    for i in range(1, last_day_of_current_month + 1):
        if calendar.SUNDAY == date.weekday(date.today().replace(day=i)):
            first_sunday = i
            break

    week_list = [(get_date(1), get_date(first_sunday))]
    first_sunday += 1

    for i in range(first_sunday + 6, last_day_of_current_month + 1, 7):
        week_list.append((get_date(first_sunday), get_date(i)))
        first_sunday = i + 1

    if last_day_of_current_month >= first_sunday:
        week_list.append((get_date(first_sunday), get_date(last_day_of_current_month)))

    if to_str:
        week_list = [f'{idx + 1})  {i[0]}  -  {i[1]}' for idx, i in enumerate(week_list)]

    return week_list


def get_current_week():
    weeks = get_week_list()
    today = date.today()
    for idx, i in enumerate(weeks):
        if i[0] <= today <= i[1]:
            return idx
    return 0

