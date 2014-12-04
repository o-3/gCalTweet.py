# -*- coding: utf-8 -*-

import json
from datetime import datetime
import pytz

import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.file import Storage

import tweepy
from OAuthSettings import settings


class GCalAPI:

    def __init__(self):
        self.calendars = []
        self.events = []
        self.service = ""

        storage = Storage('calendar.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            # !!change this
            with open("secret_json.json") as f:
                jf = json.load(f)
                private_key = jf['private_key']
                client_email = jf['client_email']

            credentials = SignedJwtAssertionCredentials(
                client_email,
                private_key,
                'https://www.googleapis.com/auth/calendar.readonly'
                )
            storage.put(credentials)

        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build(
            serviceName='calendar',
            version='v3',
            http=http)

        if(self.service):
            print("success: Oauth authorization")

    def getCalendar(self, gcalIds, *args, **kwargs):

        s = self.service
        for cid in gcalIds:
            gcal = GCalendar()
            page_token = None

            currentTime = datetime.strftime(
                datetime.now(),
                '%Y-%m-%dT%H:%M:%SZ'
                )

            while True:
                calData = s.events().list(
                    calendarId=cid,
                    pageToken=page_token,
                    timeMin=currentTime,
                    *args,
                    **kwargs
                ).execute()
                gcal.name = calData.get('summary')
                gcal.timezone = calData.get('timeZone')
                for e in calData['items']:
                    gcal.eventData.append(e)
                    # print(e)
                page_token = calData.get('nextPageToken')
                if not page_token:
                    break
            gcal.initialize()
            self.calendars.append(gcal)
            return gcal

    def getCalendars(self):
        return self.calendars


class GCalendar:

    def __init__(self):
        self.name = ""
        self.eventData = []
        self.events = []
        self.timezone = ""
        self.tweetFormat = "[{7}]\ntitle: {0}\n{1}\nwhere: {2}\nstart: {3}\nend: {4}\ncreated: {5}\nupdated: {6}\n"
        self.timeFormat = "%y/%m/%d %H:%M"

    def initialize(self):
        for data in self.eventData:
            g = GEvent(data, self.timezone)
            self.events.append(g)

    """
        Customize to change tweet format.
    """
    def formTweet(self, gEvent, *args, **kwargs):

        tweetFormat = self.tweetFormat
        timeFormat = self.timeFormat

        if(kwargs.get('tweetFormat')):
            tweetFormat = kwargs.get('tweetFormat')
        if(kwargs.get('timeFormat')):
            timeFormat = kwargs.get('timeFormat')

        calendarName = self.name.encode("utf-8")
        title = gEvent.title.encode("utf-8")
        description = gEvent.description.encode("utf-8")
        location = gEvent.location.encode("utf-8")
        # timeDurationFormat(gEvent.start, gEvent.end,gEvent.isAllDay,timeFormat)
        start = gEvent.start.strftime(timeFormat)
        end = gEvent.end.strftime(timeFormat)
        created = gEvent.created.strftime(timeFormat)
        updated = gEvent.updated.strftime(timeFormat)
        htmlLink = gEvent.htmlLink

        if(kwargs.get('limit')):
            limit = kwargs.get('limit')
            title = limitText(title, limit)
            description = limitText(description, limit)
            location = limitText(location, limit)
        else:
            if(kwargs.get('titleLimit')):
                title = limitText(title, kwargs.get('titleLimit'))
            if(kwargs.get('descLimit')):
                description = limitText(description, kwargs.get('descLimit'))
            if(kwargs.get('locateLimit')):
                location = limitText(location, kwargs.get('locateLimit'))

        tweet = tweetFormat.format(
            title,
            description,
            location,
            start,
            end,
            created,
            updated,
            calendarName
            )

        if(kwargs.get('htmlLink', False) is True):
            tweet = limitText(tweet, 115)
            tweet += "\n"
            tweet += str(htmlLink)
        else:
            tweet = limitText(tweet, 139)

        return tweet


def limitText(text, limit):
    text = unicode(text, "utf-8")
    if(len(text) > limit):
        text = text[:limit] + u"…"
    return text.encode("utf-8")


def timeDurationFormat(start, end, isAllDay, timeFormat):
    if (start.year != end.year):
        return start.strftime(timeFormat)+' - ' + end.strftime(timeFormat)
    if (start.month != end.month):
        return start.strftime(timeFormat)+' - ' + end.strftime(timeFormat)


class GEvent:

    def __init__(self, data, timezone):
        self.title = data.get('summary', u'No title')
        self.timezone = timezone
        self.description = data.get('description', u'-')
        self.location = data.get('location', u'-')
        self.htmlLink = data.get('htmlLink')
        if(data.get('start').get('date')):
            self.isAllDay = True
            self.start = formatTime(data.get('start').get('date'), timezone)
            self.end = formatTime(data.get('end').get('date'), timezone)
        else:
            self.isAllDay = False
            self.start = formatTime(data.get('start').get('dateTime'), timezone)
            self.end = formatTime(data.get('end').get('dateTime'), timezone)
        self.created = convertTime(data.get('created'), timezone)
        self.updated = convertTime(data.get('updated'), timezone)


def formatTime(timeStr, timezone):
    time_zone = pytz.timezone(timezone)
    if len(timeStr) > 10:
            timeStr = timeStr[0:19]
            tm = datetime.strptime(
                timeStr,
                '%Y-%m-%dT%H:%M:%S'
                ).replace(tzinfo=time_zone)
            return tm
    else:
        tm = datetime.strptime(
            timeStr,
            '%Y-%m-%d'
            ).replace(tzinfo=time_zone)
        return tm


def convertTime(timeStr, timezone):
    if len(timeStr) > 10:
            timeStr = timeStr[0:19]
            tm = datetime.strptime(
                timeStr,
                '%Y-%m-%dT%H:%M:%S'
                ).replace(tzinfo=pytz.utc)
            tm = tm.astimezone(pytz.timezone(timezone))
            return tm
    else:
        tm = datetime.strptime(timeStr, '%Y-%m-%d').replace(tzinfo=pytz.utc)
        tm = tm.astimezone(pytz.timezone(timezone))
        return tm


class TwitterAPI:

    def __init__(self):
        consumer_key = settings['consumer_key']
        consumer_secret = settings['consumer_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = settings['access_token_key']
        access_token_secret = settings['access_token_secret']
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(message)
        print("%s" % message)
