@echo off

set DJANGO_SETTINGS_MODULE=mysite.settings
set PYTHONPATH=.

pytest
pause