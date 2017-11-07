import urllib.request as req
import json
import re


def is_url_correct(url):
    # 检查url是否为str类型
    if not isinstance(url, str):
        return False
    # 检查url是否符合标格式
    reg_url = re.compile('item\.jd\.com/(\d+)\.html')
    match = reg_url.search(url)
    if match:
        return True
    else:
        return False
def get_id(url):
    '''输入JD商品详情页url，返回该商品id。
    
    url: 应该符合'item.jd.com/*.html'的形式
    '''
    assert is_url_correct(url), 'url错误'
    # 从url截取商品id
    reg_id = re.compile('/(\d+)\.html')
    match = reg_id.search(url)
    match_str = match.group()
    id = re.search('\d+', match_str).group()
    # print('jd-id: {}'.format(id))
    return id

def get_json(id):
    '''通过商品id发送GET请求，返回json'''
    # 发送请求，把结果解析为json
    query_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + id
    response = req.urlopen(query_url)
    assert response.status == 200, '发送的HTTP请求收不到返回数据'
    jsonStr = response.read().decode('utf-8')
    result = json.loads(jsonStr)
    return result


def get_price(url):
    '''输入一个京东商品的url，返回该商品的价格'''
    # 获取id
    try:
        id = get_id(url)
    except AssertionError as e:
        return str(e)
    # 获取json
    try:
        result = get_json(id)
    except AssertionError as e:
        return str(e)
    # 从json中获取价格
    price = None
    try:
        price = result[0]['p']
    except BaseException as e:
        return str(e)
    else:
        price = float(price)
        return price
        # print('jd-price: {}'.format(price))


if __name__ == '__main__':
    urls = [
        'https://item.jd.com/2179367.html',
        'https://item.jd2.com/1744037.html',
        332,
        True,
        None
    ]
    for url in urls:
        print(get_price(url))