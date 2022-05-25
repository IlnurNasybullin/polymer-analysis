## Installation & Running
1. Install [Python 3.9.10](https://www.python.org/downloads/release/python-3910/)
2. Clone repository: 
```
git clone https://github.com/IlnurNasybullin/polymer-analysis
```
3. Move to project directory:
```
cd polymer-analysis
```
4. Create and activate virtual environment:
```
python -m venv env
./env/Scripts/activate
```
5. Install requirements:
```
python -m pip install -r requirements.txt
```
6. Create migrations:
```
python manage.py migrate
```
```
python manage.py makemigrations
```
7. Run server:
```
python manage.py runserver
```
8. Open host http://localhost:8000/ in browser

## Other
[developers](/developers.md)
