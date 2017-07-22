import urllib
import urllib2
import json
import MySQLdb
import time


# Create your views here.


def getCoupon():
    url = 'https://order.chuchutong.com/api.php'
    data = """data[data]={"api_version":"v5","ageGroup":"AG_0to24","imei":"","channel":"QD_appstore","package_name":"com.culiukeji.huanletao","client_type":"h5","client_version":"3.9.101","userId":"","subChannel":"dwxk","method":"view_order_all_mixed","num":"30","page":1,"token":"ccjd21532088770fde000035167405671532088770","order_status_type":0}}"""
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'UTF-8',
        'Cookie':'UM_distinctid=15cafebfdc158-0f5d0448a59178-323f5c0f-1fa400-15cafebfdc2790; m_cck_access_token=54AC5F8C8B8B93CE107B95BB46E8D9D8; CNZZDATA1261674589=503176748-1499417870-https%253A%252F%252Fwww.daweixinke.com%252F%7C1499417870; CNZZDATA1261330578=1564621818-1499414616-%7C1499845721; cck_access_token=10B3EBD7ABC237329ABB699F9074B97D; PHPSESSID=15n4ms5eb1ghogsvkcml6blo07; gwapp_userId=10360; CNZZDATA1261674382=1815685325-1499077465-https%253A%252F%252Fwww.daweixinke.com%252F%7C1500538419; CNZZDATA1261294143=450722296-1497595338-https%253A%252F%252Fwww.google.co.jp%252F%7C1500534407'
    }
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    result = json.load(response)
    print result

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
    getCoupon()
    print "success"

