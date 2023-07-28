 # -*- coding: utf-8 -*-
import sys

from scrapy.utils.python import unique

sys.path.append("../../../..")
import json
import random
from copy import deepcopy
from pprint import pprint
from item.HtmlCleaners import process_cleaned_data
from item.extract_html_classify import ExtractHtmlClassify
import demjson

IS_Current = __name__ != "__main__"
import scrapy
from scrapy import Request, Spider
from bs4 import BeautifulSoup
from jsonpath import jsonpath
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
import re
import html
from json import loads
from re import findall
import requests
from parsel import Selector


class FabrikstyleSpider(scrapy.Spider):
    name = '支付填充数据网站fabrikstyle.com(0.01-169)'
    allowed_domains = ['fabrikstyle.com']
    #  包含待处理的HTML字符串的列表
    html_str_list = [
        '''<div id="main-content" class="wiki-content">
                           
        <p style="">全站采集，图片不要有logo，去掉品牌，产品描述里头不要有类似脸书/推特的链接，不要采集类似家具的大件产品；<br>每份数据4个分类，数据总量控制在100个左右<br>产品数据不要有评价信息的部分<br>标题描述里头不要出现打折等折扣字眼<span style="color: rgb(23,43,77);">；不采集“SOLD OUT”及其相关促销信息</span><br>库存用三位数随机<br>每份填充数据产品不要有重复<br>产品要带有属性<br>不采集产品描述中的图片<br><span style="color: rgb(23,43,77);">产品标题与描述规避删除“Free Shipping”这一词以及所有退换货及运输政策相关信息</span></p><p style="">产品原价0.01-169之间的数据，按那30个固定价格定价</p><p style="">不采集以下标题产品：</p><p style="">LOURDES PRINTED PUFF SLEEVE SWEATER</p><p style="">SALE - Z SUPPLY MODERN WEEKENDER</p><p style="">Venetia Gauze Pant - OFF WHITE</p><p style="">去掉所有产品第一个单词</p><p style="">不采集产品标题带有“Fab'rik”一词的产品</p><p style="">去掉产品描述中“Please note, this item is final sale”句段</p><p style="">去掉所有产品描述的第一大段</p><p style="">筛选去掉产品标题和描述中的“fabrikstyle", "sexy", "free", "SALE", "Z Supply”一词</p><p style="">货币统一设为美元</p><p style=""><span style="color: rgb(23,43,77);">按广告需求采集op和wp格式</span></p><p style=""><span style="color: rgb(23,43,77);">分类名：Dresses</span></p><p style=""><span style="color: rgb(23,43,77);"><a class="external-link" href="https://fabrikstyle.com/collections/dresses" rel="nofollow">https://fabrikstyle.com/collections/dresses</a></span></p><p style=""><span style="color: rgb(23,43,77);">分类名：Blouses</span></p><p style=""><span style="color: rgb(23,43,77);"><a class="external-link" href="https://fabrikstyle.com/collections/blouses" rel="nofollow">https://fabrikstyle.com/collections/blouses</a></span></p><p style=""><span style="color: rgb(23,43,77);">分类名：Sweaters</span></p><p style=""><span style="color: rgb(23,43,77);"><a class="external-link" href="https://fabrikstyle.com/collections/sweaters" rel="nofollow">https://fabrikstyle.com/collections/sweaters</a></span></p><p style=""><span style="color: rgb(23,43,77);">分类名：Pants</span></p><p style=""><span style="color: rgb(23,43,77);"><a class="external-link" href="https://fabrikstyle.com/collections/pants" rel="nofollow">https://fabrikstyle.com/collections/pants</a></span></p><p style=""><span style="color: rgb(23,43,77);">分类名：Skirts + Shorts</span></p><p style=""><span style="color: rgb(23,43,77);"><a class="external-link" href="https://fabrikstyle.com/collections/skirts-shorts" rel="nofollow">https://fabrikstyle.com/collections/skirts-shorts</a></span></p>

                
        
    
        </div>
    '''
    ]
    # 自定义的scrapy设置
    custom_settings = {
        # 'DOWNLOAD_DELAY': 0.1,
        # "CONCURRENT_REQUESTS": 10,
        # "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        # "CONCURRENT_REQUESTS_PER_IP": 1,
        "DOWNLOADER_MIDDLEWARES": {
            # 'Shopzze.middlewares.Seleniummiddleware': 200,
            'Shopzze.middlewares.MyUserAgentMiddleware': 100,
        },
        "ITEM_PIPELINES":
            {
                # 'Shopzze.pipelines.DescriptionImagesPipeline': 200,
                'Shopzze.pipelines.OthersImagesPipeline': 300,
                # 'Shopzze.pipelines.AttimgImagesPipeline': 100,
                'Shopzze.pipelines.Opencard_302s_Pipeline': 500,
                # 'Shopzze.pipelines.WordpressPipeline': 600,
            }

    }

    # custom_settings = {
    #     # 'DOWNLOAD_DELAY': 0.1,
    #     # "CONCURRENT_REQUESTS": 10,
    #     # "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
    #     # "CONCURRENT_REQUESTS_PER_IP": 1,
    #     "DOWNLOADER_MIDDLEWARES": {
    #         # 'Shopzze.middlewares.Seleniummiddleware': 200,
    #         'Shopzze.middlewares.MyUserAgentMiddleware': 100,
    #     },
    #     "ITEM_PIPELINES":
    #         {
    #             'Shopzze.pipelines.DescriptionOssPipeline': 200,
    #             'Shopzze.pipelines.OthersOssPipeline': 300,
    #             'Shopzze.pipelines.AttimgOssPipeline': 100,
    #             # 'Shopzze.pipelines.WordpressPipeline': 500,
    #             'Shopzze.pipelines.MysqlPipeline': 500,
    #         }
    #
    # }
    # 定义了一个列表变量'Filter_brand'，其中包含需要过滤的品牌名称
    Filter_brand = [
        "LOURDES PRINTED PUFF SLEEVE SWEATER",
        "SALE - Z SUPPLY MODERN WEEKENDER",
        "Venetia Gauze Pant - OFF WHITE",
        "Fab'rik"
    ]

    def start_requests(self):
        for html_str_index, html_str in enumerate(self.html_str_list):
            extract_html_classify = ExtractHtmlClassify()
            new_csv_classify_dict = extract_html_classify.get_html_classify(html_str)

            print(new_csv_classify_dict)
            # enumerate函数用于遍历new_csv_classify_dict字典的键值对，并返回每个键值对的索引和值。索引值即为origin_url_index，用于标识不同的原始URL
            for origin_url_index, origin_url in enumerate(new_csv_classify_dict):
                type_tuple = new_csv_classify_dict[origin_url]
                print("type_tuple:{}".format(type_tuple))
                if type_tuple:
                    yield scrapy.Request(url=origin_url, callback=self.parse,
                                         meta={'type_tuple': type_tuple, 'origin_url_index': origin_url_index,
                                               'html_str_index': html_str_index},
                                         )

    def parse(self, response):
        type_tuple = response.meta['type_tuple']
        item = dict()
        item['update_name'] = "lu"
        item["delete_brand"] = ["fabrikstyle", "sexy", "free", "SALE", "Z Supply"]
        item['origin_url_index'] = response.meta['origin_url_index']
        item['html_str_index'] = response.meta['html_str_index']
        item["type_num"] = 3

        for one_type_index, one_type in enumerate(type_tuple, start=1):
            item['type_{}'.format(one_type_index)] = one_type # type_1: NEW

        product_list = response.xpath('//p[@class="grid-link__title"]/a')
        print('----{}----数据总量：{}'.format(type_tuple, len(product_list))) # ----NEW----数据总量：66
            item["details"] = response.urljoin(ele.xpath('./@href').extract_first())
            yield scrapy.Request(url=item["details"],
                                 callback=self.parse_details,
                                 meta={'item': deepcopy(item)})

        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            # print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse,
                                 meta={"type_tuple": type_tuple, 'origin_url_index': item['origin_url_index'],
                                       'html_str_index': item['html_str_index']})

    def parse_details(self, response: HtmlResponse):
        item = response.meta["item"]

        product_data = re.findall('window\.SwymProductInfo\.product = ([\s\S]*?)};', response.text)
        product_data = json.loads(product_data[0] + '}')

        # # item["SKU"] = str(response.xpath('//div[@class="sku"]/text()').extract_first().split(':')[-1].strip())
        product_title = product_data['title']
        flag = False
        # 不采集以下标题产品：
        # </p><p style="">LOURDES PRINTED PUFF SLEEVE SWEATER</p>
        # <p style="">SALE - Z SUPPLY MODERN WEEKENDER</p>
        # <p style="">Venetia Gauze Pant - OFF WHITE</p><p style="">
        # 不采集产品标题带有“Fab'rik”一词的产品
        for brand in self.Filter_brand:
            if re.findall(brand, product_title, re.IGNORECASE):
                flag = True
                break
        if flag:
            return

        if not product_title:
            return
        # 去掉所有产品第一个单词
        item["product_title"] = ' '.join(product_title.split(' ')[1:])
        item["handle"] = product_data['handle']

        original_price = product_data['price']
        item["original_price"] = original_price / 100
        item["Product_price"] = item["special_price"] = item["original_price"]

        item["description"] = response.xpath('//div[@id="home"]').extract_first()
        # 去掉所有产品描述的第一大段
        p_desc = response.xpath('//div[@id="home"]/p[1]').extract_first()
        item["description"] = item["description"].replace(p_desc,'')

        for ele in response.xpath('//div[@id="home"]/p').extract():
            # 去掉产品描述中“Please note, this item is final sale”句段
            if 'Please note, this item is final sale' in ele:
                item["description"] = item["description"].replace(ele, '')
        item["description"] = process_cleaned_data(item['description']).replace('\n', '') if item['description'] else ''

        item["pd_img_list"] = [response.urljoin(ele["src"]) for ele in
                               BeautifulSoup(item['description'], "lxml").find_all('img')]

        item["other_image_urls"] = product_data['images']
        item["other_image_urls"] = ['https:' + ele.split('?')[0] for ele in item["other_image_urls"]]

        item["option"] = list()
        item["att_val_img"] = list() # 属性值
        group_dict = dict()
        have_color_type_name = ''

        products_list = product_data['options']
        if len(products_list) == 1 and products_list[0] == 'Title':
            products_list = []

        if products_list:
            for index, one_option_xpath in enumerate(products_list):
                type_name = one_option_xpath
                if not type_name:
                    continue
                type_name = type_name.split("_")[0].replace('-', ' ').replace('|', ' ').replace(':',
                                                                                                '').replace('Choose a',
                                                                                                            '').strip().capitalize()
                if type_name == 'Color':
                    type_name = 'Colors'

                if type_name not in item["option"]:
                    item["option"].append(type_name)
                    type_name_index = item["option"].index(type_name)
                    item[f"option{type_name_index + 1}_list"] = list()

                type_name_index = item["option"].index(type_name)
                item[f"option{index + 1}_list"] = list()

                for e in product_data['variants']:
                    types1 = e['option{}'.format(index + 1)]
                    types1 = types1.replace('-', ' ').replace('|', ' ').replace(':', ' ').replace('\n', ' ').replace(
                        ',',
                        ' ').replace(
                        '=', ' ').strip()

                    if types1 not in item[f"option{type_name_index + 1}_list"]:
                        item[f"option{type_name_index + 1}_list"].append(types1)

                        types2 = "0"
                        if type_name == 'Colors':
                            types_img = ''
                            if e.get('featured_image'):
                                types_img = e['featured_image']['src']
                            if types_img:
                                types2 = response.urljoin(types_img.replace('/50x50/', '/670x890/'))
                                have_color_type_name = type_name
                                group_dict[types1] = types2

                        types = "|".join([type_name + ":" + types1 + "-10000-1-0-0-0-0", types2])
                        item["att_val_img"].append(types)

        if have_color_type_name:
            item["option_image_urls_dict"] = {have_color_type_name: group_dict}

        item['quantity'] = str(random.randint(100, 999))
        print(item)
        # yield item


if __name__ == '__main__':
    cp = CrawlerProcess(get_project_settings())
    cp.crawl(FabrikstyleSpider)
    cp.start()
