# -*- coding: UTF-8 -*-

import re
from selenium import webdriver
import time
import json


def work():
    driver = webdriver.Chrome("chromedriver.exe")
    ds = time.strftime("%Y%m%d", time.localtime())
    fout = open("%s/data-%s.json" % (ds, ds), 'w')
    result = []
    for round in range(1, 101):
        print "the %s page start " % (round,)

        url = "http://www.qingtaoke.com/qingsou?istmall=1&min_price=50&s_type=1&sort=1&page=%s&f=1" % (round,)
        driver.get(url)
        page = driver.page_source
        item_id_list = re.findall(">https://item.taobao.com/item\.htm\?id=([0-9]+)", page, re.S)
        activity_id_list = re.findall("activityId=([A-Za-z0-9]*)<", page, re.S)

        print "item_id_list size is %d , activity_id_list size is %d" % (len(item_id_list), len(activity_id_list))

        url_head = "https://uland.taobao.com/coupon/edetail"
        for i in range(0, min(len(item_id_list), len(activity_id_list))):
            activity_id = activity_id_list[i]
            item_id = item_id_list[i]
            coupon_url = "%s?activityId=%s&itemId=%s" % (url_head, activity_id, item_id)
            item_coupon = {"item_id": item_id, "coupon_url": coupon_url}
            result.append(json.dumps(item_coupon))
        print "the %s page end \n" % (round,)
    fout.write("\n".join(result))
    fout.close()
    driver.quit()
    print "work is OK"


if __name__ == '__main__':
    work()
    print "success"
