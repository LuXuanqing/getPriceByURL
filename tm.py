from selenium import webdriver
import re

# chrome配置-不加载图片
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# chrome配置-headless
# chrome_options.add_argument("--headless")
# chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


# 打开chrome
driver = webdriver.Chrome(chrome_options=chrome_options)


def is_url_correct(url):
    '''输入一个字符串，检查是否为天猫商品详情页的url，返回一个Bool。'''
    # 检查url是否为str类型
    if not isinstance(url, str):
        return False
    # 检查url是否符合标格式
    reg_url = re.compile('detail\.tmall\.com/(.*)[?&]id=(\d)+')
    match = reg_url.search(url)
    if match:
        return True
    else:
        return False


def get_price(url):
    '''输入天猫商品详情页url，返回该商品价格。
    
    url: 应该以'detail.tmall.com/'结尾，并且带有查询参数'id'
    '''
    try:
        assert is_url_correct(url), 'url错误'
    except AssertionError as e:
        return str(e)
    driver.get(url)
    elems = driver.find_elements_by_class_name('tm-price')
    for elem in elems:
        if elem.text != '':
            price = float(elem.text)
    print('tm-price: {}'.format(price))
    return price


if __name__ == '__main__':
    test_urls = [
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=545899079127&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=545874722352&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a7i7w97j&id=35649750981&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=531593015208&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a3204.7933263.0.0.e859a78bSdQn&id=531592711979&rewcatid=50514008',
        'https://chaoshi.detail.tmall.com/item.htm?spm=a220o.7406545.0.0.37b3010cNGtC49&id=534541275468'
    ]

    driver = webdriver.Chrome(chrome_options=chrome_options)

    for url in test_urls:
        print(get_price(url))

    driver.quit()
