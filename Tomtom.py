#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: filetype=python


import pandas as pd
import datetime as dt
import time
import numpy as np
import requests
import os
os.chdir('k:/')


def main():

    prefix = 'https://api.midway.tomtom.com/ranking/liveHourly/'

    target = {
        'FRA%2FCircle%2Fparis': {'country': 'France', 'location': 'Paris'},
        'ITA%2FCircle%2Fmilan': {'country': 'Italy', 'location': 'Milan'},
        'DEU%2FCircle%2Ffrankfurt-am-main': {
            'country': 'Germany',
            'location': 'Frankfurt',
        },
        'GBR%2FCircle%2Flondon': {'country': 'United Kingdom', 'location': 'London'},
        'USA%2FCircle%2Fnew-york': {'country': 'United States', 'location': 'New York'},
        'JPN%2FCircle%2Ftokyo': {'country': 'Japan', 'location': 'Tokyo'},
        'AUS%2FCircle%2Fsydney': {'country': 'Australia', 'location': 'Sydney'},
        'ESP%2FCircle%2Fmadrid': {'country': 'Spain', 'location': 'Madrid'},
        'USA%2FCircle%2Flos-angeles': {
            'country': 'United States',
            'location': 'Los Angeles',
        },
        'USA%2FCircle%2Fseattle': {'country': 'United States', 'location': 'Seattle'},
    }

    historic_avg = {
        'Frankfurt': {
            0: 14.828168159761104,
            1: 18.556550951847704,
            2: 18.764821684086105,
            3: 20.81831114679017,
            4: 15.212893625192013,
            5: 9.440824468085108,
            6: 5.451007326007326,
        },
        'London': {
            0: 21.20389254385965,
            1: 25.025871360582304,
            2: 25.890477245862883,
            3: 27.638587079798576,
            4: 24.563016917293233,
            5: 18.371318922305765,
            6: 14.034886809414841,
        },
        'Los Angeles': {
            0: 18.081597222222225,
            1: 24.602430555555554,
            2: 27.961805555555557,
            3: 29.181798245614033,
            4: 27.713230861965037,
            5: 23.43154761904762,
            6: 13.758666928309788,
        },
        'Madrid': {
            0: 12.490570175438597,
            1: 13.618031189083823,
            2: 14.09101382667662,
            3: 14.179331140350877,
            4: 12.251941150954309,
            5: 4.372204447288434,
            6: 2.938329142699487,
        },
        'Milan': {
            0: 16.595997807017547,
            1: 19.678281697150677,
            2: 20.116642559412714,
            3: 21.798127320117878,
            4: 20.93199688049912,
            5: 11.182520463392523,
            6: 7.4401126039613885,
        },
        'New York': {
            0: 16.63888888888889,
            1: 20.151041666666668,
            2: 20.938764732923374,
            3: 22.204457295793247,
            4: 21.864376130198917,
            5: 14.28361528822055,
            6: 10.565672422815279,
        },
        'Paris': {
            0: 22.678165437974368,
            1: 27.70737293144208,
            2: 27.65354658845982,
            3: 29.25440264472295,
            4: 28.879417293233082,
            5: 15.110823934837091,
            6: 11.962517707311758,
        },
        'Seattle': {
            0: 12.897569444444445,
            1: 19.878472222222225,
            2: 21.339887521222412,
            3: 22.007419590643277,
            4: 19.98502486437613,
            5: 15.204010025062656,
            6: 8.828100470957613,
        },
        'Sydney': {
            0: 16.886235062293416,
            1: 19.2371895783413,
            2: 20.033814183747694,
            3: 20.24800293601769,
            4: 17.27066753884507,
            5: 13.693233082706767,
            6: 12.606057987711214,
        },
        'Tokyo': {
            0: 22.880642162471393,
            1: 24.30436652357845,
            2: 23.2880849082068,
            3: 25.036028679855665,
            4: 26.748143194524776,
            5: 22.496804511278196,
            6: 15.289682095309194,
        }}

    for url in target:

        time.sleep(5)
        print(url)
        session=requests.Session()
        page = session.get(prefix + url,verify=False)

        rawdata = page.json()
        try:
            # json keys
            cols = rawdata['data'][0].keys()
        except IndexError :
            continue

        # add some missing column
        for i in range(len(rawdata['data'])):
            for j in cols:
                if j not in rawdata['data'][i].keys():
                    rawdata['data'][i][j] = np.nan

        df = pd.DataFrame()

        # fill in data
        for col in cols:
            df[col] = [i[col] for i in rawdata['data']]

        # there is only system time
        t0 = dt.datetime(1970, 1, 1, 1, 44)

        # convert system time to real time
        df['datetime'] = [
            t0 + dt.timedelta(minutes=i / 60000) for i in df['UpdateTime'].tolist()
        ]

        # change column name
        df.columns = df.columns.str.replace('TrafficIndexLive', 'LiveCongestion')
        df.columns = df.columns.str.replace(
            'TrafficIndexHistoric', 'LastYearAverageCongestion'
        )

        df['location'] = target[url]['location']
        df['country'] = target[url]['country']

        # get daily average
        df['datetime'] = pd.to_datetime(df['datetime'])

        datelist = set(df['datetime'].dt.date)

        df.set_index('datetime', inplace=True)

        df['LiveCongestionDaily'] = np.nan
        df['LastYearAverageCongestionDaily'] = np.nan

        for i in datelist:
            df['LiveCongestionDaily'][
                i.strftime('%Y-%m-%d') : i.strftime('%Y-%m-%d')
            ] = df['LiveCongestion'][
                i.strftime('%Y-%m-%d') : i.strftime('%Y-%m-%d')
            ].mean()
            if "LastYearAverageCongestion" in df.columns:
                df['LastYearAverageCongestionDaily'][
                    i.strftime('%Y-%m-%d') : i.strftime('%Y-%m-%d')
                ] = df['LastYearAverageCongestion'][
                    i.strftime('%Y-%m-%d') : i.strftime('%Y-%m-%d')
                ].mean()
            # if no historic, use historic avg
            else:
                df['LastYearAverageCongestionDaily'][
                    i.strftime('%Y-%m-%d') : i.strftime('%Y-%m-%d')
                ] = historic_avg[target[url]['location']][dt.datetime.weekday(i)]

        df.reset_index(inplace=True)

        df.to_csv(f'{target[url]["location"]}.csv')

    return


if __name__ == "__main__":
    main()
