@echo off

set DJANGO_SETTINGS_MODULE=config.settings
set PYTHONPATH=.

pytest
pause