# Django-Rest-QuickStart Project

Use this a seed project in your new django rest apps. This provides quick and reusable components for a django rest project.
Basic apps included are : users, utils,permissions,and groups.

This project also provides email or phone number authentication and a customized reponse object with reponse messages.

#Usage

  1. Clone the project
  2. run "pip install -r requirements"
  3. create file "local_settings.py" in rest_api/ folder and override settings
  4. read the "utils" app and check on how global renderers and views are implemented.
  5. run server i.e "./manage.py runserver" and go to /docs and read more of the documented details
  6. For email and sms sending, check the way "notifications" app is implemented and its usage in "utils" and "scripts" apps.        In "scripts" app , check how the messages are sent and write a service for the file "send_notifications.py".
  7. customize the API to your needs.
  8. Enjoy
 
 
