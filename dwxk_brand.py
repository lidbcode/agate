import urllib
import urllib2
import json
import MySQLdb
import time


# Create your views here.


def index():
    url = "https://www.daweixinke.com/sqe.php"
    parameter = "?s=/Brand/getBrandList&data[platform]=web"
    response = urllib.urlopen(url + parameter)
    result = json.load(response)    
    insert(result["data"])


def insert(items):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='!QAZxsw2',port=3306)
    cur=conn.cursor()  
    values = []
    ds = time.strftime("%Y%m%d", time.localtime())     
    for k in items:
        values.append("('%s','%s','%s','%s')"%(str(ds),k["id"],k["ad_brand_name"],k["brand_logo"]))
   
    sql = "REPLACE INTO coupon.dwxk_brandinfo(ds,brand_id,ad_brand_name,brand_logo) VALUES %s" % ",".join(values)
    print sql
    ##cur.execute(sql)
    ##conn.commit()
    ##cur.close()
    conn.close()
 
if __name__ == '__main__':
    index()
    print "success"

