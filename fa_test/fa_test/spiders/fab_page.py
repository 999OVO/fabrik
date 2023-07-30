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
IS_Current = __name__ != "__main__"
import scrapy
from scrapy import Request, Spider
from bs4 import BeautifulSoup
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
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode


class Fab_pageSpider(scrapy.Spider):
    name = 'Fab_page'

    type_list = """<ul class="nav site-nav  site-nav--center"><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/new-arrivals?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">NEW!<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-arrivals?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All New</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Bottoms</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-accessories?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Accessories</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/spring-lookbook?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Featured</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/recruitment-ready?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rush Ready</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/summer-lookbook?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Summer Lookbook</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/vacation-ready?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Vacation Ready</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/little-white-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Little White Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/bold-brights?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Punch of Color</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Trending</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/best-dressed-guest?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Perfect Plus One</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/coastal-cowgirl?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Coastal Cowgirl</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/printed-to-perfection?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:Printed to Perfection</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/high-contrast?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Trending:High Contrast</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--smalldropdown"><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Clothing<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown  js-mobile-menu-dropdown small-dropdown"><ul class="small-dropdown__container"><li class="small-dropdown__item "><a href="https://fabrikstyle.com/collections/clothes?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Clothes</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/best-sellers?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Best Sellers</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Dresses</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Tops</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rompers+Jumpsuits</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/pants?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Pants+Leggings</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/skirts-shorts?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Skirts+Shorts</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/matching-sets?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Matching Sets</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/denim?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Denim</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sweaters+Sweatshirts</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/jackets-coats?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Jackets+Coats</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/spanx?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Spanx</a></li><li class="small-dropdown__subitem"><a href="/products/gift-card"class="site-nav__link site-nav__dropdown-link">Gift Cards</a></li></ul></div></li></ul></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Dresses<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">New Dresses</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/midi-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Midi</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/mini-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Mini</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/maxi-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Maxi</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Rompers&amp;Jumpsuits</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY OCCASION</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1&amp;occasion=Cocktail,Party"class="site-nav__link site-nav__dropdown-link">Party&amp;Cocktail Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/casual-dresses-1?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Casual Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/dresses?filter.v.availability=1&amp;limit=30&amp;occasion=Printed"class="site-nav__link site-nav__dropdown-link">Printed Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/little-white-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Little White Dresses</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item"><a href="https://fabrikstyle.com/collections/rompers-jumpsuits?filter.v.availability=1"class="site-nav__link">Rompers&amp;Jumpsuits</a></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Tops<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Tops</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/new-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">New Tops</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/blouses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Blouses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/cropped-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Cropped Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tees-basics-1?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">T-Shirts&amp;Basics</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/tanks-camis?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Tanks&amp;Bodysuits</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sweaters</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">TRENDING</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/going-out-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Going Out Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/workwear-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Workwear Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/printed-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Printed Tops</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/bottoms?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Bottoms<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/new-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">New Bottoms</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">BY STYLE</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/pants?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Pants</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/denim?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Denim</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/shorts-skirts?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Shorts+Skirts</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/spanx?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">SPANX</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item"><a href="https://fabrikstyle.com/collections/shoes?filter.v.availability=1"class="site-nav__link">Shoes</a></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--smalldropdown"><a href="https://fabrikstyle.com/collections/accessories?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Accessories<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown  js-mobile-menu-dropdown small-dropdown"><ul class="small-dropdown__container"><li class="small-dropdown__item "><a href="https://fabrikstyle.com/collections/accessories?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Accessories</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/jewelry?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Jewelry</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/hats-scarves?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Hats&amp;Scarves</a></li><li class="small-dropdown__subitem"><a href="https://fabrikstyle.com/collections/bags?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Bags&amp;Sunglasses</a></li></ul></div></li></ul></div></li><li class="site-nav__item site-nav__item--has-dropdown site-nav__item--megadropdown"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link"aria-haspopup="true"aria-expanded="false">Sale<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown js-mobile-menu-dropdown mega-dropdown container"><div class="page-width"><ul class="mega-dropdown__container grid grid--uniform"><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">Shop All Sale</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-dresses?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Dresses</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-tops?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Tops</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-bottoms?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Bottoms</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale-sweaters?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Sale Sweaters</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/final-few?filter.v.availability=1"class="site-nav__link site-nav__dropdown-link">Final Few</a></li></ul></div></li><li class="mega-dropdown__item grid__item one-quarter "><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1"class="site-nav__link site-nav__dropdown-heading">By Price</a><div class="site-nav__submenu"><ul class="site-nav__submenu-container"><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A20"class="site-nav__link site-nav__dropdown-link">Under $20</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A30"class="site-nav__link site-nav__dropdown-link">Under $30</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A40"class="site-nav__link site-nav__dropdown-link">Under $40</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A50"class="site-nav__link site-nav__dropdown-link">Under $50</a></li><li class="mega-dropdown__subitem"><a href="https://fabrikstyle.com/collections/sale?filter.v.availability=1&amp;limit=30&amp;price=5%3A60"class="site-nav__link site-nav__dropdown-link">Under $60</a></li></ul></div></li></ul></div></div></li><li class="site-nav__item site-nav__more-links more-links site-nav__invisible site-nav__item--has-dropdown"><a href="#"class="site-nav__link"aria-haspopup="true"aria-expanded="false">More links<span class="feather-icon site-nav__icon"><svg aria-hidden="true"focusable="false"role="presentation"class="icon feather-icon feather-chevron-down"viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg></span></a><div class="site-nav__dropdown small-dropdown more-links-dropdown"><div class="page-width relative"><ul class="small-dropdown__container"></ul><div class="more-links__dropdown-container"></div></div></div></li></ul>
        """

    all_new_classify_list = []
    all_tuple_classify_first_url = []

    html_etree = etree.HTML(type_list)
    first_categories = html_etree.xpath('//ul[@class="nav site-nav  site-nav--center"]/li/a/text()')[:-1]
    first_categories_urls = html_etree.xpath('//ul[@class="nav site-nav  site-nav--center"]/li/a/@href')[:-1]
    # zip同时迭代多个序列
    for category, url in zip(first_categories, first_categories_urls):
        url = url.replace('?filter.v.availability=1', '')
        all_tuple_classify_first_url.append(url)
        all_new_classify_list.append((category,))

    new_csv_classify_dict = dict(zip(all_tuple_classify_first_url, all_new_classify_list))
    print(new_csv_classify_dict)

    # start_urls = ['https://fabrikstyle.com/collections/new-arrivals', 'https://fabrikstyle.com/collections/clothes',
    #               'https://fabrikstyle.com/collections/dresses', 'https://fabrikstyle.com/collections/rompers-jumpsuits',
    #               'https://fabrikstyle.com/collections/tops', 'https://fabrikstyle.com/collections/bottoms',
    #               'https://fabrikstyle.com/collections/shoes', 'https://fabrikstyle.com/collections/accessories',
    #               'https://fabrikstyle.com/collections/sale']


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

    def start_requests(self):
        for origin_url, type_tuple in self.new_csv_classify_dict.items():
            print(f"Sending request for URL: {origin_url}, Type Tuple: {type_tuple}")
            yield scrapy.Request(url=origin_url, callback=self.parse_category,
                                 meta={'type_tuple': type_tuple,
                                       'visited_pages': set()
                                       })

    def parse_category(self, response):
        type_tuple = response.meta['type_tuple']
        visited_pages = response.meta['visited_pages']

        collection_scope = re.findall(r'collection:\s*\{[^}]*id:\s*([^,\n]+)', response.text)[0]
        collection_handle = re.findall(r"collection:\s*\{[^}]*handle:\s*'([^,\n]+)'", response.text)[0]

        collection_scope_list = []
        collection_handle_list = []

        collection_scope_list.append(collection_scope)
        collection_handle_list.append(collection_handle)
        print(f'collection_scope_list:{collection_scope_list}')
        print(f'collection_handle_list:{collection_handle_list}')

        for scope, handle in zip(collection_scope_list, collection_handle_list):
            first_page_url = self.get_collection_url(scope, handle, page=1)

            yield scrapy.Request(url=first_page_url,
                                 callback=self.require_bag,
                                 meta={
                                     'collection_list': collection_scope_list,
                                     'collection_handle_list': collection_handle_list,
                                     'type_tuple': type_tuple,
                                     'visited_pages': visited_pages
                                 })

    def require_bag(self, response):
        type_tuple = response.meta['type_tuple']
        collection_list = response.meta['collection_list']
        collection_handle_list = response.meta['collection_handle_list']
        visited_pages = response.meta['visited_pages']
        page_data = response.json()

        total_pages = (int(page_data['total_product']) // 24) + 1
        print(f'{type_tuple},total_pages:{total_pages}')

        total_pages_list = []
        total_pages_list.append(total_pages)

        for scope, handle, total_pages in zip(collection_list, collection_handle_list, total_pages_list):
            for page in range(1, total_pages + 1):
                page_url = self.get_collection_url(scope, handle, page=page)
                if page_url not in response.meta['visited_pages']:
                    visited_pages.add(page_url)
                    print(f'正在爬取{scope}中的页数: {page_url}')
                    yield scrapy.Request(
                        url=page_url,
                        callback=self.parse,
                        meta={"type_tuple": type_tuple, 'page': page,
                              'visited_pages': visited_pages.copy()}
                    )

    def parse(self, response, **kwargs):
        type_tuple = response.meta['type_tuple']
        page_data = response.json()
        product_list = page_data['products']
        print(f'----{type_tuple}----本页数据总量：{len(product_list)}')

        for ele in product_list:
            item = dict()
            item["details"] = 'https://fabrikstyle.com/products/' + ele['handle']
            # print(item["details"])

            item["product_title"] = ' '.join(ele.get('title').split(' ')[1:]).replace('-', '')  # 即从第二个元素开始取
            # print(item["product_title"])

            item["handle"] = ele.get('handle')  # clara-printed-mini-dress
            item["original_price"] = float(ele.get('price_max', 0))
            item["Product_price"] = item["special_price"] = item["original_price"]
            item["description"] = ele.get('body_html')
            # # 去掉所有产品描述的第一大段
            # item["description"] = item["description"][1:]

            for e in item["description"]:
                # 去掉产品描述中“Please note, this item is final sale”句段
                if 'Please note, this item is final sale' in e:
                    item["description"] = item["description"].replace(e, '')
            item["description"] = process_cleaned_data(item['description']).replace('\n', '') if item[
                'description'] else ''
            # print(f'description:{item["description"]}')

            product_image_urls = ele.get('images', [])  # images中保存了商品的所有图片链接，清洗后进行保存
            item["image_urls"] = [value for key, value in product_image_urls.items() if key.isdigit()]
            # print(f'image_urls:{item["image_urls"]}')

            item['option'] = [option['name'].capitalize() + ('s' if option['name'] == 'color' else '') for option in
                              ele.get('options_with_values', [])]
            item['att_val_img'] = [
                f"{option['name'].capitalize() + ('s' if option['name'] == 'color' else '')}:{value['title']}-10000-1-0-0-0-0|0"
                for option in ele.get('options_with_values', [])
                for value in option.get('values', [])
            ]

            # Add other necessary information (based on the provided data)
            item['html_str_index'] = 0
            item['option1_list'] = [value['title'] for value in
                                    ele.get('options_with_values', [])[0].get('values', [])]
            # item['option2_list'] = [value['title'] for value in
            #                         ele.get('options_with_values', [])[1].get('values', [])]
            item['option2_list'] = [value['title'] for value in
                                    ele.get('options_with_values', [])[1].get('values', []) if
                                    ele.get('options_with_values', [])[1]]

            item['origin_url_index'] = 1
            item['type_num'] = 3
            item['update_name'] = 'luo'
            item['quantity'] = str(random.randint(100, 999))  # 库存用三位数随机

            yield item

    def get_collection_url(self, collection, collection_handle, page):
        base_url = 'https://services.mybcapps.com/bc-sf-filter/filter'
        query_params = {
            't': str(int(round(time.time() * 1000))),
            '_': 'pf',
            'shop': 'fabrik-style.myshopify.com',
            'page': page,
            'limit': 24,
            'sort': 'relevance',
            'locale': 'en',
            'event_type': 'collection',
            'build_filter_tree': 'true',
            'sid': 'd1879230-b692-4693-9586-ce85fca2e98c',
            'pg': 'collection_page',
            'zero_options': 'true',
            'product_available': 'true',
            'variant_available': 'true',
            'sort_first': 'available',
            'urlScheme': 2,
            'collection_scope': collection,
            'collectionId': collection,
            'handle': collection_handle,
        }
        return f"{base_url}?{urlencode(query_params)}"


if __name__ == '__main__':
    cp = CrawlerProcess(get_project_settings())
    cp.crawl(Fab_pageSpider)
    cp.start()
