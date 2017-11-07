from urllib import request as rq
import json
import re
import time


# def get_id(url):
#     '''输入天猫商品详情页的url，返回sku的id。

#     url: 应该以'detail.tmall.com/'结尾，并且带有查询参数'id'
#     '''
#     # 检查url是否为str类型
#     if isinstance(url, str):
#         return None
#     # 检查url是否符合标格式
#     reg_url = re.compile('detail\.tmall\.com/(.*)[?&]id=(\d)+')
#     match_url = reg_url.search(url)
#     if not match_url:
#         return None
#     # 从url截取商品id
#     reg_id = re.compile('[?&]id=(\d)+')
#     match_id = reg_id.match(url)
#     if match_id:
#         id = match_id.group().split('=')[-1]
#         return id
#     else:
#         return None


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
    headers = {
        "Referer": url,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        "cookie": "lzstat_uv=21485933322929638385|3511896; ubn=p; miid=9001292936332341548; UM_distinctid=15d965b3379b5d-02a831406adc6-30657808-fa000-15d965b337a9e6; thw=cn; l=AmRk1tk-o-BSFvOfu1J5MMMwtGhWkIhk; cna=8UUyDpcaY0ECAT2t1qZcbs/n; _tb_token_=37b5aa39e81b3; hng=CN%7Czh-CN%7CCNY%7C156; v=0; uc1=cookie14=UoTcBr9Wzv2OPQ%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=VFC%2FuZ9ainBZ&tag=8&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0; uc3=sg2=AimSmhoFEYv%2FqajglLcPoQBACmdH9DU2rRQB8Uv3K%2B8%3D&nk2=D8L%2F7YD6LiI%3D&id2=W8gzaQv%2F5hs%3D&vt3=F8dBzLKEEQgYXbeUwIE%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; existShop=MTUwOTcxMTc4Nw%3D%3D; uss=VvuF6eGuZroPj2Hn6Wu%2Fk10VCFmKXe2eiGRsgpxJKgg0cHr8LVXVGd9j6w%3D%3D; lgc=lastid00; tracknick=lastid00; cookie2=391c10a031d7da5cb2ac6f29d9aa3a39; sg=017; mt=np=&ci=0_0; cookie1=UtU%2FewAgTKvDLTnmf3FBWnHb3q9zZLww%2FRmOWCjL88g%3D; unb=81056781; skt=2926e1fb4a86588d; t=9cde2ebbe7f7549b72ecd6136ddee4fb; publishItemObj=Ng%3D%3D; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=lastid00; cookie17=W8gzaQv%2F5hs%3D; isg=AkNDtulvHlZe0NxeiYxe6LCb0gEtENaf9XcUtnUgmqIZNGNW_YhnSiEk0POA; ucn=unsz"
    }
    queryURL = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId={}'.format(id)
    request = rq.Request(queryURL, headers=headers)

    # 发送请求，将返回数据解析为json格式
    def getJSON(req):
        # print(req)
        res = rq.urlopen(req)
        # print(res)
        if res.status != 200:
            print('发送的HTTP请求收不到返回数据')
            return -103
        jsonStr = res.read().decode('gbk')
        # print(jsonStr)
        result = json.loads(jsonStr)
        return result

    # 尝试从从json结果中获取价格，如果不行则重新请求获取新的json
    tries_max = 0
    tries_now = 1
    price = None
    while(price == None):
        result = None
        try:
            result = getJSON(request)
        except BaseException as e:
            print(e)
            return -104
        price_info = result.get('defaultModel').get(
        'itemPriceResultDO').get('priceInfo')
        # 目前已知有两种不同的数据结构
        price = price_info.get('def').get('price') \
        or price_info.get('def').get('promotionList')[0].get('price')
        # print('tmall-price: {}'.format(price))

        if not price:
            if tries_now <= 3:
                # print(result)
                print('获取失败，正在重试{}/{}'.format(tries_now, tries_max))
                tries_now += 1
            else:
                tries_now = 1
                print('暂时查不到，手动试试吧')
                return -104
    return float(price)

if __name__ == '__main__':
    test_urls = [
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=545899079127&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=545874722352&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a7i7w97j&id=35649750981&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=531593015208&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=531592711979&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a220o.7406545.0.0.37b3010cNGtC49&id=534541275468'
    ]
    
    for url in test_urls:
        print(getTmallPrice(url))
        time.sleep(1)