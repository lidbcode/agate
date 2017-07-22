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
        'Cookie' : 'UM_distinctid=15cafebfdc158-0f5d0448a59178-323f5c0f-1fa400-15cafebfdc2790; m_cck_access_token=54AC5F8C8B8B93CE107B95BB46E8D9D8; CNZZDATA1261674589=503176748-1499417870-https%253A%252F%252Fwww.daweixinke.com%252F%7C1499417870; CNZZDATA1261330578=1564621818-1499414616-%7C1499845721; cck_access_token=10B3EBD7ABC237329ABB699F9074B97D; PHPSESSID=15n4ms5eb1ghogsvkcml6blo07; gwapp_userId=10360; CNZZDATA1261674382=1815685325-1499077465-https%253A%252F%252Fwww.daweixinke.com%252F%7C1500538419; CNZZDATA1261294143=450722296-1497595338-https%253A%252F%252Fwww.google.co.jp%252F%7C1500534407'
    }
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    result = json.load(response)["data"]
    if("couponShare" in result):
        return result["couponShare"]["discount_url"]
    if("productShare" in result):
        return result["productShare"]["detail_url"]


