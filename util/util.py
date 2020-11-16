import datetime

def parseTime(t):
    microsecond = 0
    second = 0
    minute = 0
    hour = 0
    time = tuple(t.split(sep=":"))
    s = time[len(time) - 1].split(sep=".")
    if len(s) > 1:
        microsecond = int(s[1].ljust(6, "0"))
    second = int(s[0])
    if len(time) > 1:
        minute = int(time[len(time) - 2])
    if len(time) > 2:
        hour = int(time[len(time) - 3])
    return datetime.time(hour=hour, minute=minute, second=second, microsecond=microsecond)

def format_delta(t):
    seconds = t.seconds
    microseconds = t.microseconds
    hours = seconds // 3600
    seconds = seconds - hours * 3600
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    value = ""
    if hours > 0:
        value += str(hours)
        value += ":"
    if hours > 0 or minutes > 9:
        value += str(minutes).rjust(2, "0")
        value += ":"
    else:
        if minutes > 0:
            value += str(minutes)
            value += ":"
    if hours > 0 or minutes > 0 or seconds > 9:
        value += str(seconds).rjust(2, "0")
    else:
        if seconds > 0:
            value += str(seconds)
    value += "."
    value += str(microseconds)[0]
    return value
