# -*- coding: utf-8 -*-
from gcaltweet import GCalAPI, TwitterAPI
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
"""


"""


def gCalTweetBot():

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
        "j6hvnb2e7jdhcu19tltl24q0lo@group.calendar.google.com"
    ]

    gCalTweetBot()

    # sched = BlockingScheduler()

    # sched.add_job(tweetBot(), 'cron', hour=6, minute=0, id="myCalendarbot")


    # while True:
    #     pass
