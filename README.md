Craigslist For Sale Alerts
-------------------

Craigslist For Sale Alerts is a bot that will scrape Craigslist for real-time for sale postings matching specific criteria. When it finds a listing that it hasn't already seen, it will alert you via Slack and/or Email.

It can optionally read from an external JSON list of search URLs so that search criteria can be updated independently. 

This project is adapted from [apartment finder](https://github.com/VikParuchuri/apartment-finder) by Vik Paruchuri.

Settings
--------------------

Look in `settings.py` for the list of configuration options. The options are:

 * LISTING_URLS_JSON - optionally, a URL to a JSON array with the Craigslist searches you want to alert on
 * LISTING_URLS - the harcoded Craigslist searches you want to alert on
 * SLEEP_INTERVAL - How long we should sleep between scrapes of Craigslist in seconds
 * SMTP_SERVER - The SMTP server to use send email alerts
 * SMTP_PORT - The SMTP port to use send email alerts
 * SMTP_USERNAME - The SMTP username to use send email alerts
 * SMTP_PASSWORD - The SMTP password to use send email alerts
 * EMAIL_RECIPIENT - The address where you want to receive email alerts
 * SLACK_TOKEN - The token that allows us to connect to Slack
 * SLACK_CHANNEL - the Slack channel you want the bot to post in
 * DMS_URL - Optional Dead Man's Snitch URL used for monitoring


Deployment
--------------------

    # copy all files to server
    scp *.py user@domain:/path/to/project/directory
    scp listings.db user@domain:/path/to/project/directory

    # install modules
    pip install -r requirements.txt

    # set permissions
    chmod +x main_loop.py
    chmod +x scraper.py
    chmod +x settings.py
    chmod +x util.py
    chmod +x listings.db

    # start as service
    nohup python main_loop.py &

    # find it again
    ps ax | grep main_loop.py

    # kill it 
    kill -9 process-id



Testing
--------------------

The `remove_listing.py` file is useful for testing your alerts and allows you to easily delete a record from your local database to make sure your alert fires as you expect. Also, it displays the most recent 15 items in your local database for debugging purposes. You must know the Craigslist ID to be able to delete the record.


