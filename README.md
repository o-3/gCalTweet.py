**Warning!! **
Please be aware that this project is nicely working but incomplete for distribution.

gCalTweet.py
======================
Helps creating a bot to automatically tweet events from Google Calendar.

## Installation

    npm pip install


You need to create OAuthSettings.py file: 
````
settings = {
    'consumer_key': 'xxxx',
    'consumer_secret': 'xxxx',
    'access_token_key': 'xxxx',
    'access_token_secret': 'xxxx'
}
````

And get an OAuth Json Key file from https://console.developers.google.com/ and rename the downloaded file to "secret_json.json": 

In bot.py file, insert google your calendar IDs into calIds.

````
    calIds = [
        "xxx@group.calendar.google.com",
        "xxx@group.calendar.google.com"
    ]

````

## Usage

Test in the terminal and use cloud services like Heroku for deployment.
Modify ( gCalTweetBot(), GCalendar.formTweet(), etc... )  and schedulers as you want.
Happy coding! :)