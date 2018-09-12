import datetime


def get_week_of_month(year, month, day):
    """
    计算这个日期在这个月份的第几个星期
    :param year: (int) 年份
    :param month: (int) 月份
    :param day: (int) 几号
    :return: (int) 第几个日期
    """
    end = int(datetime.datetime(year, month, day).strftime("%W"))
    begin = int(datetime.datetime(year, month, 1).strftime("%W"))
    return end - begin + 1


def check_date(checking_date):
    """
    检查沪牌拍卖日期是否过期
    :param checking_date: (str) 需要检查的日期 example => "20180901"
    :return: 
    """
    dt = datetime.datetime.strptime(checking_date, "%Y%m%d").timetuple()
    year = dt[0]
    month = dt[1]
    day = dt[2]
    # 比较是第几周
    week_number = get_week_of_month(year=year, month=month, day=day)
    if week_number > 3:
        return True
    if week_number < 3:
        return False
    # 比较星期几
    week_day = int(datetime.datetime(year, month, day).strftime("%w"))
    if week_day == 0:
        return True

    return False


def test_check_date():
    be_checked_date_one = "20180901"
    be_checked_date_two = "20180915"
    be_checked_date_three = "20180916"
    be_checked_date_four = "20180818"
    be_checked_date_five = "20180819"

    assert check_date(be_checked_date_one) == False
    assert check_date(be_checked_date_two) == False
    assert check_date(be_checked_date_three) == True
    assert check_date(be_checked_date_four) == False
    assert check_date(be_checked_date_five) == True


if __name__ == '__main__':
    test_check_date()