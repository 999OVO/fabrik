import sys
sys.path.append(r'D:\study-nn\nn\project\fab_test')
# sys.path.append('../../HtmlCleaners.py')
import scrapy
import re
import random
import json
import time
import pprint
from lxml import etree
from copy import deepcopy
from scrapy.http import HtmlResponse
from HtmlCleaners import process_cleaned_data
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from fake_useragent import UserAgent
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
from fa_test.items import FaTestItem


class FTestSpider(scrapy.Spider):
    name = 'f_test'
    allowed_domains = ['fabrikstyle.com']
    start_urls = [
        """<ul class="nav site-nav  site-nav--center"><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/new-arrivals?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">NEW!<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-arrivals?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All New</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Bottoms</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-accessories?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Accessories</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/spring-lookbook?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Featured</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/recruitment-ready?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rush Ready</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/summer-lookbook?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Summer Lookbook</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/vacation-ready?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Vacation Ready</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/little-white-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Little White Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/bold-brights?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Punch of Color</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Trending</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/best-dressed-guest?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Perfect Plus One</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/coastal-cowgirl?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Coastal Cowgirl</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/printed-to-perfection?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Printed to Perfection</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/high-contrast?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:High Contrast</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--smalldropdown"><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Clothing<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown  js-mobile-menu-dropdown small-dropdown"><ul class="small-dropdown__container"><li class="small-dropdown__item "><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Clothes</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/best-sellers?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Best Sellers</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Dresses</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Tops</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rompers+Jumpsuits</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/pants?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Pants+Leggings</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/skirts-shorts?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Skirts+Shorts</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/matching-sets?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Matching Sets</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/denim?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Denim</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sweaters+Sweatshirts</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/jackets-coats?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Jackets+Coats</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/spanx?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Spanx</a></li><li class="small-dropdown__subitem"><a href="/products/gift-card"class="site-nav__link site-nav__dropdown-link">Gift Cards</a></li></ul></div></li></ul></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Dresses<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">New Dresses</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/midi-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Midi</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/mini-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Mini</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/maxi-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Maxi</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rompers&amp;Jumpsuits</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY OCCASION</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1&amp;occasion=Cocktail,Party"class="site-nav__link site-nav__dropdown-link">Party&amp;Cocktail Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/casual-dresses-1?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Casual Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1&amp;limit=30&amp;occasion=Printed"class="site-nav__link site-nav__dropdown-link">Printed Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/little-white-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Little White Dresses</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link">Rompers&amp;Jumpsuits</a></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Tops<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Tops</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Tops</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/blouses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Blouses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/cropped-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Cropped Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tees-basics-1?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">T-Shirts&amp;Basics</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tanks-camis?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Tanks&amp;Bodysuits</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sweaters</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">TRENDING</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/going-out-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Going Out Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/workwear-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Workwear Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/printed-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Printed Tops</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/bottoms?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Bottoms<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">New Bottoms</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/pants?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Pants</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/denim?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Denim</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/shorts-skirts?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Shorts+Skirts</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/spanx?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">SPANX</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item"><a href="https://fabrikstyle.com/collections/shoes?filter.v.availability=1"class="site-nav__link">Shoes</a></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--smalldropdown"><a href="https://fabrikstyle.com/collections/accessories?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Accessories<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown  js-mobile-menu-dropdown small-dropdown"><ul class="small-dropdown__container"><li class="small-dropdown__item "><a href="https://fabrikstyle.com/collections/accessories?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Accessories</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/jewelry?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Jewelry</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/hats-scarves?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Hats&amp;Scarves</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/bags?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Bags&amp;Sunglasses</a></li></ul></div></li></ul></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Sale<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Sale</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Bottoms</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Sweaters</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/final-few?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Final Few</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">By Price</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A20"class="site-nav__link site-nav__dropdown-link">Under $20</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A30"class="site-nav__link site-nav__dropdown-link">Under $30</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A40"class="site-nav__link site-nav__dropdown-link">Under $40</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A50"class="site-nav__link site-nav__dropdown-link">Under $50</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A60"class="site-nav__link site-nav__dropdown-link">Under $60</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__more-links more-links site-nav__invisible site-nav__item--has-dropdown"><a href="#"class="site-nav__link"aria-haspopup="true"aria-expanded="false">More links<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown small-dropdown more-links-dropdown"><div class="page-width relative"><ul class="small-dropdown__container"></ul><div class="more-links__dropdown-container"></div></div></div></li></ul>
    """
                     ]

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'fa_test.middlewares.MyUserAgentMiddleware': 100
        },
        "ITEM_PIPELINES":
            {
                'fa_test.pipelines.OthersImagesPipeline': 300,
                'fa_test.pipelines.Opencard_302s_Pipeline': 500,
            }
    }

    Filter_brand = [
        "LOURDES PRINTED PUFF SLEEVE SWEATER",
        "SALE - Z SUPPLY MODERN WEEKENDER",
        "Venetia Gauze Pant - OFF WHITE",
        "Fab'rik"
    ]

    def start_requests(self):
        # for page in range(1,9):
        collection_scope = [57115050042, 262358532154, 57116622906, 57118621754, 83666632762]
        base_url = 'https://services.mybcapps.com/bc-sf-filter/filter?t={timestamp}&_=pf&shop=fabrik-style.myshopify.com&page={page}&limit=24&sort=relevance&locale=en&event_type=collection&build_filter_tree=true&sid=2d79bf4e-fd7f-4415-9eba-38ee688374ff&pg=collection_page&zero_options=true&product_available=true&variant_available=true&sort_first=available&urlScheme=2&collection_scope={collection}'
        # base_url = 'https://services.mybcapps.com/bc-sf-filter/filter?t=1690165121517&_=pf&shop=fabrik-style.myshopify.com&page=1&limit=24&sort=relevance&locale=en&event_type=collection&build_filter_tree=true&sid=d1879230-b692-4693-9586-ce85fca2e98c&pg=collection_page&zero_options=true&product_available=true&variant_available=true&sort_first=available&urlScheme=2&collection_scope=57115050042&collectionId=57115050042&handle=dresses'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Referer': 'https://fabrikstyle.com/'
        }
        for collection in collection_scope:
            page = 1  # 默认初始页数为1
            count = 0  # 计数器变量

            while count < 8:  # 限制循环次数不超过8次
                url = base_url.format(timestamp=str(int(round(time.time() * 1000))), page=page, collection=collection)
                request = scrapy.Request(url=url, headers=headers)
                yield request

                count += 1  # 增加计数器
                page += 1  # 递增页数

    def parse(self, response, **kwargs):
        # 从源码中获取商品大页url，并组合成元组
        all_new_classify_list = []
        all_tuple_classify_first_url = []


        html_etree = etree.HTML(self.start_urls[0])
        first_categories = html_etree.xpath('//ul[@class="nav site-nav  site-nav--center"]/li/a/text()')
        first_categories_urls = html_etree.xpath('//ul[@class="nav site-nav  site-nav--center"]/li/a/@href')[:-1]
        # zip同时迭代多个序列
        for category, url in zip(first_categories, first_categories_urls):
            url = url.replace('?filter.v.availability=1', '')
            all_tuple_classify_first_url.append(url)
            all_new_classify_list.append((category,))

        # item = FaTestItem()
        item = ()
        # 将域名和分类字典化
        new_csv_classify_dict = dict(zip(all_tuple_classify_first_url, all_new_classify_list))
        print(new_csv_classify_dict)
        # 提取出类型元组，传给解析方法，做后续分类命名处理;同理，提取出url索引，供后面使用
        for origin_url_index, origin_url in enumerate(new_csv_classify_dict):
            type_tuple = new_csv_classify_dict[origin_url]
            print(f"type_tuple:{type_tuple}")

        item['origin_url_index'] = origin_url_index
        item['update_name'] = "luo"  # 将值 "lu" 分配给键 'update_name'
        # 筛选去掉产品标题和描述中的“fabrikstyle", "sexy", "free", "SALE", "Z Supply”一词
        item["delete_brand"] = ["fabrikstyle", "sexy", "free", "SALE", "Z Supply"]
        item["type_num"] = 3

        for one_type_index, one_type in enumerate(type_tuple, start=1):
            # 将值 one_type 分配给名为 'type_1' 的键 （或“type_2”、“type_3”等，具体取决于循环）
            item[f'type_{one_type_index}'] = one_type  # {type_1, ('Blouses',)}

# 获取大页元组后，开始处理，发送数据包请求后获得的响应
        json_str = response.text
        data = json.loads(json_str)
        products = data.get('products', [])
        print(f'----{type_tuple}----数据总量：{len(products[0])}')  # ----('Blouses',)----数据总量：24

        for product in products:
            # 提取产品信息
            # product_title = product.get('title')
            # product_price_max = product.get('price_max')
            # product_price_min = product.get('price_min')
            # product_type = product.get('product_type')
            # product_handle = product.get('handle')
            # product_image_urls = product.get('images', [])
            # product_images = [value for key, value in product_image_urls.items() if key.isdigit()]

            # product_images = [url for url in product_image_urls]

            # product_list = response.xpath('//*[@class="boost-sd__product-list boost-sd__product-list-grid--3-col boost-sd__product-list--margin"]/div') # 分析层级结构获取的xpath
            # product_list = re.findall(r'window.boostSDFallback = ([\s\S]*?)};', html_source)[0]
            # product_list = json.loads(product_list[0] + '}')['products']

            item['details'] = 'https://fabrikstyle.com/products/' + product['handle']
            # item['details'] = response.urljoin(ele.xpath('./@href'))
            yield scrapy.Request(url=item['details'], callback=self.parse_details,
                                 meta={'item': deepcopy(item)})

    def parse_details(self, response: HtmlResponse):
        item = response.meta['item']
        # 利用正则表达式从js代码中定位到产品数据
        product_data = re.findall(r'sgGlobalVars.currentProduct = ([\s\S]*?)};', response.text)
        pprint.pprint(product_data[0])
        product_data = json.loads(product_data[0] + '}')

        product_title = product_data['title']
        flag = False

        for brand in self.Filter_brand:
            if re.findall(brand, product_title, re.IGNORECASE):
                flag = True
                break
        if flag:
            return

        if not product_title:
            return

        item["product_title"] = ' '.join(product_title.split(" ")[-1:])
        item["description"] = response.xpath('//div[@id="tab1"]').extract_first()
        p_desc = response.xpath('//div[@id="tab1"]/p[1]').extract_first()
        item["description"] = item["description"].replace(p_desc, '')

        for ele in response.xpath('//div[@id="tab1"]/p').extract():
            if 'Please note, this item is final sale' in ele:
                item["description"] = item["description"].replace(ele, '')
        # 如果item字典中不存在该键，会引发“KeyError”，所以要用条件表达式捕获异常
        item["description"] = process_cleaned_data(item["description"]).replace('\n', '') if item["description"] else ''
        item["image_urls"] = product_data['images']
        item["image_urls"] = ['https:' + ele.split('?')[0] for ele in item["image_urls"]]

        item["option"] = list()
        item["att_val_img"] = list()
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
                    types1 = e[f'option{(index + 1)}']
                    types1 = types1.replace('-', ' ').replace('|', ' ').replace(':', ' ').replace('\n', ' ').replace(
                        ',',
                        ' ').replace(
                        '=', ' ').strip()

                    if types1 not in item[f"option{type_name_index + 1}_list"]:
                        item[f"option{type_name_index +1 }_list"].append(types1)

                        types2 = "0" # 初始化变量types2为0 逻辑是如果图像有颜色url，types2就为url，没有就为0
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


if __name__ == '__main__':
    cp = CrawlerProcess(get_project_settings())
    cp.crawl(FTestSpider)
    cp.start()








