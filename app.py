from openpyxl import load_workbook
from openpyxl import Workbook
from tmall import getTmallPrice
from jd import getJdPrice

# 加载excel文件中的第一个sheet
wb = load_workbook('source.xlsx')
ws = wb.worksheets[0]
lenRows = len(list(ws.rows))
print('共有{}行'.format(lenRows))
# 获取除了第一行表头外的所有行
rows = ws.iter_rows(row_offset=1, max_row=lenRows-1)

for sku,name,jd_price,jd_url,tmall_price,tmall_url in rows:
    print('正在查询：{0}-{1}'.format(sku.value, name.value))
    if jd_url.value:
        jd_price.value = getJdPrice(jd_url.value)
    if tmall_url.value:
        tmall_price.value = getTmallPrice(tmall_url.value)

wb.save('result.xlsx')
print('successfully saved')