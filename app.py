import tm
import jd
from excel import Excel as E

# 打开excel表格
e = E()
e.get_path()
e.open()
e.get_index()


def get_price():
    # 遍历所有行(第一行除外)
    for row in range(1, e.nrows):
        # 获得该行所需的单元格
        tm_url_cell = e.ws.cell(row=row + 1, column=e.index['tm_url'] + 1)
        tm_price_cell = e.ws.cell(row=row + 1, column=e.index['tm_price'] + 1)
        jd_url_cell = e.ws.cell(row=row + 1, column=e.index['jd_url'] + 1)
        jd_price_cell = e.ws.cell(row=row + 1, column=e.index['jd_price'] + 1)
        sku_cell = e.ws.cell(row=row + 1, column=e.index['sku'] + 1)
        name_cell = e.ws.cell(row=row + 1, column=e.index['name'] + 1)
        # 打印查询进度信息
        print('({}/{})正在查询:({}){}'.format(e.items_counting, e.items_total, sku_cell.value,
                                          name_cell.value))
        e.items_counting += 1
        # 查询价格并写入表格
        if tm_url_cell.value:
            tm_price_cell.value = tm.get_price(tm_url_cell.value)
            if isinstance(tm_price_cell.value, str):
                tm_price_cell.font = e.ft
                e.err_row.add(row)
        if jd_url_cell.value:
            jd_price_cell.value = jd.get_price(jd_url_cell.value)
            if isinstance(jd_price_cell.value, str):
                jd_price_cell.font = e.ft
                e.err_row.add(row)

try:
    get_price()
except BaseException as err:
    print(err)
finally:
    # 关闭chrome
    # tm.driver.quit()
    # 保存excel
    e.save()

# 打印异常商品信息
if len(e.err_row) > 0:
    key = input('{}个商品的价格查询有异常，按回车查看，输入q退出\n'.format(len(e.err_row)))
    if key == 'q':
        quit()
    elif key == '':
        e.err_rows = list(e.err_row)

        def printItem(row):
            '''输出指定行的商品sku和名称。
            '''
            sku = e.ws.cell(row=row + 1, column=e.index['sku'] + 1).value
            name = e.ws.cell(row=row + 1, column=e.index['name'] + 1).value
            print('{}-{}'.format(sku, name))

        print('\n+++++++++++++++以下商品价格查询有异常，记得检查一下哦+++++++++++++++')
        for row in e.err_rows:
            printItem(row)
        print('+++++++++++++++以上商品价格查询有异常，记得检查一下哦+++++++++++++++\n')

# 退出程序
input('按回车退出程序')