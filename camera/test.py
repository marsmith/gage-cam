import datetime

def checkIfDark():
    start = datetime.time(22, 0, 0)
    end = datetime.time(4, 0, 0)
    now = datetime.datetime.now().time()
    if start <= end:
        return start <= now <= end
    else:
        return start <= now or now <= end

print 'is it dark:', checkIfDark()