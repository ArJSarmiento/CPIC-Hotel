# CPIC Hotel
A Hotel Management and Reservation System for the Hotel and Restaurant Services Department of Christian Polytechnic Institute of Catanduanes.

# Setup Environment

## For Linux/Mac
### Installing venv 
```shell 
sudo apt-get install python3.8-venv
```
### Creating virtual env
```shell 
python3 -m venv env
```
### Activating virtual env
```shell 
source env/bin/activate
```

## For Windows
### Installing venv
```shell 
py -m pip install --user virtualenv
```
### Creating virtual env
```shell 
py -m venv env
```
### Activating virtual env
```shell 
.\env\Scripts\activate
```

# Setup:
1.
```shell
pip3 install -r requirements.txt
```
2.
```shell
python manage.py makemigrations
```
3.
```shell
python manage.py migrate
```
# Run:
```shell
python manage.py runserver
```
