# from showa.lib import logs
from showa.modules import combinedEqt, gvcylinder, cryopump
import pandas as pd
import time


start_time = time.time()


def getALLeqt():
    try:
        finalEqtList = (gvcylinder.allLinesGV(), combinedEqt.getEqt(),
                        cryopump.getCryo())
        finalEqt = pd.DataFrame(columns=['Line', 'Location', 'Type', 'Date',
                                         'Due Date'])
        for i in finalEqtList:
            finalEqt = pd.concat([finalEqt, i])
        finalEqt = finalEqt.reset_index(drop=True)
        # add Due date
        today = pd.Timestamp.now().normalize()
        finalEqt['Past Due'] = finalEqt['Due Date'] - today
        # add regen
        finalEqt.Line.astype(int)
        # df2 = regen.regenize()
        # df3 = pd.merge(finalEqt, df2, how='right', on='Line')
    except Exception as e:
        print(e)
    # return df3
    return finalEqt


def evaluate_Due(df):
    mask1 = df['Past Due'] <= pd.Timedelta(0)
    ng = df.loc[mask1]
    return ng


# def plan():
#     x = getALLeqt()
#     x.to_csv('All_eqt.csv', sep=';', index=True, mode='w')
#     df = evaluate_Due(x)
#     df.to_csv('final.csv', sep=';', index=True, mode='w')
#     return df


def main():
    # logs.initLogger(logLevel=logs.LEVEL_DEBUG)
    x = getALLeqt()
    # x.to_csv('All_eqt.csv', sep=';', index=True, mode='w')
    df = evaluate_Due(x)
    df.to_csv('final.csv', sep=';', index=True, mode='w')
    # logs.closeLogger()


if __name__ == '__main__':
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
