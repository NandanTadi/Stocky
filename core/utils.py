import os

def dateToString(date):
    if date is None:
        return date.strftime("%Y%m%dT%H%M")
    else:
        return "null date"

def formatDateToHuman(date):
    if date is None:
        dt = datetime.strptime(date, "%Y%m%dT%H%M%S")
        return dt.strftime("%B %d, %Y, %I:%M:%S %p")
    else:
        return "null date"

