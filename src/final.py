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


if __name__ == "__main__":
    templater = DefaultTemplater("template.html", "report.html")
    df = pd.read_csv('final.csv', sep=';', index_col=False)
    df = preprocess_df(df)
    df_203 = df_for_line(df, 203, -1000)
    line_df = df.groupby("Line").Line.count().to_dict()
    type_df = df.groupby("Type").Type.count().to_dict()
    # print(type_df)
    data = pd.Series(line_df).reset_index(name='Quantity').rename(
                 columns={'index': 'Line'})
    rows1 = list(data.to_dict("index").values())
    columns1 = list(rows1[0].keys())
    data1 = pd.Series(type_df).reset_index(name='Quantity').rename(
                 columns={'index': 'Equipment'})
    rowy = list(data1.to_dict("index").values())
    rows = sorted(rowy, key=lambda d: d['Quantity'], reverse=True)
    columns = list(rows[0].keys())
    metrics = ['Quantity']
    dimension = ['Equipment']
    dimension1 = ['Line']
    date = "'" + datetime.now().strftime("%d %B %Y %H:%M") + "'"
    print(date)
    tags = {
        # "date": "'August 2020'",
        "date": date,
        "metrics": metrics,
        "dimension": dimension,
        "rows": rows,
        "columns": columns,
        "metrics1": metrics,
        "dimension1": dimension1,
        "rows1": rows1,
        "columns1": columns1
    }

    templater.render(tags)

    # with Gmail('kyaw.s.thein@gmail.com', '') as gmail:
    #     gmail.send('joshuakyaw@outlook.com', subject='your subject',
    #                body='your message', attachment="report.html")

