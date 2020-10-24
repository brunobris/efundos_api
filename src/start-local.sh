#!/bin/bash
#Este arquivo é utilizado apenas quando executado pelo docker-compose (local), unicamente para desenvolvimento. 

echo "Executando requirements.."
pip install -r requirements.txt
echo "Subindo servidor..."
gunicorn --reload -c gunicorn_config.py --chdir src wsgi:app
#gunicorn --workers=2 --reload --worker-tmp-dir /dev/shm --chdir projeto -b 0.0.0.0:5000 wsgi:app


#Se por algum motivo desejar subir pelo servidor do Flask (desenvolvimento apenas):
#python -u run.py


