import urllib
import urllib2
import json
import MySQLdb
import time


# Create your views here.


def index():
    url = "https://www.daweixinke.com/sqe.php"
    items = []
    for c1 in range(-14,0):
        parameter = "?s=/CCKItem/getAdItemList&data[platform]=web&data[pageNum]=10&data[order_status]=10&data[c1]=%s&data[page]="%(c1,)
        for page in range(1,11):
            response = urllib.urlopen(url + parameter + str(page))
            ## print url + parameter + str(page) 
            result = json.load(response)
            if (result != None):
                items = items + result["data"]["data"]

        for item in items:
            adId = "&data[adId]=%s" % (item["ad_id"])
            itemId = "&data[itemId]=%s" % (item["item_id"])
            adZoneId = "&data[adZoneId]=18557"
            addSource = "&data[add_source]=home"
            isVideo = "&data[isVideo]=0"
            platform = "&data[platform]=web"
            data = adId + itemId + adZoneId + addSource + isVideo + platform
            coupon = getCoupon(data)
            item["coupon"] = coupon
        print parameter
        insert(items)

def getCoupon(data):
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

def insert(items):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='!QAZxsw2',port=3306)
    cur=conn.cursor()  
    values = []
    ds = time.strftime("%Y%m%d", time.localtime())     
    for k in items:
        values.append("('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(str(ds),k["ad_id"],k["ad_name"],k["money"],k["ad_coupon_price"],k["image_urls_head"],k["coupon"],k['c1'],k['sales_num']))
   
    sql = "REPLACE INTO coupon.dwxk_itemsinfo(ds,ad_id,ad_name,coupon_value,price,img_url,coupon_url,c1,sales_num) VALUES %s" % ",".join(values)
    ## print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
 
if __name__ == '__main__':
    index()
    print "success"

