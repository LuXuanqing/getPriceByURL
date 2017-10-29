import urllib.request
import json
import re

def getJdPrice(url):
    '''输入一个String类型的参数（京东商品的url），返回该商品的价格.
    
    异常返回：
    -101：商品的url错误
    -102：无法获取商品id
    -103：发送的HTTP请求收不到返回数据
    -104：服务器没有返回正确数据'''

    # 检查输入的url是否是字符串，并且符合京东商品链接的形式
    regex_url = re.compile('item\.jd\.com/(\d+)\.html')
    if (not isinstance(url, str)) or (not regex_url.search(url)):
        print('京东url错误')
        return -101

    # 从url截取商品id
    regex_id = re.compile('/(\d+)\.html')
    match = regex_id.search(url)
    if match:
        match_str = match.group()
        id = re.search('\d+', match_str).group()
        # print('jd-id: {}'.format(id))
    else:
        print('无法获取商品id')
        return -102

    # 发送请求，解析json
    query_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + id
    response = urllib.request.urlopen(query_url)
    if response.status != 200:
        print(-103)
        return '发送的HTTP请求收不到返回数据'
    jsonStr = response.read().decode('utf-8')
    result = json.loads(jsonStr)
    # print(result)
    price = float(result[0]["p"])
    # print('jd-price: {}'.format(price))
    if price >=0:
        return price
    else:
        print('商品已下架或查询不到价格')
        return -104

if __name__ == '__main__':
    urls = [
        'https://item.jd.com/2179367.html',
        'https://item.jd.com/1744037.html',
        'https://item.jd.com/1590230.html',
        'https://item.jd.com/2385471.html',
        None
    ]
    for url in urls:
        getJdPrice(url)