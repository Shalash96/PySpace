import requests
from bs4 import BeautifulSoup as bs 
from prettytable import PrettyTable
import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-y', type=int, required=True, help='Specify the year you want to know about its astronomy events')
args = parser.parse_args()

year = args.y

def app():
    yearLink = f"http://www.seasky.org/astronomy/astronomy-calendar-{year}.html"
    req = requests.get(yearLink)

    soup = bs(req.text, 'html.parser')
    dates = []
    events = []

    for event in soup.select("li p"):
        date_of_event, details = event.text.split('-', 1) # get date of events
        name_of_event, berif_info = details.split('.', 1) # get names of events and berif information
        dates.append(date_of_event)
        events.append(name_of_event)

    t = PrettyTable()
    t.field_names = ['Event', 'Date', 'Status']
    for event, date in zip (events, dates):
        date = f'{date.split(",")[0]}, {year}'

        try:
            datetime_str = datetime.datetime.strptime(date, '%B %d, %Y')
        except:
            datetime_str = datetime.datetime.strptime(date, '%B %d , %Y')

        status = f'Coming in {(datetime_str.date() - datetime.date.today()).days} days' if datetime_str.date() > datetime.date.today() else 'Event Passed'
        t.add_row([event, datetime_str.date(), status])
        t.add_row(['-*'*15,'-*'*10,'-*'*10])


    print(t)
    print('Made with love by @ShalashOfficial')


app()


