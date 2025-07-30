from lxml import html


def list_purchasing_all(html_str: str):
    tree = html.fromstring(html_str)
    good_element_list: list[html.HtmlElement] = tree.xpath('//tr[contains(@class, "goodsId")]')
    for good_element in good_element_list:
        purchase_id = good_element.xpath('@id')[0]
        purchase_order_number = good_element.xpath('.//a[@class="limingcentUrlpic"]/text()')[0]
        ghs_id = good_element.xpath('.//span[contains(@class, "ghsHoverPrompt")]/@data-ghsid')[0]
        ghs_name = good_element.xpath('.//span[contains(@class, "ghsHoverPrompt")]/span/text()')[0].strip()
        warehouse_name, purchase_info = good_element.xpath('.//td[4]/span/text()')[0].strip().split('|')
        # 采购员
        agent_name = purchase_info.split('：')[1]
        #print(purchase_order_number, ghs_id, ghs_name, warehouse_name, agent_name)
        # 获取兄弟元素
        content_element = good_element.getnext()
        # 获取商品信息
        img = content_element.xpath('.//img/@data-original')[0]
        content_number_info = content_element.xpath('./td[2]/text()')
        product_zl_number = None
        purchase_number = None
        for content_number in content_number_info:
            content_number = content_number.strip()
            if content_number.split('：')[0] == '商品种类':
                product_zl_number = content_number.split('：')[1].strip()
            elif content_number.split('：')[0] == '采购数量':
                purchase_number = content_number.split('：')[1].strip()
        # 解析出货款
        total_amount = content_element.xpath('./td[3]//input/@data-totalamount')[0]
        # 运费
        shipping_amount = content_element.xpath('./td[3]//input/@value')[0]
        platform_list = content_element.xpath('./td[4]/div/span')
        if len(platform_list) > 0:
            source = platform_list[0].text.strip()
        else:
            source = content_element.xpath('./td[4]/span/span/text()')[0].strip()
            source2 = content_element.xpath('./td[4]/span/span[@class="alibabaPurchaseOrder"]/text()')[0].strip()
            source = source + source2
        print(source)
