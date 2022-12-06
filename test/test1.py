import datetime
today = datetime.date.today()
t='2022-12-07'
print(today.strftime('%Y-%m-%d')==t)
print(today==t)