with open("log.log","r+") as logfile:
    log = logfile.readlines()
    
import datetime

def to_datetime (log, i):
    temp = log[i].split("->")
    dstring = temp[0].replace("[","").replace("]","").replace("/","-")
    dstring = dstring[0:len(dstring)-1]
    date = dstring.split(" ")[0]
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    time = dstring.split(" ")[1]
    datetime_date = year + "-" + month + "-" + day
    d = datetime.datetime.strptime(datetime_date + " " + time, '%Y-%m-%d %H:%M:%S')
    return d

start = to_datetime(log, 0)
end = to_datetime(log, len(log)-1)

db_size = 222.0 * 1000000.0 * 8 - 32.0 * 1000000.0 * 8
s = float ((end - start).total_seconds())
print db_size/s
