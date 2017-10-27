import urllib.request
import json
import re

def getTmallPrice(url):
    # 检查url是否是字符串
    if not url.isalnum:
        print('商品的天猫url错误')
        return None

    # 从url截取商品id
    regex = re.compile('[?&]id=(\d)+')
    match = regex.search(url)
    if match:
        id = match.group().split('=')[-1]
        print('id: {}'.format(id))
    else:
        print('无法获取商品id')
        return None

    # http请求的request headers
    headers = {"Referer": url}
    # 查询价格的地址
    queryURL = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId={}'.format(id)

    # 发送请求
    request = urllib.request.Request(queryURL, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('gbk')
    result = json.loads(html)
    # print(type(result))
    # print(result)
    try:
        price_info = result["defaultModel"]["itemPriceResultDO"]["priceInfo"]
        price = price_info["def"]["promotionList"][0]["price"]
        print('price: {}'.format(price))
    except KeyError as e:
        print(e,'获取失败，请稍后重试')
    

getTmallPrice('https://detail.tmall.com/item.htm?id=20757312104')
getTmallPrice('https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-15096307578.48.751595225uUB1Q&id=525167180958&rn=27a3c84555e1eda097271292eb27af13&abbucket=11')
getTmallPrice('https://detail.tmall.com/item.htm?spm=a220o.1000855.0.da321h.621b1e40ug4X52&id=22354227999')
getTmallPrice('https://chaoshi.detail.tmall.com/item.htm?spm=a220m.1000858.1000725.5.d81179771fpxr&id=536571819737&areaId=310100&user_id=725677994&cat_id=2&is_b=1&rn=81f6294d7e67f238244f5882f43c506f')