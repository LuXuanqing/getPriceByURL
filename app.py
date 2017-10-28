from openpyxl import load_workbook
from openpyxl import Workbook
from tmall import getTmallPrice
from jd import getJdPrice
import os.path
import time

# 获取文件路径
path = {}
path['source'] = input('正在获取文件目录\n把表格拖进这个窗口，然后按下回车\npath: ')
while path['source'].endswith(' '):
    path['source'] = path['source'][:-1]

# 加载excel文件中的第一个sheet
wb = load_workbook(path['source'])
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
# 设置保存路径以及文件名
path['dirname'] = os.path.dirname(path['source'])
path['basename'] = os.path.basename(path['source'])
now = time.strftime('%H%M%S')
path['filename'] = now + '已抓取_' + path['basename']
path['target'] = os.path.join(path['dirname'], path['filename'])
print(path)
wb.save(path['target'])
print('successfully saved')