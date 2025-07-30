from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bio_polls'


class MyAdminConfig(AdminConfig):
    default_site = 'bio_polls.admin.MyAdminSite'
