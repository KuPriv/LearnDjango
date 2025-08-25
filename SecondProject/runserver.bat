@echo off

call venv\Scripts\activate

set HOST=127.0.0.1
set PORT=8000

set CERT_FILE=cert.crt

start "" https://%HOST%:%PORT%/
python manage.py runserver_plus %HOST%:%PORT% --cert-file %CERT_FILE%

pause