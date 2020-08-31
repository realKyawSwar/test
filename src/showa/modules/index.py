import pandas as pd
import config


df = pd.read_csv('final.csv', sep=';')
df1 = pd.read_csv('All_eqt.csv', sep=';')
df2 = df1.pivot_table(index=['Line'], aggfunc='size')
df2 = df1.pivot_table(index=['Line'])


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
                      "V1000", "Compressor").replace("Y-VHF ", "")


def calcIndex(df):
    df.Type = df.Type.apply(tidyUp)
    penalty = config.penalty
    data = pd.Series(penalty).reset_index(name='Penalty').rename(
                     columns={'index': 'Type'})
    df3 = pd.merge(df, data, how='inner', on='Type')
    df3.to_csv('grandfinal.csv', sep=';', index=True, mode='w')
    return df3


calcIndex(df)

# print(df2)
# print(df2.loc[201])
