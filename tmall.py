import urllib.request
import json
import re

def getTmallPrice(url):
    '''输入一个String类型的参数（天猫商品的url），返回该商品的价格.

    异常返回：
    -101：商品的url错误
    -102：无法获取商品id
    -103：发送的HTTP请求收不到返回数据
    -104：服务器没有返回正确数据'''
   
    # 检查url是否是字符串并且符合天猫链接的格式
    if (not isinstance(url, str)) or (not re.search('detail\.tmall\.com/(.*)[?&]id=(\d)+', url)):
        print('天猫url错误')
        return -101

    # 从url截取商品id
    regex = re.compile('[?&]id=(\d)+')
    match = regex.search(url)
    if match:
        id = match.group().split('=')[-1]
        # print('tmall-id: {}'.format(id))
    else:
        print('无法获取商品id')
        return -102

    # 构造包含headers的请求
    headers = {"Referer": url}
    queryURL = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId={}'.format(id)
    request = urllib.request.Request(queryURL, headers=headers)
    
    # 发送请求，将返回数据解析为json格式
    def getJSON():
        response = urllib.request.urlopen(request)
        if response.status != 200:
            print('发送的HTTP请求收不到返回数据')
            return -103
        jsonStr = response.read().decode('gbk')
        result = json.loads(jsonStr)
        return result

    # 尝试从从json结果中获取价格，如果不行则重新请求获取新的json
    tries_max = 3
    tries_now = 1
    price = None
    while(price == None):
        try:
            result = getJSON()
            price_info = result["defaultModel"]["itemPriceResultDO"]["priceInfo"]
            # 目前已知有两种不同的数据结构
            if "price" in price_info["def"]:
                price = price_info["def"]["price"]
            else:
                price = price_info["def"]["promotionList"][0]["price"]
            # print('tmall-price: {}'.format(price))
            return float(price)
        except KeyError as e:
            if tries_now <= 3:
                print(result)
                print('获取失败，正在重试{}/{}'.format(tries_now, tries_max))
                tries_now += 1
            else:
                tries_now = 1
                print('暂时查不到，手动试试吧')
                return 104
    
if __name__ == '__main__':
    test_urls = [
        'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.57.d811797BWzo4C&id=551260402678&areaId=310100&user_id=2616970884&cat_id=2&is_b=1&rn=641326f23d0d27fe06b99e092effd88e',
    ]

    for url in test_urls:
        print(getTmallPrice(url))