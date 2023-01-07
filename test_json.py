import pandas as pd 

# def abc(row):
#     if row['missin_month'] in 
#     print(type(row))
df= pd.read_csv('tes.csv',sep='|')
data =df.to_dict('records')

# df =df['2022-11' in df['Missing_month']]
# print(df)
print(df.explode('Missing_month'))
# a = '2022-12-02'
# print(a[0:7])