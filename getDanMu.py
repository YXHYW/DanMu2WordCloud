import requests
import json
import chardet
import re

def get_cid(bvid):
    """根据 bvid 得到 cid"""
    url = 'https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(bvid)
    res = requests.get(url).text
    json_dict = json.loads(res)
    return json_dict["data"][0]["cid"]

"""
注意：哔哩哔哩的网页现在已经换了，那个list.so接口已经找不到，但是我们现在记住这个接口就行了。
"""
def get_data(cid):
    # 根据cid请求弹幕，解析弹幕得到最终的数据
    final_url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(cid)
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    pattern = re.compile('<d.*?>(.*?)</d>')
    data = pattern.findall(final_res)
    return data

def save_to_file(data):
    # 保存弹幕列表
    with open(".\\dan_mu.txt",'w', encoding="utf-8") as f:
        count = 0
        for i in data:
            f.write(i)
            f.write("\n")
            count += 1
        print("{0}条弹幕写入完成！".format(count))


if __name__ == "__main__":
    bvid = "BV17s411B73s"
    cid = get_cid(bvid)
    data = get_data(cid)
    save_to_file(data)
    # print(data)