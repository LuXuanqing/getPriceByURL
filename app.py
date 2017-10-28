from openpyxl import load_workbook
from openpyxl import Workbook
from tmall import getTmallPrice

# 加载excel文件中的第一个sheet
wb = load_workbook('source.xlsx')
ws = wb.worksheets[0]
lenRows = len(list(ws.rows))
# 获取除了第一行表头外的所有行
rows = ws.iter_rows(row_offset=1, max_row=lenRows-1)

for sku,name,url,price in rows:
    # print(name)
    price.value = getTmallPrice(url.value)

wb.save('result.xlsx')
print('successfully saved')