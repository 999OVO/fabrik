 # -*- coding: utf-8 -*-
import sys

from scrapy.utils.python import unique

sys.path.append("../../../..")
import json
import random
import ast
from copy import deepcopy
from pprint import pprint
from HtmlCleaners import process_cleaned_data
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
import time
from lxml import etree
import html
from json import loads
from re import findall
import requests
from parsel import Selector


class Fab_pageSpider(scrapy.Spider):
    name = '支付填充数据网站fabrikstyle.com(0.01-169)'
    # allowed_domains = ['fabrikstyle.com']
    #  包含待处理的HTML字符串的列表
    # 拿到要包含所有所需链接的最小html片段，后期用自己写的xpath表达式，拿到每个链接
    # 这个途径可以避免页面内容反复修改，且不需要定位数据接口（存疑）
    # 截取源码中包含所有分类的html片段
    start_urls = [
        """<ul class="nav site-nav  site-nav--center"><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/new-arrivals?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">NEW!<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-arrivals?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All New</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Bottoms</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-accessories?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Accessories</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/spring-lookbook?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Featured</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/recruitment-ready?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rush Ready</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/summer-lookbook?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Summer Lookbook</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/vacation-ready?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Vacation Ready</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/little-white-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Little White Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/bold-brights?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Punch of Color</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Trending</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/best-dressed-guest?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Perfect Plus One</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/coastal-cowgirl?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Coastal Cowgirl</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/printed-to-perfection?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Printed to Perfection</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/high-contrast?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:High Contrast</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--smalldropdown"><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Clothing<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown  js-mobile-menu-dropdown small-dropdown"><ul class="small-dropdown__container"><li class="small-dropdown__item "><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Clothes</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/best-sellers?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Best Sellers</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Dresses</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Tops</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rompers+Jumpsuits</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/pants?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Pants+Leggings</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/skirts-shorts?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Skirts+Shorts</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/matching-sets?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Matching Sets</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/denim?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Denim</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sweaters+Sweatshirts</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/jackets-coats?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Jackets+Coats</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/spanx?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Spanx</a></li><li class="small-dropdown__subitem"><a href="/products/gift-card"class="site-nav__link site-nav__dropdown-link">Gift Cards</a></li></ul></div></li></ul></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Dresses<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">New Dresses</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/midi-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Midi</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/mini-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Mini</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/maxi-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Maxi</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rompers&amp;Jumpsuits</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY OCCASION</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1&amp;occasion=Cocktail,Party"class="site-nav__link site-nav__dropdown-link">Party&amp;Cocktail Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/casual-dresses-1?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Casual Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1&amp;limit=30&amp;occasion=Printed"class="site-nav__link site-nav__dropdown-link">Printed Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/little-white-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Little White Dresses</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link">Rompers&amp;Jumpsuits</a></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Tops<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Tops</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Tops</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/blouses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Blouses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/cropped-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Cropped Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tees-basics-1?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">T-Shirts&amp;Basics</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tanks-camis?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Tanks&amp;Bodysuits</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sweaters</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">TRENDING</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/going-out-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Going Out Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/workwear-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Workwear Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/printed-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Printed Tops</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/bottoms?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Bottoms<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">New Bottoms</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/pants?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Pants</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/denim?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Denim</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/shorts-skirts?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Shorts+Skirts</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/spanx?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">SPANX</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item"><a href="https://fabrikstyle.com/collections/shoes?filter.v.availability=1"class="site-nav__link">Shoes</a></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--smalldropdown"><a href="https://fabrikstyle.com/collections/accessories?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Accessories<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown  js-mobile-menu-dropdown small-dropdown"><ul class="small-dropdown__container"><li class="small-dropdown__item "><a href="https://fabrikstyle.com/collections/accessories?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Accessories</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/jewelry?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Jewelry</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/hats-scarves?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Hats&amp;Scarves</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/bags?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Bags&amp;Sunglasses</a></li></ul></div></li></ul></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Sale<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Sale</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Bottoms</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Sweaters</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/final-few?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Final Few</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">By Price</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A20"class="site-nav__link site-nav__dropdown-link">Under $20</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A30"class="site-nav__link site-nav__dropdown-link">Under $30</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A40"class="site-nav__link site-nav__dropdown-link">Under $40</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A50"class="site-nav__link site-nav__dropdown-link">Under $50</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A60"class="site-nav__link site-nav__dropdown-link">Under $60</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__more-links more-links site-nav__invisible site-nav__item--has-dropdown"><a href="#"class="site-nav__link"aria-haspopup="true"aria-expanded="false">More links<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown small-dropdown more-links-dropdown"><div class="page-width relative"><ul class="small-dropdown__container"></ul><div class="more-links__dropdown-container"></div></div></div></li></ul>
    """
    ]
    # 自定义的scrapy设置
    # 开启一个UA中间件和两个自定义管道，用于存储数据和图像
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            # 'Shopzze.middlewares.Seleniummiddleware': 200,
            'fa_test.middlewares.MyUserAgentMiddleware': 100,
        },
        "ITEM_PIPELINES":
            {
                # 'Shopzze.pipelines.DescriptionImagesPipeline': 200,
                'fa_test.pipelines.OthersImagesPipeline': 300,
                # 'Shopzze.pipelines.AttimgImagesPipeline': 100,
                'fa_test.pipelines.Opencard_302s_Pipeline': 500,
                # 'Shopzze.pipelines.WordpressPipeline': 600,
            }

    }

    # 声明标题中不需要的内容为Filter_brand
    # 不采集以下标题产品：
    # </p><p style="">LOURDES PRINTED PUFF SLEEVE SWEATER</p>
    # <p style="">SALE - Z SUPPLY MODERN WEEKENDER</p>
    # <p style="">Venetia Gauze Pant - OFF WHITE</p><p style="">
    # 不采集产品标题带有“Fab'rik”一词的产品
    Filter_brand = [
        "LOURDES PRINTED PUFF SLEEVE SWEATER",
        "SALE - Z SUPPLY MODERN WEEKENDER",
        "Venetia Gauze Pant - OFF WHITE",
        "Fab'rik"
    ]
# 用lxml解析html字段，提取出分类及其URL，并发送大类请求
    all_collection_scopes = []
    all_collection_handles = []

    def start_requests(self):
        # 获取大页url及分类元组
        all_new_classify_list = []
        all_tuple_classify_first_url = []

        html_etree = etree.HTML(self.start_urls[0])
        first_categories = html_etree.xpath('//ul[@class="nav site-nav  site-nav--center"]/li/a/text()')[:-1]
        first_categories_urls = html_etree.xpath('//ul[@class="nav site-nav  site-nav--center"]/li/a/@href')[:-1]
        # zip同时迭代多个序列
        for category, url in zip(first_categories, first_categories_urls):
            url = url.replace('?filter.v.availability=1', '')
            all_tuple_classify_first_url.append(url)
            all_new_classify_list.append((category,))
        # 将域名和分类字典化
        new_csv_classify_dict = dict(zip(all_tuple_classify_first_url, all_new_classify_list))
        print(new_csv_classify_dict)
        for origin_url_index, origin_url in enumerate(new_csv_classify_dict):
            type_tuple = new_csv_classify_dict[origin_url]
            print(f"type_tuple:{type_tuple}")

            if type_tuple:
                # 向每个大类页发起请求，例如url = https://fabrikstyle.com/collections/dresses', 回调函数为parse
                # 元数据为字典：{'type_tuple': ('Blouses',), 'origin_url_index': 2})，传递的原因是因为解析可能要用这些元数据
                yield scrapy.Request(url=origin_url, callback=self.parse, meta={'type_tuple': type_tuple, 'origin_url_index': origin_url_index})
        # 获取第一页的collection_scope
        # collection_scope = [57115050042, 262358532154, 57116622906, 57118621754, 83666632762]
        # base_url = 'https://services.mybcapps.com/bc-sf-filter/filter?t={timestamp}&_=pf&shop=fabrik-style.myshopify.com&page={page}&limit=24&sort=relevance&locale=en&event_type=collection&build_filter_tree=true&sid=2d79bf4e-fd7f-4415-9eba-38ee688374ff&pg=collection_page&zero_options=true&product_available=true&variant_available=true&sort_first=available&urlScheme=2&collection_scope={collection}'

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        #     'Referer': 'https://fabrikstyle.com/'
        # }
        # for collection in collection_scope:
        #     page = 1  # 默认初始页数为1
        #     count = 0  # 计数器变量
        #
        #     while count < 8:  # 限制循环次数不超过8次
        #         url = base_url.format(timestamp=str(int(round(time.time() * 1000))), page=page, collection=collection)
        #         request = scrapy.Request(url=url, headers=headers)
        #         yield request
        #
        #         count += 1  # 增加计数器
        #         page += 1  # 递增页数

# parse基于每大页的响应，拿到请求参数，定制数据包请求url，并发送请求
    def parse(self, response, **kwargs):
        type_tuple = response.meta['type_tuple']
        origin_url_index = response.meta['origin_url_index']
        item = dict()
        for one_type_index, one_type in enumerate(type_tuple, start=1):
            # 将值 one_type 分配给名为 'type_1' 的键 （或“type_2”、“type_3”等，具体取决于循环）
            item[f'type_{one_type_index}'] = one_type
            print(f"type_{one_type_index}:{item[f'type_{one_type_index}']}")
        # 从大类发送回的响应中，提取出发送数据包请求所需的参数
        collection_scope = re.findall(r'collection:\s*\{[^}]*id:\s*([^,\n]+)', response.text)[0]
        collection_handle = re.findall(r"collection:\s*\{[^}]*handle:\s*'([^,\n]+)'", response.text)[0]

        # 将collection_scope和collection_handle保存为实例属性
        Fab_pageSpider.all_collection_scopes.append(collection_scope)
        Fab_pageSpider.all_collection_handles.append(collection_handle)
        print(Fab_pageSpider.all_collection_scopes)
        print(Fab_pageSpider.all_collection_handles)

        for collection_scope in Fab_pageSpider.all_collection_scopes:
            page = 1
            base_url = 'https://services.mybcapps.com/bc-sf-filter/filter?t={timestamp}&_=pf&shop=fabrik-style.myshopify.com&page={page}&limit=24&sort=relevance&locale=en&event_type=collection&build_filter_tree=true&sid=d1879230-b692-4693-9586-ce85fca2e98c&pg=collection_page&zero_options=true&product_available=true&variant_available=true&sort_first=available&urlScheme=2&collection_scope={collection}&collectionId={collection}&handle={collection_handle}'
            url = base_url.format(timestamp=str(int(round(time.time() * 1000))), collection=collection_scope,
                                  collection_handle=collection_handle, page=page)
            # 发送第一页请求
            yield scrapy.Request(url=url, callback=self.parse_bag,
                                 meta={"type_tuple": type_tuple, 'origin_url_index': origin_url_index,
                                       'collection': collection_scope, 'collection_handle': collection_handle,
                                       'item': deepcopy(item)
                                       })

            # yield scrapy.Request(url=url, callback=self.parse_bag,
            #                      meta={"type_tuple": type_tuple, 'origin_url_index': item['origin_url_index'],
            #                            'item': deepcopy(item)
            #                            })

# 使用urljoin补全翻页链接，比字符串拼接容错率更高   next_page = response.urljoin(next_page)
# parse_bag解析数据包发回来的数据（包含每页商品数据列表），注意，除了主页，翻页后的主页也要获取商品列表
    def parse_bag(self, response):
        item = response.meta['item']
        # 使用普通 Python 字典（如 item = dict()）是一种更轻量级、更直接的方法
        item['update_name'] = "lu"  # 将值 "lu" 分配给键 'update_name'
        item["delete_brand"] = ["fabrikstyle", "sexy", "free", "SALE",
                                "Z Supply"]  # 筛选去掉产品标题和描述中的“fabrikstyle", "sexy", "free", "SALE", "Z Supply”一词
        item['origin_url_index'] = response.meta['origin_url_index']
        # item['html_str_index'] = response.meta['html_str_index']
        item["type_num"] = 3
        type_tuple = response.meta['type_tuple']
        collection = response.meta['collection']
        collection_handle = response.meta['collection_handle']
        page_data = response.json()
        product_list = page_data['products']
        print(f'----{type_tuple}----数据总量：{len(product_list)}')  # ----('Blouses',)----数据总量：24

        for ele in product_list:
            item["details"] = 'https://fabrikstyle.com/products/' + ele['handle']
            print(item["details"])

        total_products = page_data['total_product']
        print(f'大页商品数据总量：{total_products}')
        page = (int(total_products) // 24) + 1
        print(f'商品总页数：{page}')

        for p in range(2, page + 1):
            base_url = 'https://services.mybcapps.com/bc-sf-filter/filter?t={timestamp}&_=pf&shop=fabrik-style.myshopify.com&page={page}&limit=24&sort=relevance&locale=en&event_type=collection&build_filter_tree=true&sid=d1879230-b692-4693-9586-ce85fca2e98c&pg=collection_page&zero_options=true&product_available=true&variant_available=true&sort_first=available&urlScheme=2&collection_scope={collection}&collectionId={collection}&handle={collection_handle}'
            url = base_url.format(timestamp=str(int(round(time.time() * 1000))), page=p, collection=collection, collection_handle=collection_handle)
            yield scrapy.Request(url=url, callback=self.parse_bag,
                                 meta={"type_tuple": type_tuple, 'origin_url_index': item['origin_url_index']
                                       })
            print(f'正在爬取第{p}页数据包：{url}')

            # cookies_str = 'secure_customer_sig=; localization=US; cart_currency=USD; _y=3169e62b-90f2-46e3-b096-3f05ed5b2563; _shopify_y=3169e62b-90f2-46e3-b096-3f05ed5b2563; __attentive_id=e83494b5daa946379cf4b7e4b70cb215; _attn_=eyJ1Ijoie1wiY29cIjoxNjg4NjA4OTIwNjczLFwidW9cIjoxNjg4NjA4OTIwNjczLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImU4MzQ5NGI1ZGFhOTQ2Mzc5Y2Y0YjdlNGI3MGNiMjE1XCJ9In0=; __attentive_cco=1688608920674; _fbp=fb.1.1688692311731.1229665160; _pin_unauth=dWlkPVpXTXlNR05pTURJdE1HWmpOQzAwTkdNeExUbGhaRGt0TkRjNVptUTRZekpqTXpkaA; _orig_referrer=https%3A%2F%2Ffabrikstyle.com%2Fproducts%2Fclara-printed-mini-dress; _landing_page=%2Frecommendations%2Fproducts%3Fsection_id%3Dtemplate--14584073289786__recommendations%26limit%3D3%26product_id%3D7046447038522; _gid=GA1.2.51925846.1690348930; __attentive_dv=1; _ce.clock_event=1; _ce.clock_data=2121%2C84.17.41.94%2C1%2C15c2f6f9416d00cec8b4f729460293c0; __attentive_vf=true; __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE2ODg2MDg5MTksInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vZmFicmlrc3R5bGUuY29tL2NvbGxlY3Rpb25zL2RyZXNzZXMifSwiJGxhc3RfcmVmZXJyZXIiOnsidHMiOjE2OTA1MDUzNTQsInZhbHVlIjoiaHR0cHM6Ly9mYWJyaWtzdHlsZS5jb20vY29sbGVjdGlvbnMvZHJlc3NlcyIsImZpcnN0X3BhZ2UiOiJodHRwczovL2ZhYnJpa3N0eWxlLmNvbS9wcm9kdWN0cy9sYXVyYS1zbW9ja2VkLWJpYi1taW5pLWRyZXNzIn19; _ga=GA1.2.601203676.1688608917; cebs=1; _ce.s=v~bf4e8268fb29779180222bc141ca8277d74e0ebc~lcw~1690505357734~vpv~23~v11ls~5acf7970-1bae-11ee-974e-3b976002796d~ir~1~v11.rlc~1690505357742~v11slnt~1690364931790~gtrk.la~lkkycf08~lcw~1690505357742; cebsp_=4; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22US%22%2C%22sale_of_data_region%22%3Afalse%7D; keep_alive=d9eb8a8f-2716-47c3-9ebd-1cb4713a7f4d; _s=57023b29-e02b-4d34-ba0e-15e70f1618aa; _shopify_s=57023b29-e02b-4d34-ba0e-15e70f1618aa; _ga_8KDE0QBNN0=GS1.1.1690510848.59.0.1690510848.0.0.0; _shopify_sa_t=2023-07-28T02%3A20%3A51.611Z; _shopify_sa_p='
            # cookies_list = cookies_str.split("; ") # cookies_dict = {}
            # for cookie in cookies_list:
            #     name, value = cookie.split("=", 1)  #     cookies_dict[name] = value

        for product in product_list:
            product_title = product.get('title')
            print(f'product_title:{product_title}')

            flag = False

            for brand in self.Filter_brand:
                # 通过忽略大小写的正则，从product_title中匹配到所有包含brand内容的数据
                if re.findall(brand, product_title, re.IGNORECASE):
                    # 修改标志变量，退出循环
                    flag = True
                    break
            if flag:
                return

            if not product_title:
                return

            item["product_title"] = ' '.join(product_title.split(' ')[1:])  # 即从第二个元素开始取
            item["handle"] = product.get('handle')  # clara-printed-mini-dress
            original_price = product.get('price_max')  # 7400
            item["original_price"] = original_price
            item["Product_price"] = item["special_price"] = item["original_price"]
            # description结构复杂，用响应的xpath路径，而非js，可以避免转义字符、空白、编码等问题
            item["description"] = product.get('body_html')
            # # 去掉所有产品描述的第一大段
            # item["description"] = item["description"][1:]

            for ele in item["description"]:
                # 去掉产品描述中“Please note, this item is final sale”句段
                if 'Please note, this item is final sale' in ele:
                    item["description"] = item["description"].replace(ele, '')
            # 用process_cleaned_data对description进行清洗
            item["description"] = process_cleaned_data(item['description']).replace('\n', '') if item['description'] else ''
            print(f'description:{item["description"]}')

            # item["pd_img_list"] = [response.urljoin(ele[" src"]) for ele in
            #                        BeautifulSoup(item['description'], "lxml").find_all('img')]  现在description里已经没有img标签了

            # item["other_image_urls"] = product_data['images']
            # item["other_image_urls"] = ['https:' + ele.split('?')[0] for ele in item["other_image_urls"]]

            product_image_urls = product.get('images', [])  # images中保存了商品的所有图片链接，清洗后进行保存
            item["image_urls"] = [value for key, value in product_image_urls.items() if key.isdigit()]
            print(f'image_urls:{item["image_urls"]}')

            item["option"] = list()  # 此时是个空列表，后续会变成option: ['Colors', 'Size']
            item["att_val_img"] = list()  # 属性值
            group_dict = dict()  # 建立一个空字典group_dict
            have_color_type_name = ''
            # 目标：option': ['Colors', 'Size']
            products_list = product.get('options_with_values')
            if len(products_list) == 1 and products_list[0] == 'Title':
                products_list = []

            if products_list:
                for index, one_option in enumerate(products_list):
                    type_name = one_option
                    print(f'type_name:{type_name}')
                    print(f'products_list:{products_list}')
                    if not type_name:
                        continue  # 跳过options为空的情况
                    type_name = type_name.get('name')
                    if type_name == 'Color':
                        type_name = 'Colors'
                    if type_name not in item["option"]:
                        item["option"].append(type_name)  # 给item["option"]添加数据 目标：option': ['Colors', 'Size']
                        print(f'option:"{item["option"]}')
                        # .index() 是列表对象的方法调用，搜索列表中第一次出现的元素type_name，如果找到，返回元素在列表中的索引值
                        type_name_index = item["option"].index(type_name)
                        print(f'type_name_index:{type_name_index}')  # check index right
                        item[f"option{type_name_index + 1}_list"] = list()
                        print(f'option{type_name_index + 1}_list:{item[f"option{type_name_index + 1}_list"]}') #check option_list right

                    type_name_index = item["option"].index(type_name)  # 已有对象，执行相同操作获得索引
                    print(f'type_name_index:{type_name_index}')
                    # 目标为option1_list': ['white dustblue'], 'option2_list': ['xs', 's', 'm', 'l', 'xl'],
                    item[f"option{index + 1}_list"] = list()
                    print(f'option{type_name_index + 1}_list:{item[f"option{type_name_index + 1}_list"]}')
                    # 进入不同尺码进行处理
                    for e in product.get('variants'):
                        types1 = e.get('merged_options')[0]  # types1 = e[option(1)] = MULTI
                        print(f'types1:{types1}')
                        # types1 = types1.replace('-', ' ').replace('|', ' ').replace(':', ' ').replace('\n', ' ').replace(
                        #     ',',
                        #     ' ').replace(
                        #     '=', ' ').strip()

                        if types1 not in item[f"option{type_name_index + 1}_list"]:
                            item[f"option{type_name_index + 1}_list"].append(types1)
                            print(f'option{type_name_index + 1}_list:{item[f"option{type_name_index + 1}_list"]}')
                            #  'option1_list': ['white dustblue'],
                            #  'option2_list': ['xs', 's', 'm', 'l', 'xl'],

                            types2 = "0"  # 初始化变量types2为0 逻辑是如果图像有颜色url，types2就为url，没有就为0
                            if type_name == 'Colors':
                                types_img = ''  # 初始化变量types_img为空字符串
                                # 如果有featured_image就获取图片下载路径
                                if e.get('featured_image'):
                                    types_img = e['featured_image']['src']  # featured_image: null

                                if types_img:
                                    # 通过将“/50x50/”替换为“/670x890/”来修改 URL 路径。 会获得更高分辨率版本的图像
                                    types2 = response.urljoin(types_img.replace('/50x50/', '/670x890/'))
                                    have_color_type_name = type_name  # have_color_type_name = Colors
                                    group_dict[types1] = types2  # group_dic = {types1: types2} = {MULTI: url}

                            types = "|".join([type_name + ":" + types1 + "-10000-1-0-0-0-0", types2])
                            # ['Colors:white dustblue-10000-1-0-0-0-0|0','Size:xs-10000-1-0-0-0-0|0']
                            item["att_val_img"].append(types)  # 将types添加进att_val_img
                            print(f'att_val_img:{item["att_val_img"]}')

            if have_color_type_name:
                # 处理完所有数据后，如果变量 `have_color_type_name` 有值（即如果在处理过程中遇到 'Colors'）
                # 则会创建以 `have_color_type_name` 为键的字典 , `group_dict` 作为值
                item["option_image_urls_dict"] = {have_color_type_name: group_dict}  # {Colors: {MULTI: url}}

            item['quantity'] = str(random.randint(100, 999))  # 库存用三位数随机
            print(item)
            # yield item 为什么要注释？

    # def parse_details(self, response):
    #     item = response.meta["item"]
    #     # re.findall匹配得到的是一个列表，通过索引拿到json格式的产品数据
    #     # product_data = json.loads(product_data[0])
    #     # # item["SKU"] = str(response.xpath('//div[@class="sku"]/text()').extract_first().split(':')[-1].strip())
    #     # product_title = product_data[0]['title']
    #     # print(product_title)
    #     flag = False
    #
    #     for brand in self.Filter_brand:
    #         # 通过忽略大小写的正则，从product_title中匹配到所有包含brand内容的数据
    #         if re.findall(brand, product_title, re.IGNORECASE):
    #             # 修改标志变量，退出循环
    #             flag = True
    #             break
    #     # 只有 flag = False 才能执行后面的代码
    #     if flag:
    #         return
    #
    #     if not product_title:
    #         return
    #     # 去掉所有产品第一个单词
    #     item["product_title"] = ' '.join(product_title.split(' ')[1:]) # 即从第二个元素开始取
    #     item["handle"] = product_data['handle'] # clara-printed-mini-dress
    #
    #     original_price = product_data['price'] # 7400
    #     item["original_price"] = original_price / 100
    #     item["Product_price"] = item["special_price"] = item["original_price"]
    #     # description结构复杂，用响应的xpath路径，而非js，可以避免转义字符、空白、编码等问题
    #     item["description"] = response.xpath('//div[@id="tab1"]').extract_first()
    #     # 去掉所有产品描述的第一大段
    #     p_desc = response.xpath('//div[@id="tab1"]/p[1]').extract_first()
    #     item["description"] = item["description"].replace(p_desc,'')
    #
    #     for ele in response.xpath('//div[@id="tab1"]/p').extract():
    #         # 去掉产品描述中“Please note, this item is final sale”句段
    #         if 'Please note, this item is final sale' in ele:
    #             item["description"] = item["description"].replace(ele, '')
    #     # 用process_cleaned_data对description进行清洗
    #     item["description"] = process_cleaned_data(item['description']).replace('\n', '') if item['description'] else ''
    #
    #     # item["pd_img_list"] = [response.urljoin(ele[" src"]) for ele in
    #     #                        BeautifulSoup(item['description'], "lxml").find_all('img')]  现在description里已经没有img标签了
    #
    #     # item["other_image_urls"] = product_data['images']
    #     # item["other_image_urls"] = ['https:' + ele.split('?')[0] for ele in item["other_image_urls"]]
    #
    #     item["image_urls"] = product_data['images'] # images中保存了商品的所有图片链接，清洗后进行保存
    #     # 去掉?后面的参数，以免利用图片名字保存图片路径时报错
    #     item["image_urls"] = ['https:' + ele.split('?')[0] for ele in item["image_urls"]]
    #
    #     item["option"] = list() # 此时是个空列表，后续会变成option: ['Colors', 'Size']
    #     item["att_val_img"] = list() # 属性值
    #     group_dict = dict() # 建立一个空字典group_dict
    #     have_color_type_name = ''
    #
    #     products_list = product_data['options'] # ["Color", "Size"]
    #     if len(products_list) == 1 and products_list[0] == 'Title':
    #         products_list = []
    #
    #     # 逻辑是把json数据中大的options提取出来变成导出数据中的option
    #     # 并获取每项数据的参数值，+1，作为后面optionx命名的基数
    #     # 把variants小字典中的options/option1提出来添加到option1_list、option2_list列表中
    #     if products_list:
    #         # 此时products_list为 ["Color", "Size"]，one_option_xpath为"Color", "Size"
    #         for index, one_option_xpath in enumerate(products_list):
    #             type_name = one_option_xpath # type_name = ["Color", "Size"]
    #             if not type_name:
    #                 continue # 跳过options为空的情况
    #             # 清洗type_name
    #             type_name = type_name.split("_")[0].replace('-', ' ').replace('|', ' ').replace(':',
    #                                                                                             '').replace('Choose a',
    #                                                                                                         '').strip().capitalize()
    #             if type_name == 'Color':
    #                 type_name = 'Colors' # 将Color变成Colors
    #             # 此时products_list为 ["Colors", "Size"]
    #             # option之前声明为空列表
    #             if type_name not in item["option"]:
    #                 # 给新的列表item["option"]添加数据
    #                 item["option"].append(type_name) # option: ['Colors', 'Size']
    #                 # .index() 是列表对象的方法调用，搜索列表中第一次出现的元素type_name，如果找到，返回元素在列表中的索引值
    #                 type_name_index = item["option"].index(type_name)
    #                 # 将空列表赋值给对应选项的键，以便后续填充该选项的值。
    #                 item[f"option{type_name_index + 1}_list"] = list()
    #                 # 后续为option1_list': ['white dustblue'], 'option2_list': ['xs', 's', 'm', 'l', 'xl'],
    #             # option列表中的已有对象，执行相同操作获得索引
    #             type_name_index = item["option"].index(type_name)
    #             # 将空列表赋值给当前循环索引（index）加1后作为键，也是为了后续填充该选项的值
    #             item[f"option{index + 1}_list"] = list() # 拿type_name_index是用来+1，获得option1_list键名
    #             # 进入不同尺码进行处理
    #             for e in product_data['variants']:
    #                 # e是一个大字典，利用dic[key]拿到value
    #                 types1 = e[f'option{(index + 1)}'] # types1 = e[option(1)] = MULTI
    #                 types1 = types1.replace('-', ' ').replace('|', ' ').replace(':', ' ').replace('\n', ' ').replace(
    #                     ',',
    #                     ' ').replace(
    #                     '=', ' ').strip()
    #                 # item[option1_list]初始化为空列表， 往中添加数据
    #                 if types1 not in item[f"option{type_name_index + 1}_list"]: # item[option1_list]
    #                     item[f"option{type_name_index + 1}_list"].append(types1) # option1_list': ['white dustblue']
    #
    #                     types2 = "0" # 初始化变量types2为0 逻辑是如果图像有颜色url，types2就为url，没有就为0
    #                     if type_name == 'Colors':
    #                         types_img = '' # 初始化变量types_img为空字符串
    #                         # 如果有featured_image就获取图片下载路径
    #                         if e.get('featured_image'):
    #                             types_img = e['featured_image']['src'] # featured_image: null
    #
    #                         if types_img:
    #                             # 通过将“/50x50/”替换为“/670x890/”来修改 URL 路径。 会获得更高分辨率版本的图像
    #                             types2 = response.urljoin(types_img.replace('/50x50/', '/670x890/'))
    #                             have_color_type_name = type_name # have_color_type_name = Colors
    #                             group_dict[types1] = types2  # group_dic = {types1: types2} = {MULTI: url}
    #
    #                     types = "|".join([type_name + ":" + types1 + "-10000-1-0-0-0-0", types2])
    #                     # ['Colors:white dustblue-10000-1-0-0-0-0|0','Size:xs-10000-1-0-0-0-0|0']
    #                     item["att_val_img"].append(types) # 将types添加进att_val_img
    #
    #     if have_color_type_name:
    #         # 处理完所有数据后，如果变量 `have_color_type_name` 有值（即如果在处理过程中遇到 'Colors'）
    #         # 则会创建以 `have_color_type_name` 为键的字典 , `group_dict` 作为值
    #         item["option_image_urls_dict"] = {have_color_type_name: group_dict} # {Colors: {MULTI: url}}
    #
    #     item['quantity'] = str(random.randint(100, 999)) # 库存用三位数随机
    #     print(item)
    #     # yield item 为什么要注释？


if __name__ == '__main__':
    cp = CrawlerProcess(get_project_settings())
    cp.crawl(Fab_pageSpider)
    cp.start()
