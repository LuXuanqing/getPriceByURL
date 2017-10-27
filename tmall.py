import urllib.request
import json

def getTmallPrice(url):
    # 检查url是否是字符串
    if not url.isalnum:
        print('商品的天猫url错误')
        return None

    # 从url截取商品id
    tempId = url.split('id=')[-1]
    # id后面可能带有其它参数
    if tempId.find('&') == -1:
        id = tempId
    else:
        id = tempId.split('&')[0]
    # 检验id是否为数字
    if not id.isdigit():
        print('无法获取正确的商品id，id={}'.format(id))
        return None
    print('id: {}'.format(id))

    # http请求的request headers
    headers = {"Referer": url}
    # 查询价格的地址
    queryURL = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId={}'.format(id)

    # 发送请求
    request = urllib.request.Request(queryURL, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('gbk')
    result = json.loads(html)
    price_info = result["defaultModel"]["itemPriceResultDO"]["priceInfo"]
    price = price_info["def"]["promotionList"][0]["price"]
    print('id: {}, price: {}'.format(id, price))

getTmallPrice('https://chaoshi.detail.tmall.com/item.htm?spm=a220m.1000858.1000725.5.d81179771fpxr&id=536571819737')