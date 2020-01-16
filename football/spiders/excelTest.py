# from openpyxl import Workbook
# wb = Workbook()
# ws = wb.active
# data = ["0",1,231,3123121,2312321]
# ws.append(data)
# wb.save("F:\\dsFootball.xlsx")


import time, datetime


def get_week_day(date):
    week_day_dict = {
        0: '周一',
        1: '周二',
        2: '周三',
        3: '周四',
        4: '周五',
        5: '周六',
        6: '周天',
    }
    day = date.weekday()
    return week_day_dict[day]

str="19/12/12 4:01"
datas = str.split("/")
datas[0] = "20"+datas[0]
str='/'.join(datas)
year = datas[0]

str2date=datetime.datetime.strptime(str,"%Y/%m/%d %H:%M")#字符串转化为date形式
print(get_week_day(str2date))

# dates = str.split("/")
