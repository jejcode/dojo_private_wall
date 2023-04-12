# apply jinja filters here
from flask_app import app
import datetime

# code function attributed to:
# https://shubhamjain.co/2018/12/22/how-to-render-human-readable-time-in-jinja/
# comments are mine trying to figure out how this function is working
@app.template_filter('humanize')
def humanize_date(db_date):
    now = datetime.datetime.now()
    diff = now - db_date
    second_diff = diff.seconds # convert to seconds the difference between now and date posted
    day_diff = diff.days # convert to day the difference between now and posting date

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10: # less than ten seconds
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago" # less than 60 seconds
        if second_diff < 120:
            return "a minute ago" # less than 2 minutes or between 1 and 2 minutes
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago" # between 2 minutes and an hour
        if second_diff < 7200: # between on and two hours
            return "an hour ago"
        if second_diff < 86400: # between two hours and 24 hours
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1: # greater than 24 hours  equals a day
        return "Yesterday"
    if day_diff < 7: # if less than a week
        return str(day_diff) + " days ago"
    if day_diff < 31: # if less than a month
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365: # if less than a year
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago" # or else it is just years ago