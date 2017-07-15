Craigslist For Sale Alerts
-------------------

Craigslist For Sale Alerts is a bot that will scrape Craigslist for real-time for sale postings matching specific criteria. When it finds a listing that it hasn't already seen, it will alert you via Slack and/or Email.

It can optionally read from an external JSON list of search URLs so that search criteria can be updated independently. 

This project is adapted from [apartment finder](https://github.com/VikParuchuri/apartment-finder) by Vik Paruchuri.


Deployment
--------------------

    # copy all files
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

The `remove_listing.py` file is useful for testing your alerts and allows you to easily delete a record from your local database to make sure your alert fires as you expect. Also, it displays the most recent 15 items in your local database for debugging purposes.


