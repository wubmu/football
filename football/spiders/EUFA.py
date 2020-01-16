# -*- coding: utf-8 -*-
import datetime
import random

import js2xml
import scrapy
import scrapy
import logging
import time
from lxml import etree
from requests import request

# from football.spiders import dataAnalysis
from football.spiders.dataAnalysis import DataHandle

logger = logging.getLogger(__name__)





class EufaSpider(scrapy.Spider):
    # cookies = "race_id=701326; Hm_lvt_a68414d98536efc52eeb879f984d8923=1578795943,1578885205,1578885229,1578894438; ds_session=7ch78k4cic7bsr89tlu6lptb77; uid=R-562432-5461160605e1c04e225d7f; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1578895079"
    name = 'EUFA'
    # allowed_domains = ['www.dszuqiu.com']
    headler = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    start_urls = ['https://www.dszuqiu.com/league/117']

    def start_requests(self):
        # cookies ="race_id=701326;Hm_lvt_a68414d98536efc52eeb879f984d8923=1578795943,1578885205,1578885229,1578894438; ds_session=7ch78k4cic7bsr89tlu6lptb77; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1578894546; uid=R-562432-5461160605e1c04e225d7f"
        # cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            # cookies=cookies
        )

    # 赛程爬取
    def parse(self, response):
        match_list = response.xpath("//section[@id='ended']/table[@class='live-list-table diary-table']/tbody/tr")
        for tr in match_list:
            item = {}
            item["name"] = tr.xpath("./td[1]/a/text()").extract_first()
            # 时间格式 19/12/12 01:57 处理成 2019/12/12  4:01:00
            match_time = tr.xpath("./td[3]/text()").extract_first()
            str, year, week = self.handle_time(match_time)
            item["year"] = year
            item["time"] = str
            item["weekday"] = week
            # item["time"] = tr.xpath("./td[3]/text()").extract_first()
            item["homeTeam"] = tr.xpath("./td[4]/a/text()").extract_first().strip()
            item["awayTeam"] = tr.xpath("./td[6]/a/text()").extract_first()
            score = tr.xpath("./td[5]/text()").extract_first().split(":")
            item["hostScore"] = int(score[0].strip())
            item["awayScore"] = int(score[1].strip())
            item["goalDifference"] = int(score[0]) - int(score[1])
            # 爬取到的link /race/701326 重新组装link
            link = tr.xpath("./td[12]/a/@href").extract_first()
            no = link.split("/")[2]

            real_detail_link = "https://www.dszuqiu.com/race_xc/" + no
            item["link"] = real_detail_link
            # 到详情页面继续爬取
            cookies = "race_id=" + no + "; ds_session=o2hdfpu33dupfsjepcfam0bgs2; Hm_lvt_a68414d98536efc52eeb879f984d8923=1578885229,1578894438,1578969849,1579054299; uid=R-562432-73a411e605e1e74ffb1523; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1579054703"
            cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split(";")}

            yield scrapy.Request("https://www.dszuqiu.com/race_sp/" + no, callback=self.parse_detail_info,
                                 dont_filter=True, meta={"item": item, "no": no}, cookies=cookies
                                 )
        # 找到下一页url地址
        next_page = response.xpath("//*[@id='pager']/a[10]")[0]
        next_url = next_page.xpath("./@data-url").extract_first()
        real_url = "www.dszuqiu.com" + next_url
        # yield scrapy.Request(real_url, headers=self.headler, callback=self.parse, dont_filter=True)


    # 爬取让球实时数据页面

    def parse_detail_info(self, response):
        print("开始爬取详细页面----------")
        item = response.meta["item"]
        no = response.meta["no"]
        letBalls = response.xpath('//*[@id="sp_rangfen"]/tr')
        # letBalls = response.xpath('//*[@id="annlysisSpNav1-2"]/div/div[2]/table[1]')
        letBalls_processing = []
        for lb in letBalls:
            letBall = {}
            # //*[@id="sp_rangfen"]/tr[1]/td[1]
            letBall["match_time"] = lb.xpath("./td[1]/text()").extract_first().strip().replace("'", "")
            letBall["score"] = lb.xpath("./td[2]/text()").extract_first()

            # 处理 - 的
            home_team = lb.xpath("./td[3]/text()").extract_first()
            if home_team == '-':
                home_team = 0.0
            else:
                home_team = float(home_team)
            letBall["home_team"] = home_team
            # 得处理有的是 - 有的是 0.5 有的是0.5,0.2 有的是0.5
            letBall["let_ball"] = lb.xpath("./td[4]/text()").extract_first()

            # 处理 - 的
            away_team = lb.xpath("./td[5]/text()").extract_first()
            if away_team == '-':
                away_team = 0.0
            else:
                away_team = float(away_team)
            letBall["away_team"] = away_team

            letBall["away_team"] = away_team
            letBall["time"] = lb.xpath("./td[6]/text()").extract_first()
            # print(letBall)
            letBalls_processing.append(letBall)
        logger.warning(item)
        logger.warning(letBalls_processing)
        print("让球数据格式-----------------------")
        # print(str(letBalls_processing))
        # print(letBalls_processing)
        print("准备进入现场" + no)
        time.sleep(int(format(random.randint(0, 9))))
        cookies = "uid=R-562432-73a411e605e1e74ffb1523; ds_session=5bpuqsh9in3dmdt3amlh7ti823; Hm_lvt_a68414d98536efc52eeb879f984d8923=1578894438,1578969849,1579054299,1579138698; Hm_lpvt_a68414d98536efc52eeb879f984d8923=1579138748"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split(";")}
        yield scrapy.Request(url="https://www.dszuqiu.com/race_xc/"+no,
                             callback=self.parse_live_info,
                             dont_filter=True,
                             cookies=cookies,
                             meta={"item":item,"letBalls":letBalls_processing})

    def parse_live_info(self, response):
        # 抓取现场数据’ https://www.dszuqiu.com/race_xc/701326
        print("开始抓取现场数据")
        names = response.xpath("//script")[-5]
        js_text = names.xpath("./text()").extract_first()
        script_text = js2xml.parse(js_text, encoding='utf-8', debug=False)
        script_tree = js2xml.pretty_print(script_text)
        selector = etree.HTML(script_tree)
        data_s = selector.xpath("//property[@name='data']")
        dics = []
        for xys in data_s:
            xs = xys.xpath(".//property[@name='x']/number/@value")
            ys = xys.xpath(".//property[@name='y']/number/@value")
            dic = dict(map(lambda x, y: [x, y], xs, ys))
            dics.append(dic)
        logger.warning(response)
        logger.warning(dics)

        item = response.meta["item"]
        letballs = response.meta["letBalls"]
        match_data = DataHandle().all_data_handle(item,letballs,dics)
        # item = response.meta["item"]
        # print(response.xpath("//script"))
        # print(item)
        # print(match_data)
        line_data = {}
        item_values = item.values()
        line_data["match_info"] = item_values
        line_data["match_data"] = match_data

        yield line_data

    def handle_time(self,str):
        datas = str.split("/")
        datas[0] = "20" + datas[0]
        str = '/'.join(datas)
        year = datas[0]
        str2date = datetime.datetime.strptime(str, "%Y/%m/%d %H:%M")  # 字符串转化为date形式
        week = self.get_week_day(str2date)
        return str,year,week
    def get_week_day(self,date):
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