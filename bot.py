# -*- coding: utf-8 -*-
from gcaltweet import GCalAPI, TwitterAPI
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
"""


"""


def gCalTweetBot(calIds):

    """
    Customize to change the bot behavior.
    ex: to tweet only events happening today,
    """

    gcal = GCalAPI()
    twitter = TwitterAPI()

    calendar = gcal.getCalendar(
        calIds,
        singleEvents=True,
        orderBy='startTime'
        )

    for event in calendar.events:
        tweet = calendar.formTweet(event)
        twitter.tweet(tweet)


if __name__ == "__main__":

    calIds = [
        ""
    ]

    sched = BlockingScheduler()

    sched.add_job(gCalTweetBot(calIds), 'cron', hour=6, minute=0, id="myCalendarbot")


    while True:
        pass
