import csv
import pandas as pd
import requests
import json
from google.colab import files
from IPython.display import clear_output
 
col = ['URLs', 'Device Type', 'Score', 'First Contentful Paint (s)', \
           'Speed Index (s)', 'Largest Contentful Paint (s)',\
            'Time to Interactive (s)', 'Total Blocking Time (ms)', 'Cumulative Layout Shift']
 
df = pd.DataFrame(columns=col)
 
device_type = ['mobile', 'desktop']
category = 'performance'

urls = ['Your url list goes here...']
 
i = 1
for device in (device_type):
    row = []
    for url in urls:
        clear_output(wait=True)
        print(f' \n Fetching {device} data for url: {url} : {i} / {len(urls)*len(device_type)}')
        contents = requests.get(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={device}&category={category}')
        data = contents.json()
        Score = data['lighthouseResult']['categories']['performance']['score']*100
        first_contentful_paint = data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
        Speed_Index = data['lighthouseResult']['audits']['speed-index']['displayValue']
        Largest_Contentful_Paint = data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
        interactive = data['lighthouseResult']['audits']['interactive']['displayValue']
        Total_Blocking_Time = data['lighthouseResult']['audits']['total-blocking-time']['displayValue']
        Cumulative_Layout_Shift = data['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
        df_row = url, device, Score, first_contentful_paint, Speed_Index, Largest_Contentful_Paint,\
                    interactive, Total_Blocking_Time, Cumulative_Layout_Shift
        df.loc[i] = df_row
        row.append(df_row)
        i += 1
    print()
    print(row)
 
df['First Contentful Paint (s)'] = df['First Contentful Paint (s)'].str.extract(r'(\d+.\d+)', expand = True)
df['Speed Index (s)'] = df['Speed Index (s)'].str.extract(r'(\d+.\d+)', expand = True)
df['Largest Contentful Paint (s)'] = df['Largest Contentful Paint (s)'].str.extract(r'(\d+.\d+)', expand = True)
df['Time to Interactive (s)'] = df['Time to Interactive (s)'].str.extract(r'(\d+.\d+)', expand = True)
df['Total Blocking Time (ms)'] = df['Total Blocking Time (ms)'].str.extract(r'(\d+)', expand = True)
 

 
df.to_csv("page_speed_data.csv")

try:
    files.download("page_speed_data.csv")
    print("\n File Downloaded")
except:
    print(f' Kindly Download your file from the left nav folder. File name is "page_speed_data.csv"')
