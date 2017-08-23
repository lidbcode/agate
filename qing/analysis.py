# -*- coding: UTF-8 -*-

import time
import json


def work():
    ds = 20170820
    res_dic = {}
    num = 8
    for r in range(1, num + 1):
        fin = open("coupon-%s-%s.json" % (ds, r))
        for line in fin:
            line_json = json.loads(line)
            item_id = line_json["itemId"]
            activity_id = line_json["activityId"]
            spider_time = int(line_json["time"])

            start_time = 0
            end_time = spider_time

            if line_json["effectiveStartTime"] != "":
                start_time = int(line_json["effectiveStartTime"])
            if line_json["effectiveEndTime"] != "":
                end_time = int(line_json["effectiveEndTime"])

            if (item_id, activity_id) not in res_dic:
                res_dic[(item_id, activity_id)] = (start_time, end_time)
            else:
                (old_start_time, old_end_time) = res_dic[(item_id, activity_id)]
                if old_start_time > start_time:
                    start_time = old_start_time
                if old_end_time < end_time:
                    end_time = old_end_time
                res_dic[(item_id, activity_id)] = (start_time, end_time)
        fin.close()

    freq_dic = {}
    for (item_id, activity_id) in res_dic.keys():
        start_time = res_dic[(item_id, activity_id)][0]
        end_time = res_dic[(item_id, activity_id)][1]
        online_time = (end_time - start_time) / 3600
        if start_time != 0:
            if online_time not in freq_dic:
                freq_dic[online_time] = 1
            else:
                freq_dic[online_time] = freq_dic[online_time] + 1

    fout = open("res-%s-%s.csv" % (ds, num), "w")
    for freq in sorted(freq_dic.keys()):
        fout.write("%s,%s\n" % (freq, freq_dic[freq]))
    fout.close()


if __name__ == "__main__":
    work()
