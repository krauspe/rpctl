import datetime

now = datetime.datetime.now()

if now.month == 3 and now.day == 31:
    print "yes"
else:
    print "no"

print "now.day is  %s " % (type(now.day))
print "now.month is  %s " % (type(now.month))

