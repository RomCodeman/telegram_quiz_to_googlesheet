![GitHub release (python version)](https://img.shields.io/badge/python-3.9-informational)
# Telegram bot Questionnaire 

### Table of contents
* [Table of contents](#table-of-content)
* [Description](#description)
* [Project structure](#project-structure)
* [Examples of the workflow](#examples-of-the-workflow)
* [Technology Stack](#technology-stack)
* [Known issues](#known-issues)

### Description
Very simple implementation of the telegram bot for clients polling and writing their answers to the Google Sheet's tables.
And in the near future to the PostgreSQL and Mongo DB's.

At this moment, polling mode launch, via CLI command, is more preferable: 
> ./manage.py bot_start

The deployment on Heroku is also possible, but operation of this Bot sometimes unstable. 

### Example of the workflow
Image below displays how it's should be.

<p align="center">
  <img src="/static/workflow.png?raw=true" alt="Workflow example"/>
</p>

Automatic sheets and column titles creation, according to the classes in ```sheets_class.py```. This kind of implementation is not the
best idea, as I think. I did it in the simplest way, to check how it will work. The Builder or the Factory Method pattern's, may be a good feature for these cases.

<p align="center">
  <img src="/static/sheet_autocreating.png?raw=true" alt="Sheet automatic creation"/>
</p>

In cases, when we have some sheet, which not described in the ```sheets_class.py``` we would have next notification in
log.

<p align="center">
  <img src="/static/unused_sheet_notifying.png?raw=true" alt="Unused sheet notification"/>
</p>

### Project structure
    .
    ├── bot_app/
    │    ├── management/
    │    │    └── commands/
    │    │         └── bot_start.py         # CLI command for Polling launch mode
    │    ├── sheets/
    │    │    ├── __init__.py               # Automatic sheets and column titles creation
    │    │    └── sheets_class.py           # Sheet's logic
    │    ├── admin.py                       # Simple admin-panel implementation
    │    ├── bot_app_logic.py               # Logic of the Bot application
    │    ├── bot_text_templates.py          # Text templates for the Bot answers 
    │    ├── buttons.py                     # Custom buttons
    │    ├── logger.py                      # Logging setup
    │    ├── models.py                      # Local DB models setup (in future: PostgreSQL, MongoDB)
    │    ├── states.py                      # States logic
    │    ├── views.py                       # Webhook
    │    └── (...)
    ├── static/                             # Images for this repo
    │    └── (...)
    ├── telegram_quiz_to_googlesheet/
    │    ├── settings/                      # Different project launch settings
    │    │    ├── base.py                   # Base project settings
    │    │    ├── develop_mongo.py          # MongoDB not implemented at this moment
    │    │    ├── develop_postgresql.py     # PostgreSQL not implemented at this moment
    │    │    └── production.py             # Not implemented at this moment
    │    ├── urls.py                        # Admin-panel, webhook register and webhook url patterns
    │    └── (...)
    ├── config.py                           # Environment variables settings
    ├── manage.py                           # CLI application launch with DJANGO_SETTINGS_MODULE
    ├── Procfile                            # Commands that are executed by the app on Heroku startup
    ├── README.md                           # Description of the project
    ├── requirements.txt                    # Application package requirements
    └── runtime.txt                         # Specifying a Python runtime for startup on Heroku

### Technology Stack
* PL - [Python](https://www.python.org/)
* Web framework - [Django](https://www.djangoproject.com/)
* Deploy - [Heroku](https://www.heroku.com/), by applying: [django-on-heroku](https://github.com/pkrefta/django-on-heroku), [gunicorn](https://gunicorn.org/)
* Telegram Bot API implementation - [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
* Google Sheet API implementation - [oauth2client](https://github.com/googleapis/oauth2client), [gspread](https://github.com/burnash/gspread)



### Known issues
* the validation of obtained data required

* sometimes unstable execution on Heroku

* MongoDB/PostgreSQL are not implemented (it will be done in upcoming updates)

* manual phone number input (will change on a special button)

* current users states can be saved in the class attributes and operated by a separate method

* sometimes creates incorrect sheet (example: TempSheet_conflict1933130442)