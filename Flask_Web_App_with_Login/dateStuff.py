from datetime import datetime,timedelta,timezone

a = datetime.now(timezone(timedelta(hours=-4),name="EST"))
print(a)
b = datetime(2021,5,4)
d = datetime(2021,7,3)
print(a.month,a.day,a.year)

c = d-b
print(c.days)

print(a.hour,a.minute,a.second)

a = 12.393
b = round(a,2)
print(b)

print(f'${a:.2f}')

my_var = "2020-04"

my_tup = my_var.split(sep="-")