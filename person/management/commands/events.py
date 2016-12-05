# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from icalendar import Calendar, Event
from icalendar.prop import vText
from datetime import datetime
from pytz import timezone # timezone
import requests, os


class Command(BaseCommand):
    def handle(self, *args, **options):
        URL = r'http://contests.acmicpc.info/contests.json'
        TZ = timezone('Asia/Shanghai')

        cal = Calendar()
        cal.add('prodid', '-//ACM EVENTS CALENDAR//WHUACM TEAM//')
        cal.add('version', '2.0')
        events = requests.get(URL).json()

        for item in events:
            event = Event()
            fmt = '%Y-%m-%d %H:%M:%S'
            time = datetime.strptime(item['start_time'], fmt).replace(tzinfo=TZ)
            event.add('dtstart', time)
            event.add('summary', item['name'])
            event['location'] = vText(item['oj'])
            event['uid'] = item['id'] + '@whuctf.org'
            cal.add_component(event)
        print '%d events checked' % len(events)
        f = open(os.path.join(settings.MEDIA_ROOT, 'acmevents.ics'), 'wb')
        f.write(cal.to_ical())
        f.close()
