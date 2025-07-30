# from win32com.client import constants

# from xlviews.utils import rgb


# def add_connector(s1, s2, begin_arrow=False, end_arrow=False, weight=1.5,
#                   color=rgb(0, 0, 0), arrowhead=None, direction='horizontal'):
#     shapes = s1.api.Parent.Shapes
#     if s1.top == s2.top and s1.height == s2.height:
#         connector_type = constants.msoConnectorStraight
#         if s1.left < s2.left:
#             begin, end = 4, 2
#         else:
#             begin, end = 2, 4
#     elif s1.left == s2.left and s1.width == s2.width:
#         connector_type = constants.msoConnectorStraight
#         if s1.top < s2.top:
#             begin, end = 3, 1
#         else:
#             begin, end = 1, 3
#     else:
#         connector_type = constants.msoConnectorElbow
#         if direction == 'horizontal':
#             if s1.left < s2.left:
#                 begin, end = 4, 2
#             else:
#                 begin, end = 2, 4
#         else:
#             if s1.top < s2.top:
#                 begin, end = 3, 1
#             else:
#                 begin, end = 1, 3

#     if s1.api.ConnectionSiteCount == 8:
#         begin = 2 * begin - 1
#     if s2.api.ConnectionSiteCount == 8:
#         end = 2 * end - 1

#     connector = shapes.AddConnector(connector_type, 1, 1, 2, 2)
#     connector.ConnectorFormat.BeginConnect(s1.api, begin)
#     connector.ConnectorFormat.EndConnect(s2.api, end)
#     connector.Line.Weight = weight
#     connector.Line.ForeColor.RGB = color

#     if begin_arrow:
#         if begin_arrow is True:
#             begin_arrow = constants.msoArrowheadOpen
#         else:
#             begin_arrow = hasattr(constants, 'msoArrowhead' + begin_arrow)
#         connector.Line.BeginArrowheadStyle = begin_arrow
#     return connector


# if __name__ == '__main__':
#     import xlviews as xv
#     import datetime
#     from xlviews.powerpoint.gantt import GanttChart

#     pp = xv.PowerPoint()
#     slide = pp.slides(3)
#     start = datetime.datetime(2018, 5, 3)
#     end = datetime.datetime(2018, 6, 10)
#     gc = GanttChart(start, end, 'weekly')
#     gc.set_slide(slide)

#     s1 = gc.add_point('o', datetime.datetime(2018, 5, 8), 0.5, 20,
#                       fill_color=rgb(255, 230, 210), line_color=rgb(0, 0, 0),
#                       line_weight=1, text='day')

#     s2 = gc.add_point('r', datetime.datetime(2018, 5, 28), 0.8, 16,
#                       fill_color=rgb(255, 230, 210), line_color=rgb(0, 0, 0),
#                       line_weight=1, size=10)

#     connector = add_connector(s1, s2, weight=3, direction='vertical',
#                               begin_arrow=True)
