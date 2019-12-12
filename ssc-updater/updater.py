import requests
from bs4 import BeautifulSoup
from fbchat import Client
from fbchat.models import *
import time
import json

sent = [False]
webhook_url = "INSERT SLACK WEBHOOK URL HERE"


def course_checker(dept, code, section, slot, slack_user):
    if sent[slot]==0:
        url = "https://courses.students.ubc.ca/cs/courseschedule?campuscd=UBC&pname=subjarea&tname=subj-section&course={code}&section={section}&dept={dept}".format(code = code, dept = dept, section = section)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h4')
        title = title.get_text()
        print(title)
        table = soup.find('table', attrs={'class':"'table"})

        # total remaining
        rows = table.find_all('tr')[0]
        total = rows.find_all('td')[1]
        total = ''.join(total.findAll(text=True))
        total_seats = "Total seats remaining     : " + total + "\n"

        # general remaining
        rows = table.find_all('tr')[2]
        general = rows.find_all('td')[1]
        general = ''.join(general.findAll(text=True))
        general_seats = "General seats remaining   : " + general + "\n"

        # restricted remaining
        rows = table.find_all('tr')[3]
        restricted = rows.find_all('td')[1]
        restricted = ''.join(restricted.findAll(text=True))
        restricted_seats = "Restricted seats remaining   : " + restricted + "\n"

        total = int(total, 10)
        if total > 0:
            # send notification
            slack_msg = {
                'text': slack_user + '\n' + dept + code + '—' + section + ' is available!\n\n' + total_seats + general_seats + restricted_seats
            }
            requests.post(webhook_url, data=json.dumps(slack_msg))
            sent[slot] = True


while True:
    course_checker("CPSC", "310", "102", 0, "<@nkawanto>")
    if all(item == 1 for item in sent):
        break
    # 5sec delay
    time.sleep(10)