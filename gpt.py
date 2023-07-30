

class Fab_pageSpider(scrapy.Spider):
    name = 'Fab_page'

    type_list = """..."""

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
    print(all_tuple_classify_first_url)
    print(new_csv_classify_dict)
    for origin_url_index, origin_url in enumerate(new_csv_classify_dict):
        type_tuple = new_csv_classify_dict[origin_url]
        print(f"type_tuple:{type_tuple}")

    start_urls = ['https://fabrikstyle.com/collections/new-arrivals', 'https://fabrikstyle.com/collections/clothes',
                  'https://fabrikstyle.com/collections/dresses', 'https://fabrikstyle.com/collections/rompers-jumpsuits',
                  'https://fabrikstyle.com/collections/tops', 'https://fabrikstyle.com/collections/bottoms',
                  'https://fabrikstyle.com/collections/shoes', 'https://fabrikstyle.com/collections/accessories',
                  'https://fabrikstyle.com/collections/sale']



    # 声明标题中不需要的内容为Filter_brand
    Filter_brand = [
        "LOURDES PRINTED PUFF SLEEVE SWEATER",
        "SALE - Z SUPPLY MODERN WEEKENDER",
        "Venetia Gauze Pant - OFF WHITE",
        "Fab'rik"
    ]

    def start_requests(self):

        for index, start_url in enumerate(self.start_urls):
            yield scrapy.Request(url=start_url, callback=self.parse_category,
                                 meta={'origin_url_index': index})

    def parse_category(self, response):
        index = response.meta['origin_url_index']

        collection_scope = re.findall(r'collection:\s*\{[^}]*id:\s*([^,\n]+)', response.text)[0]
        collection_handle = re.findall(r"collection:\s*\{[^}]*handle:\s*'([^,\n]+)'", response.text)[0]


        page = 1
        yield scrapy.Request(url=self.get_collection_url(collection_scope, collection_handle, page),
                             callback=self.parse_bag,
                             meta={
                                 'origin_url_index': index,
                                 'collection': collection_scope,
                                 'collection_handle': collection_handle,
                                 'type_tuple': type_tuple
                             })

    def parse_bag(self, response):
        item = dict()
        item["delete_brand"] = ["fabrikstyle", "sexy", "free", "SALE",
                                "Z Supply"]  # 筛选去掉产品标题和描述中的“fabrikstyle", "sexy", "free", "SALE", "Z Supply”一词
        item['origin_url_index'] = response.meta['origin_url_index']
        # type_tuple = response.meta['type_tuple']
        collection = response.meta['collection']
        collection_handle = response.meta['collection_handle']
        page_data = response.json()
        product_list = page_data['products']
        print(f'----{type_tuple}----数据总量：{len(product_list)}')  # ----('Blouses',)----数据总量：24

        for ele in product_list:
            item["details"] = 'https://fabrikstyle.com/products/' + ele['handle']
            # print(item["details"])

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

            item["product_title"] = ' '.join(product_title.split(' ')[1:]).replace('-','')  # 即从第二个元素开始取
            item["handle"] = product.get('handle')  # clara-printed-mini-dress
            item["original_price"] = float(product.get('price_max', 0))
            item["Product_price"] = item["special_price"] = item["original_price"]
            item["description"] = product.get('body_html')
            # # 去掉所有产品描述的第一大段
            # item["description"] = item["description"][1:]

            for ele in item["description"]:
                # 去掉产品描述中“Please note, this item is final sale”句段
                if 'Please note, this item is final sale' in ele:
                    item["description"] = item["description"].replace(ele, '')
            item["description"] = process_cleaned_data(item['description']).replace('\n', '') if item['description'] else ''
            print(f'description:{item["description"]}')

            product_image_urls = product.get('images', [])  # images中保存了商品的所有图片链接，清洗后进行保存
            item["image_urls"] = [value for key, value in product_image_urls.items() if key.isdigit()]
            print(f'image_urls:{item["image_urls"]}')

            item['option'] = [option['name'].capitalize() + ('s' if option['name'] == 'color' else '') for option in
                              product.get('options_with_values', [])]
            item['att_val_img'] = [
                f"{option['name'].capitalize() + ('s' if option['name'] == 'color' else '')}:{value['title']}-10000-1-0-0-0-0|0"
                for option in product.get('options_with_values', [])
                for value in option.get('values', [])
            ]

            # Add other necessary information (based on the provided data)
            item['html_str_index'] = 0
            item['option1_list'] = [value['title'] for value in
                                    product.get('options_with_values', [])[0].get('values', [])]
            item['option2_list'] = [value['title'] for value in
                                    product.get('options_with_values', [])[1].get('values', [])]
            item['origin_url_index'] = 1
            item['type_num'] = 3
            item['update_name'] = 'luo'
            item['quantity'] = str(random.randint(100, 999))  # 库存用三位数随机

            current_page = int(findall(r'page=(\d+)', response.url)[0])
            total_pages = (int(page_data['total_product']) // 24) + 1

            if current_page < total_pages:
                next_page = current_page + 1
                yield scrapy.Request(url=self.get_collection_url(collection, collection_handle, next_page),
                                     callback=self.parse_bag,
                                     meta={"type_tuple": type_tuple, 'origin_url_index': item['origin_url_index'],
                                           'item': item, 'collection': collection,
                                           'collection_handle': collection_handle,
                                           }
                                     )
                print(f'正在爬取第{next_page}页数据包：{url}')
            # print(item)
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
