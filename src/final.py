from templater import DefaultTemplater
# from senders import Gmail
import pandas as pd
from datetime import datetime


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


def preprocess_df(df):
    df.rename({"Unnamed: 0": "a"}, axis="columns", inplace=True)
    df.drop(["a"], axis=1, inplace=True)
    df.dropna(axis='columns')
    df.Type = df.Type.astype(str)
    df.Type = df.Type.apply(tidyUp)
    df['Past Due'] = pd.to_timedelta(df['Past Due'])
    return df


def df_for_line(df, line, days_overdue):
    mask = (df['Line'].values == line) & (df['Past Due'] <= pd.Timedelta(days=days_overdue))
    return df[mask]


def line_select(df, line):
    temp_df = df.loc[df['Line'] == line]
    temp_dict = temp_df.groupby("Type").Type.count().to_dict()
    temp_dict['Line'] = line
    return temp_dict


def scatter_data(df, eqt):
    temp_df = df.loc[df['Type'] == eqt]
    temp_df['Past Due'] = temp_df['Past Due'].apply(lambda x: x.days)
    # temp_df['Date'] = temp_df['Date'].apply(lambda x: x[:10])
    temp_df['Due Date'] = temp_df['Due Date'].apply(lambda x: x[:10])
    temp_df.sort_values(by=['Past Due'], inplace=True)
    temp_df['Due Date'] = temp_df['Due Date'].map(str)
    temp_df = temp_df.drop(['Date'], axis=1)
    temp_df = temp_df.drop(['Past Due'], axis=1)
    temp = temp_df.to_dict("records")
    # print(temp_df['Past Due'])
    return temp


if __name__ == "__main__":
    templater = DefaultTemplater("template.html", "report.html")
    df = pd.read_csv('final.csv', sep=';', index_col=False)
    df = preprocess_df(df)
    df_203 = df_for_line(df, 203, -1000)
    line_df = df.groupby("Line").Line.count().to_dict()
    # print(line_df)
    type_df = df.groupby("Type").Type.count().to_dict()
    # print(type_df)
    data = pd.Series(line_df).reset_index(name='Quantity').rename(
                 columns={'index': 'Line'})
    # print(data)
    data1 = pd.Series(type_df).reset_index(name='Quantity').rename(
                 columns={'index': 'Equipment'})
    rowy = list(data1.to_dict("index").values())
    # print(rowy)
    pie_rows = sorted(rowy, key=lambda d: d['Quantity'], reverse=True)
    pie_columns = list(pie_rows[0].keys())
    pie_dimension = ['Equipment']
    pie_metrics = ['Quantity']
    hist_rows = [line_select(df, x) for x in [i for i in range(201, 212) if i != 206 and i != 207]]
    # print(hist_rows)
    hist_columns = [pie_rows[i]['Equipment'] for i in range(len(pie_rows))]
    hist_metrics = [pie_rows[i]['Equipment'] for i in range(len(pie_rows))]
    hist_columns.insert(0, "Line")
    hist_stack = {'whatever': hist_metrics}
    date = "'" + datetime.now().strftime("%d %B %Y %H:%M") + "'"
    print(date)
    eqt_list = list(type_df.keys())
    # scatter_rows = {"Cryopump": scatter_data(df, "Cryopump")}
    # print(scatter_rows)
    scatter_rows = {}
    for i in ['Bias', 'Brooks Robot', 'Carrier Force', 'Carrier Lock',
              'Compressor', 'Corner TDU', 'Cryopump', 'EGV Cylinder', 'Epson',
              'Orifice', 'PGV Cylinder', 'Process TDU', 'Robot Arm',
              'Robot Batteries', 'TDU Greasing', 'VAC Cylinder']:
    # for i in eqt_list:
        scatter_rows[i] = scatter_data(df, i)
    # print(scatter_rows)
    scatter_columns = ['Due Date', 'Line', 'Location']
    tags = {
        "date": date,
        "pie_metrics": pie_metrics,
        "pie_dimension": pie_dimension,
        "pie_rows": pie_rows,
        "pie_columns": pie_columns,
        "hist_metrics": hist_metrics,
        "hist_rows": hist_rows,
        "hist_columns": hist_columns,
        "hist_stack": hist_stack,
        "scatter_rows": scatter_rows,
        "scatter_columns": scatter_columns,
        "scatter_dimension": ['Due Date'],
        "scatter_metrics": ['Line', 'Location']
    }

    templater.render(tags)

    # with Gmail('kyaw.s.thein@gmail.com', '') as gmail:
    #     gmail.send('joshuakyaw@outlook.com', subject='your subject',
    #                body='your message', attachment="report.html")
