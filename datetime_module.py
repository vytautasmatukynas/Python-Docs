import datetime as dt

current_date = dt.datetime.now()
year = current_date.year
month = current_date.month
day = current_date.day
hour = current_date.hour
weekday = current_date.weekday()

print(current_date)
print(year, month, day, hour)
print(weekday)

date_of_kebabas = dt.datetime(year=2020, month=5, day=25, hour=5, minute=25, second=27)

print(date_of_kebabas)
