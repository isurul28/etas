import re
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import subprocess

def extract_etas(text):
    pattern = r"Best Case Estimate: (\d{4}-\d{2}-\d{2})\nMost Likely Estimate: (\d{4}-\d{2}-\d{2})\nWorst Case Estimate: (\d{4}-\d{2}-\d{2})"
    match = re.search(pattern, text)
    if match:
        return match.groups()
    else:
        return None

def create_calendar_event(etas, ticket_id):
    cal = Calendar()
    cal.add('prodid', '-//ETAs Reminder//')
    cal.add('version', '2.0')

    estimates = ['Best Case', 'Most Likely', 'Worst Case']

    for i, eta in enumerate(etas):
        event = Event()
        estimate_description = f'{ticket_id} - {estimates[i]}'
        event.add('summary', estimate_description)
        event.add('description', 'Estimated Time of Arrival')
        event.add('dtstart', datetime.strptime(eta, '%Y-%m-%d'))
        event.add('dtend', datetime.strptime(eta, '%Y-%m-%d') + timedelta(days=1))

        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', 'Reminder')
        alarm.add('trigger', timedelta(minutes=-10))  # Set the trigger 10 minutes before the event

        event.add_component(alarm)
        cal.add_component(event)

    with open('eta_reminder.ics', 'wb') as f:
        f.write(cal.to_ical())

    print("Reminder events created.")
    return True

eta_text = []
print("Enter the ETA text (press Enter on an empty line to finish):")
while True:
    line = input()
    if not line:
        break
    eta_text.append(line)

eta_text = '\n'.join(eta_text)

etas = extract_etas(eta_text)
if etas:
    ticket_id = input("Enter the Ticket ID: ")
    if create_calendar_event(etas, ticket_id):
        subprocess.call(['xdg-open', 'eta_reminder.ics'])
else:
    print("ETAs not found in the text.")
