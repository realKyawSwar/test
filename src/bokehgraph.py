from bokeh.models import Panel, Tabs, ColumnDataSource
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.palettes import Category20c, Category10
from bokeh.transform import cumsum
from bokeh.layouts import row, gridplot
import pandas as pd
from math import pi

output_file("mhi.html")
df = pd.read_csv('All_eqt.csv', sep=';', index_col=False)
df.rename({"Unnamed: 0": "a"}, axis="columns", inplace=True)
df.drop(["a"], axis=1, inplace=True)
df.dropna(axis='columns')
df.Type = df.Type.astype(str)


# Get rid of LD and ULD and other types
def tidyUp(things):
    a = things.replace("ULD ", "").replace("LD ", "")
    b = a.replace("Xfer Arm", "Robot Arm").replace(
                      "PP Arm", "Robot Arm").replace(
                      "Epson ", "Epson Robot")
    c = b.replace("PP", "Brooks Robot").replace(
                      "Xfer", "Brooks Robot")
    return c.replace(
                      "DC(CVD) ", "").replace("DC ", "").replace(
                      "Etch ", "").replace("P0 ", "").replace(
                      "VS Mini", "Compressor").replace(
                      "V1000", "Compressor").replace("Y-VHF ", "").replace(
                      "Compressor V7", "Compressor")


def firstTab(df):
    df.Type = df.Type.astype(str)
    df.Type = df.Type.apply(tidyUp)
    line_df = df.groupby("Line").Line.count()
    temp = line_df.to_dict()
    data = pd.Series(temp).reset_index(name='Quantity').rename(
                     columns={'index': 'Line'})
    data['color'] = Category10[len(temp)]
    source = ColumnDataSource(data)
    p = figure(plot_width=800, plot_height=400,
               title="Overdue Equipment by Line",
               toolbar_location=None,
               tooltips=[("Line", "@Line"), ("Quantity", "@Quantity")])
    p.vbar(x='Line', top='Quantity', width=1, source=source,
           line_color="white", fill_color='color')
    columns = [TableColumn(field="Line", title="Lines"),
               TableColumn(field="Quantity", title="Overdue Quantity")]
    data_table = DataTable(source=source, columns=columns, width=200,
                           height=400, index_position=None)
    p.y_range.start = 0
    p.x_range.range_padding = 0.05
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Lines"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    type_df = df.groupby("Type").Type.count()
    temp1 = type_df.to_dict()
    data1 = pd.Series(temp1).reset_index(name='Quantity').rename(
                     columns={'index': 'Type'})
    data1['angle'] = data1['Quantity']/data1['Quantity'].sum() * 2*pi
    # data1['color'] = Category10[len(temp1)]
    # data1['color'] = Category20[len(temp1.items())]
    source1 = ColumnDataSource(data1)
    p1 = figure(plot_height=400, title="Pie Chart", toolbar_location=None,
                tools="hover", tooltips="@Type: @Quantity")
    p1.wedge(x=0, y=1, radius=0.425,
             start_angle=cumsum('angle', include_zero=True),
             end_angle=cumsum('angle'),
             line_color="white", fill_color='color', legend_group='Type',
             source=source1)
    columns1 = [TableColumn(field="Type", title="Type"),
                TableColumn(field="Quantity", title="Overdue Quantity")]
    data_table1 = DataTable(source=source1, columns=columns1, width=200,
                            height=400, index_position=None)
    p1.axis.axis_label = None
    p1.axis.visible = False
    p1.grid.grid_line_color = None
    grid = gridplot([[p, data_table], [p1, data_table1]], plot_width=550,
                    plot_height=400)
    return grid


def p2():
    p2 = figure(plot_width=300, plot_height=300)
    p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
    return p2


# tab1 = Panel(child=firstTab(df), title="Overdue Equipment Quantity by Line")
# # tab2 = Panel(child=piebyEqt(df), title="Overdue Equipment Quantity")
# tab3 = Panel(child=p2(), title="bars")
# # tabs = Tabs(tabs=[tab1, tab2, tab3])
# tabs = Tabs(tabs=[tab1, tab3])
# show(tabs)

# # # make a grid
# # grid = gridplot([[s1, s2], [None, s3]], plot_width=250, plot_height=250)
# # show(grid)

df.Type = df.Type.apply(tidyUp)
type_df = df.groupby("Type").Type.count().to_dict()
line_df = df.groupby("Line").Line.count().to_dict()
data = pd.Series(line_df).reset_index(name='Quantity').rename(
                 columns={'index': 'Line'})
data = data.to_dict("index").values()
data1 = pd.Series(type_df).reset_index(name='Quantity').rename(
                 columns={'index': 'Equipment'})
data1 = data1.to_dict("index").values()

print(data)
