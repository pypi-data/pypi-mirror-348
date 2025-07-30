# """
# ガントチャート作成モジュール
# """
# import datetime
# from itertools import product

# import pandas as pd
# from dateutil.relativedelta import relativedelta
# from win32com.client import constants

# import xlviews as xv
# from xlviews.powerpoint.connector import add_connector
# from xlviews.powerpoint.layout import copy_layout
# from xlviews.powerpoint.main import Shape
# from xlviews.powerpoint.style import set_fill
# from xlviews.powerpoint.table import create_table
# from xlviews.utils import rgb


# def to_datetime(date):
#     if isinstance(date, str):
#         return datetime.datetime.strptime(date, '%Y/%m/%d')
#     elif isinstance(date, list):
#         return datetime.datetime(*date)
#     else:
#         return date


# def date_index(start, end, how):
#     if how in ['year', 'yearly']:
#         start = datetime.datetime(start.year, 4, 1)  # For FY
#         delta = relativedelta(end, start)
#         counts = delta.years
#         step = relativedelta(years=1)
#     elif how in ['quarterly']:
#         start = datetime.datetime(start.year, 4, 1)  # For FY
#         delta = relativedelta(end, start)
#         counts = (12 * delta.years + delta.months) // 3
#         step = relativedelta(months=3)
#     elif how in ['month', 'monthly']:
#         start = datetime.datetime(start.year, start.month, 1)
#         delta = relativedelta(end, start)
#         counts = 12 * delta.years + delta.months
#         step = relativedelta(months=1)
#     elif how in ['week', 'weekly']:
#         start -= relativedelta(days=start.weekday())  # To Monday
#         end -= relativedelta(days=end.weekday())  # To Monay
#         counts = (end - start).days // 7
#         step = relativedelta(days=7)
#     elif how in ['day', 'daily']:
#         counts = (end - start).days
#         step = relativedelta(days=1)
#     index = [start + k * step for k in range(counts + 2)]
#     return index


# def fiscal_year(date):
#     if 1 <= date.month <= 3:
#         return f'FY{date.year - 1}'
#     else:
#         return f'FY{date.year}'


# class GanttChart:
#     def __init__(self, start, end, how='weekly', index=None):
#         self.date_index = date_index(start, end, how)
#         self.start = self.date_index[0]
#         self.end = self.date_index[-1] - relativedelta(days=1)
#         self.date_index = self.date_index[:-1]
#         self.how = how

#         years = [fiscal_year(date) for date in self.date_index]
#         months = [date.month for date in self.date_index]
#         days = [date.day for date in self.date_index]
#         if how in ['year', 'yearly']:
#             columns = years
#         elif how in ['month', 'monthly', 'quarterly']:
#             columns = [years, months]
#         else:
#             columns = [years, months, days]

#         if index:
#             length = len(index)
#         else:
#             length = 1
#             index = ['']

#         empty = [[''] * len(self.date_index)] * length
#         df = pd.DataFrame(empty)
#         df.index = index
#         df.columns = columns
#         self.frame = df
#         self.name = '-'.join([self.start.strftime('%Y/%m/%d'),
#                               self.end.strftime('%Y/%m/%d'),
#                               self.how])

#     def set_slide(self, slide, left_margin=30, right_margin=30,
#                   top_margin=50, bottom_margin=50, index_width=80):
#         self.slide = slide
#         layout = slide.api.CustomLayout
#         if layout.Name != self.name:
#             for layout in slide.parent.api.SlideMaster.CustomLayouts:
#                 if layout.Name == self.name:
#                     slide.api.CustomLayout = layout
#                     break
#             else:
#                 self.create_frame(slide, left_margin=left_margin,
#                                   right_margin=right_margin,
#                                   top_margin=top_margin,
#                                   bottom_margin=bottom_margin,
#                                   index_width=index_width)
#                 return

#         for shape in layout.Shapes:
#             if shape.Name == self.name:
#                 shape = Shape(shape, parent=None)
#                 self.table = shape.table
#                 self.calc_scale()

#     def create_frame(self, slide, left_margin=30, right_margin=30,
#                      top_margin=50, bottom_margin=50, index_width=80):
#         layout = copy_layout(slide, name=self.name, replace=True)
#         width = layout.Width - left_margin - right_margin
#         height = layout.Height - top_margin - bottom_margin
#         columns_name = self.how in ['year', 'yearly']
#         shape = create_table(layout.Shapes, self.frame,
#                              columns_name=columns_name,
#                              left=left_margin, top=top_margin,
#                              width=width, height=height, preclean=False)
#         shape.api.Name = self.name
#         self.table = shape.table

#         table = self.table.api
#         table.FirstRow = False
#         table.HorizBanding = False
#         nrows = len(self.frame.columns.names)
#         ncols = len(self.frame.index.names)
#         for row, column in product(range(nrows), range(ncols)):
#             cell = table.Cell(row + 1, column + 1)
#             cell.Shape.Fill.Visible = False

#         columns_level = len(self.frame.columns.names)
#         if columns_level >= 2:
#             for cell in self.table.row(2):
#                 cell.shape.size = 10
#         if columns_level == 3:
#             for cell in self.table.row(3):
#                 cell.shape.size = 8

#         self.table.columns(1).width = index_width
#         column_width = (width - index_width) / len(self.frame.columns)
#         for k in range(len(self.frame.columns)):
#             self.table.columns(k + 2).width = column_width

#         columns_height = sum(self.table.rows(k + 1).height
#                              for k in range(columns_level))
#         index_height = height - columns_height
#         self.table.rows(len(self.frame) + columns_level).height = index_height

#         for column in range(len(self.frame.columns)):
#             color = (rgb(246, 250, 252) if column % 2 else rgb(246, 252, 246))
#             set_fill(table, (columns_level, column + 2),
#                      (columns_level + 1, column + 2), color)
#             cell = self.table.cell(columns_level, column + 2)
#             text_frame2 = cell.shape.api.TextFrame2
#             text_frame2.MarginBottom = 0
#             text_frame2.MarginTop = 0
#             text_frame2.MarginLeft = 0
#             text_frame2.MarginRight = 0

#         self.calc_scale()

#     def calc_scale(self):
#         columns_level = len(self.frame.columns.names)
#         self.left = self.table.cell(1, 2).left
#         self.top = self.table.cell(columns_level + 1, 2).top
#         end = self.table.left + self.table.parent.width
#         self.day_width = (end - self.left) / ((self.end - self.start).days + 1)
#         self.bottom = self.table.top + self.table.parent.height
#         self.height = self.bottom - self.top

#     def to_position(self, date, offset=0.5):
#         return ((date - self.start).days + offset) * self.day_width + self.left

#     def to_date(self, position, offset=0.5):
#         days = round((position - self.left) / gc.day_width - offset)
#         return self.start + relativedelta(days=days)

#     def add_point(self, date, y, width=10, height=None, text='day', shape='r',
#                   size=10, **kwargs):
#         if isinstance(shape, str):
#             shape = {'r': 5, 'd': 4, '^': 7, 'o': 9}[shape]
#         if height is None:
#             height = width
#         left = self.to_position(date) - width / 2
#         top = y * self.height + self.top - height / 2

#         if text == 'day':
#             text = str(date.day)

#         shape = self.slide.shapes.add_shape(shape, left, top, width, height,
#                                             text=text, italic=False, size=size,
#                                             **kwargs)
#         shape.api.Name = 'gantt_point'
#         shape.api.Fill.Solid()
#         shape.api.Shadow.Visible = False

#         if text:
#             text_frame2 = shape.api.TextFrame2
#             text_frame2.VerticalAnchor = constants.msoAnchorMiddle
#             paragraph_format = text_frame2.TextRange.ParagraphFormat
#             paragraph_format.Alignment = constants.msoAlignCenter
#             text_frame2.MarginBottom = 0
#             text_frame2.MarginTop = 0
#             text_frame2.MarginLeft = 0
#             text_frame2.MarginRight = 0
#             shape.api.TextFrame.TextRange.Font.Shadow = False

#         return shape

#     def add_line(self, start, end, y, height=10, text=None, **kwargs):
#         shape = 5
#         left = self.to_position(start, offset=0)
#         right = self.to_position(end, offset=1)
#         width = right - left
#         top = y * self.height + self.top - height / 2

#         shape = self.slide.shapes.add_shape(shape, left, top, width, height,
#                                             text=text, italic=False, **kwargs)
#         shape.api.Name = 'gantt_line'
#         shape.api.Fill.Solid()
#         shape.api.Shadow.Visible = False

#         if text:
#             text_frame2 = shape.api.TextFrame2
#             text_frame2.VerticalAnchor = constants.msoAnchorMiddle
#             paragraph_format = text_frame2.TextRange.ParagraphFormat
#             paragraph_format.Alignment = constants.msoAlignCenter
#             text_frame2.MarginBottom = 0
#             text_frame2.MarginTop = 0
#             text_frame2.MarginLeft = 0
#             text_frame2.MarginRight = 0
#             shape.api.TextFrame.TextRange.Font.Shadow = False

#         return shape

#     def add_connector(self, s1, s2, **kwargs):
#         connector = add_connector(s1, s2, **kwargs)
#         connector.Name = 'gantt_connector'
#         return connector


# if __name__ == '__main__':
#     pp = xv.PowerPoint()
#     slide = pp.slides(1)
#     start = datetime.datetime(2018, 7, 1)
#     end = datetime.datetime(2018, 7, 30)
#     gc = GanttChart(start, end, 'daily')
#     gc.set_slide(slide)
#     gc.frame
#     gc.end

#     s1 = gc.add_point(gc.start, 0.5, 20, fill_color=rgb(255, 230, 210),
#                       line_color=rgb(0, 0, 0), line_weight=1)
#     s2 = gc.add_point(gc.end, 0.5, 20, fill_color=rgb(255, 230, 210),
#                       line_color=rgb(0, 0, 0), line_weight=1)

#     connector = gc.add_connector(s1, s2, weight=3, direction='vertical',
#                                  begin_arrow=True)

#     gc.add_line(datetime.datetime(2018, 5, 7),
#                 datetime.datetime(2023, 9, 30), 0.5)

#     s1.api.Name

#     slide.shapes.api.Count
#     shape = slide.shapes(3)
#     gc.to_date(shape.left)

#     connector.ConnectorFormat.BeginConnectedShape.Name
#     connector.Type
#     constants.msoConnectorStraingt
