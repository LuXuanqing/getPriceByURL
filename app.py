import tm
import jd
from excel import Excel

# 打开excel表格
xls = Excel()


def set_price():
    # 遍历所有行(第一行除外)，查询并写入价格
    for row in range(1, xls.nrows):
        sku = xls.fetch_sku_by_row(row)
        name = xls.fetch_name_by_row(row)
        tm_url = xls.fetch_tm_url_by_row(row)
        jd_url = xls.fetch_jd_url_by_row(row)
        # 打印查询进度信息
        print('{}/{}正在查询\t{}\t{}'.format(xls.items_counting, xls.items_total, sku, name))
        xls.items_counting += 1
        # 查询价格并写入表格
        if tm_url:
            tm_price = tm.get_price(tm_url)
            xls.set_tm_price_by_row(row, tm_price)
        if jd_url:
            jd_price = jd.get_price(jd_url)
            xls.set_jd_price_by_row(row, jd_price)


try:
    set_price()
except BaseException as err:
    print(err)
finally:
    # 关闭chrome
    tm.driver.quit()
    # 保存excel
    xls.save()

# 打印异常商品信息
if len(xls.err_rows) == 0:
    print('没有异常')
else:
    key = input('{}个商品的价格有异常，按回车查看'.format(len(xls.err_rows)))
    if key == '':
        rows = list(xls.err_rows)
        for row in rows:
            sku = xls.fetch_sku_by_row(row)
            name = xls.fetch_name_by_row(row)
            print('行\tSKU\t商品名称')
            print('{}\t{}\t{}'.format(row+1, sku, name))

# 退出程序
input('按回车退出程序')