El programa funciona al correr tres programas secuencialmente

py -m venv venv --- la primera vez
venv\Scripts\activate.bat --- cada vez que abra la consola
pip install -r requirements --- la primera vez
set FLASK_APP=main.py --- la primera vez
set FLASK_DEBUG=1 --- la primera vez
py main.py --- cada vez que abra la consola