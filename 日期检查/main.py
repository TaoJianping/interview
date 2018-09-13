import datetime


def get_third_saturday(year, month):
    count = 0
    day = 1
    while True:
        week_day = int(datetime.datetime(year, month, day).strftime("%w"))
        if week_day == 6:
            count += 1
        if count == 3:
            return day
        day += 1


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
    saturday_day = get_third_saturday(year=year, month=month)
    if day <= saturday_day:
        return False
    else:
        return True


def test_get_third_saturday():
    year = 2018
    month_one = 1
    month_two = 3
    month_three = 6
    month_four = 7
    month_five = 10
    month_six = 12

    assert get_third_saturday(year, month_one) == 20
    assert get_third_saturday(year, month_two) == 17
    assert get_third_saturday(year, month_three) == 16
    assert get_third_saturday(year, month_four) == 21
    assert get_third_saturday(year, month_five) == 20
    assert get_third_saturday(year, month_six) == 15


def test_check_date():
    be_checked_date_one = "20180101"
    be_checked_date_two = "20180115"
    be_checked_date_three = "20180927"
    be_checked_date_four = "20180818"
    be_checked_date_five = "20180819"
    be_checked_date_six = "20180317"
    be_checked_date_seven = "20180422"
    be_checked_date_eight = "20181021"
    be_checked_date_nine = "20181215"

    assert check_date(be_checked_date_one) is False
    assert check_date(be_checked_date_two) is False
    assert check_date(be_checked_date_three) is True
    assert check_date(be_checked_date_four) is False
    assert check_date(be_checked_date_five) is True
    assert check_date(be_checked_date_six) is False
    assert check_date(be_checked_date_seven) is True
    assert check_date(be_checked_date_eight) is True
    assert check_date(be_checked_date_nine) is False


if __name__ == '__main__':
    test_get_third_saturday()
    test_check_date()
