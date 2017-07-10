import urllib
import urllib2
import json
import MySQLdb
import time


# Create your views here.


def get_item_info(url,module_source):
    items = []
    response = urllib.urlopen(url)
    result = json.load(response)
    if (result != None):
        items = result["data"]["data"]
        for item in items:
            adId = "&data[adId]=%s" % (item["ad_id"])
            itemId = "&data[itemId]=%s" % (item["item_id"])
            adZoneId = "&data[adZoneId]=18557"
            addSource = "&data[add_source]=%s"%(module_source)
            isVideo = "&data[isVideo]=0"
            platform = "&data[platform]=web"
            data = adId + itemId + adZoneId + addSource + isVideo + platform
            coupon = get_coupon_url(data)
            item["coupon"] = coupon
    return items


def get_coupon_url(data):
    url = "https://www.daweixinke.com/sqe.php?s=/CCKItem/addCCKItem"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'UTF-8',
        'Cookie': 'UM_distinctid=15b2a27ba8581-01c694495-66121479-15f900-15b2a27ba88cc; cck_access_token=E39E77BAF9D80C3CFEE2529120D8048C; C NZZDATA1261673522=1222127928-1497702020-https%253A%252F%252Fwww.daweixinke.com%252F%7C1497702020; PHPSESSID=9goqo4bnidkigl5qt2c40kips4; CNZ ZDATA1261294143=8452916-1491059078-https%253A%252F%252Fwww.baidu.com%252F%7C1497887195'
    }
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    result = json.load(response)["data"]
    if("couponShare" in result):
        return result["couponShare"]["discount_url"]
    if("productShare" in result):
        return result["productShare"]["detail_url"]


