# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FaTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SKU = scrapy.Field()  # 产品sku
    product_title = scrapy.Field()  # 产品标题
    categories_name = scrapy.Field()  # 分类 （多级分类使用';'分开）
    original_price = scrapy.Field()  # 产品原价
    special_price = scrapy.Field()  # 产品特价
    description = scrapy.Field()  # 产品描述
    product_Color = scrapy.Field()  # 产品颜色
    product_Size = scrapy.Field()  # 产品尺寸
    product_Style = scrapy.Field()  # 产品风格
    image_urls = scrapy.Field()  # 主要图
    other_image_urls = scrapy.Field()  # 次要图 （多个图片使用';'分开)

    origin_url_index = scrapy.Field()
    update_name = scrapy.Field()
    delete_brand = scrapy.Field()
    type_num = scrapy.Field()
    details = scrapy.Field()
    type_1 = scrapy.Field()
    option = scrapy.Field()
    att_val_img = scrapy.Field()
    option1_list = scrapy.Field()
    option2_list = scrapy.Field()

    pd_img_list = scrapy.Field()
    categories_opencard = scrapy.Field()
    Product_price = scrapy.Field()
