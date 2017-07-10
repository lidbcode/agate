import urllib
import urllib2
import json
import MySQLdb
import time
import common_items


# Create your views here.


def index():
    brand_ids = []
    brand_url = "https://www.daweixinke.com/sqe.php?s=/Brand/getBrandList&data[platform]=web"
    response = urllib.urlopen(brand_url)
    result = json.load(response)
    for brand in result["data"]:
      brand_ids.append(int(brand["id"]))
    brand_ids.sort()
    print brand_ids
 
    base_url = "https://www.daweixinke.com/sqe.php?s=/Brand/getBrandItemList"
    items = []
    for brand_id in brand_ids:
        url = "%s&data[platform]=web&data[pageNum]=10&data[order_status]=9&data[ad_brand_id][]=%s&data[page]="%(base_url,brand_id)
        for page in range(1,11):
            items = common_items.get_item_info(url + str(page),"brand")    
            print "################ %s" %(brand_id,)
            if(len(items) > 0):
                insert(items,brand_id)

def insert(items,brand_id):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='!QAZxsw2',port=3306)
    cur=conn.cursor()  
    values = []
    ds = time.strftime("%Y%m%d", time.localtime())     
    for k in items:
        values.append("('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(str(ds),k["ad_id"],k["ad_name"],k["money"],k["ad_coupon_price"],k["image_urls_head"],k["coupon"],str(brand_id),k['sales_num']))
   
    sql = "REPLACE INTO coupon.dwxk_branditems(ds,ad_id,ad_name,coupon_value,price,img_url,coupon_url,brand_id,sales_num) VALUES %s" % ",".join(values)
    ## print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
 
if __name__ == '__main__':
    index()
    print "success"

