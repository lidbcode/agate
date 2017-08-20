import urllib
import urllib2
import json
import MySQLdb
import time


# Create your views here.


def index():
    url = "https://www.daweixinke.com/sqe.php"
    items = []
    for c1 in range(-1,-15,-1):
        parameter = "?s=/CCKItem/getAdItemList&data[platform]=web&data[pageNum]=10&data[order_status]=10&data[c1]=%s&data[page]="%(c1,)
        for page in range(1,101):
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
        'Cookie' : 'UM_distinctid=15cafebfdc158-0f5d0448a59178-323f5c0f-1fa400-15cafebfdc2790; m_cck_access_token=54AC5F8C8B8B93CE107B95BB46E8D9D8; CNZZDATA1261674589=503176748-1499417870-https%253A%252F%252Fwww.daweixinke.com%252F%7C1499417870; CNZZDATA1261330578=1564621818-1499414616-%7C1499845721; CNZZDATA1261674382=1815685325-1499077465-https%253A%252F%252Fwww.daweixinke.com%252F%7C1500538419; gwapp_userId=10360; PHPSESSID=re0fs5fi4mij7dkjti95sm23m4; cookie_test=1; cck_access_token=A36FF87B177F17EACC68150E55C3C719; CNZZDATA1261294143=450722296-1497595338-https%253A%252F%252Fwww.google.co.jp%252F%7C1501223559'
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
        values.append("""("%s","%s","%s","%s","%s","%s","%s","%s","%s")"""%(str(ds),k["ad_id"],k["ad_name"],k["money"],k["ad_coupon_price"],k["image_urls_head"],k["coupon"],k['c1'],k['sales_num']))
   
    sql = "REPLACE INTO coupon.dwxk_itemsinfo(ds,ad_id,ad_name,coupon_value,price,img_url,coupon_url,c1,sales_num) VALUES %s" % ",".join(values)
    ## print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
 
if __name__ == '__main__':
    index()
    print "success"

