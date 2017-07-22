# -*- coding: UTF-8 -*-
import urllib
import urllib2
import json
import MySQLdb
import time


# Create your views here.


def index():
    info = [{'banner_id':'1', 'keyword':u'韩都','img_url':'http://ads-cdn.chuchuguwen.com/FjYB3BRtbIiND66TuB2D3OFr_0bw'},
            {'banner_id':'2', 'keyword':u'纯色','img_url':'https://afp-cdn.chuchujie.com/o_1bl84gdeuvs323g1936nq711fc1l.png'},
            {'banner_id':'3', 'keyword':u'雪纺','img_url':'https://afp-cdn.chuchujie.com/o_1bl84v5kf4pb105gks168tsrg1j.png'},
            {'banner_id':'4', 'keyword':u'旗袍','img_url':'https://afp-cdn.chuchujie.com/o_1bl85e4rnpr81vug10t3t3ermv1l.png'},
            {'banner_id':'5', 'keyword':u'裙套装','img_url':'https://afp-cdn.chuchujie.com/o_1bktgh5v221rbau1mor1h4s2sn1j.png'}
           ]
    insert(info)


def insert(items):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='!QAZxsw2',port=3306)
    cur=conn.cursor()  
    values = []
    ds = time.strftime("%Y%m%d", time.localtime())     
    for k in items:
        values.append("('%s','%s','%s','%s')"%(str(ds),k["banner_id"],k["keyword"],k["img_url"]))
   
    sql = "REPLACE INTO coupon.dwxk_bannerinfo(ds,banner_id,keyword,img_url) VALUES %s" % ",".join(values)
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
 
if __name__ == '__main__':
    index()
    print "success"

