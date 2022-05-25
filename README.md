## Installation & Running

*Note: on Windows if you using cmd for all commands replace '/' on '\\'*

1. Install [Python 3.9.10](https://www.python.org/downloads/release/python-3910/)
2. Clone repository: 
```
git clone https://github.com/IlnurNasybullin/polymer-analysis
```
3. Move to project directory:
```
cd polymer-analysis
```
4. Create dir weights in expert_system/particle_model
```
mkdir ./expert_system/particle_model/weights
```
5. Download trained model [particles-yolov5l-best.pt](https://drive.google.com/drive/folders/1cvMy4u7qFtPSNI4_kzOa3YlcHMiTZO9e) from Google Drive and put downloaded file to created dir weights
6. Create and activate virtual environment:
```
python -m venv env
./env/Scripts/activate
```
7. Install requirements:
```
python -m pip install -r requirements.txt
```
8. Create migrations:
```
python manage.py migrate
```
```
python manage.py makemigrations
```
9. Run server:
```
python manage.py runserver
```
10. Open host http://localhost:8000/ in browser

## Other
[developers](/developers.md)
