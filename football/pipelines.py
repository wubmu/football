# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class FootballPipeline(object):
    def __init__(self):
        self.wbook = Workbook()
        # 激活工作表
        self.wsheet = self.wbook.active
        # 设置表头
        head = ["比赛类型","年份","时间","星期几","主队","客队","主进","客进","净胜球","链接"]
        minites = [6, 10, 13, 16, 20, 23, 26, 30, 33, 36, 38, 43, "半",
                50, 53, 56, 60, 63, 66, 70, 73, 76, 80, 83, 86, 88]
        for minite in minites:
            head.append(str(minite)+"滚比")
            head.append(str(minite)+"净胜球")
            head.append(str(minite)+"盘口")
            head.append(str(minite)+"主危")
            head.append(str(minite)+"客危")
            head.append(str(minite)+"危比")
            head.append(str(minite)+"主攻")
            head.append(str(minite)+"客攻")
            head.append(str(minite)+"攻比")
            head.append(str(minite)+"主正")
            head.append(str(minite)+"客正")
            head.append(str(minite)+"主总")
            head.append(str(minite)+"客总")
            head.append(str(minite)+"射差")
            head.append(str(minite)+"射比")
            head.append(str(minite)+"主")
            head.append(str(minite)+"客")
        self.wsheet.append(head)
    def process_item(self, item, spider):
        line_data = []
        match_info = item["match_info"]
        match_data = item["match_data"]
        # match_info.append(match_data)
        for v in match_info:
            line_data.append(v)
        line_data.extend(match_data)

        print("进去持久层保存数据-------------------------")
        print("一行数据----------------------------------")
        print(line_data)
        self.wsheet.append(line_data)
        self.wbook.save('F:\\dsFootball.xlsx')
        return item
