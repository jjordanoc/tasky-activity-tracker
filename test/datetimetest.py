import datetime
import pytz

x = datetime.date(2016, 10, 12)
today = datetime.date.today()
print(x.day-today.day)




















"""
# Get current date y-m-d
d = datetime.date.today()
# Print the whole date
print(d)
# Print days
print(d.day)
# Print month
print(d.month)
# Print year
print(d.year)
# Print index of week
print(d.isoweekday())

# Set timedelta of a week
td = datetime.timedelta(days=7)
# Add delta
print(d + td)
# Subtract delta
print(d - td)

bday = datetime.date(2021, 9, 15)

till_bday = bday - d
print(till_bday)
"""
"""
dt = datetime.datetime.today()
dt_now = datetime.datetime.now()
dt_utcnow = datetime.datetime.utcnow()
print(dt)
print(dt_now)
print(dt_utcnow)
"""