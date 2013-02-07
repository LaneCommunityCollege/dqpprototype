Degree Qualifications Profile Spidergraphs Prototype
==================

![screenshot showing overlapping program and course objectives](https://github.com/LaneCommunityCollege/dqpprototype/raw/master/screnshot.png)

With newer verions of Django (>= 1.4.3) and/or MySQL (>=5.5.29) there are some known issues with syncing the database.

A live demonstration of this application is available [online](http://oregondqp.lanecc.edu/spidergraphs).

## Installation
Unfortunately, these instructions are likely missing some steps.

1. Unzip the application into your /opt directory
2. Copy settings_default.py to dqp/settings.py
3. Edit the file dqp/settings.py with your local database settings, as well as a new secret string (You can generate a new secret [online](http://www.miniwebtool.com/django-secret-key-generator/))
4. Tell Django to sync the database with `python manage.py syncdb`
5. Let Apache know about your new Django app and restart Apache.

Alternatively, you can unzip the application in any location, sync the database, and then run the Django local development server. 

## About
This protype was developed at [Lane Community College](http://www.lanecc.edu), during the last week of October, 2012, as part of the [Oregon DQP Project](http://oregondqp.lanecc.edu), with grant support from the [Lumina Foundation](http://www.luminafoundation.org/). It represents a web enabled version of the work started by Mark Williams, at [Umpqua Community College](http://www.umpqua.edu). Additional information about the Degree Qualifications Profile can be found at the [Oregon DQP Project website](http://oregondqp.lanecc.edu). 

This prototype is in the process of being redeveloped as a more fully featured application, and consequently only limited support is available, although pull requests are welcomed. Questions regarding this version of the DQP Spidergraphs tool should be directed to the original developer, Kyle Schmidt, at schmidtk@lanecc.edu. Questions about future features should be directed to the new developer, Matthew Danskine, at danskinem@lanecc.edu. 
