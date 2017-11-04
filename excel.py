from openpyxl import load_workbook
from openpyxl.styles import Font, Color, colors
import os.path
import time
import tm
import yapf


class Excel(object):
    def __init__(self):
        self.path = {}
        self.fields = []
        # 存储异常商品所在行
        self.err_row = set()
        # 设置字体
        self.ft = Font(color=colors.RED)

    def get_path(self):
        '''获取excel文件目录'''
        path = input('把表格拖进这个窗口，然后按下回车\n')
        # 去除路径末尾的空格
        while path.endswith(' '):
            path = path[:-1]
        # 保存路径
        self.path['source'] = path
        self.path['dirname'] = os.path.dirname(self.path['source'])
        self.path['basename'] = os.path.basename(self.path['source'])

    def open(self):
        # 加载excel文件中的第一个sheet
        self.wb = load_workbook(self.path['source'])
        self.ws = self.wb.worksheets[0]
        # 统计总共多少行多少列
        self.nrows = self.ws.max_row
        self.ncols = self.ws.max_column
        # 商品计数
        self.items_counting = 1
        self.items_total = self.nrows - 1
        print('共有{}个商品'.format(self.items_total))

    def save(self):
        now = time.strftime('%m%d')
        self.path['filename'] = now + '已抓取_' + self.path['basename']
        self.path['target'] = os.path.join(self.path['dirname'], self.path['filename'])
        # 保存新表格
        self.wb.save(self.path['target'])
        print('''
        *************************************************************************
        完成!已保存到 {}
        *************************************************************************
        '''.format(self.path['target']))

    def get_index(self,
                  tm_url_tag='天猫网址',
                  tm_price_tag='天猫价',
                  jd_url_tag='京东网址',
                  jd_price_tag='京东价',
                  sku_tag='SKU',
                  name_tag='商品名称'):
        # 获取第一行表头的所有字段
        for i in range(self.ncols):
            self.fields.append(self.ws.cell(row=1, column=i + 1).value)
        # 确定所需字段在第几列
        self.index = {}
        self.index['tm_url'] = self.fields.index(tm_url_tag)
        self.index['tm_price'] = self.fields.index(tm_price_tag)
        self.index['jd_url'] = self.fields.index(jd_url_tag)
        self.index['jd_price'] = self.fields.index(jd_price_tag)
        self.index['sku'] = self.fields.index(sku_tag)
        self.index['name'] = self.fields.index(name_tag)


# 测试
if __name__ == '__main__':
    test = Excel()
    test.get_path()
    print(test.path)
    test.open()
    test.get_index()
    print(test.index)