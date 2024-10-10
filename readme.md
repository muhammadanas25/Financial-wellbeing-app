# Instructions to run the project
install dependencies
```
pip install -r requirements.txt
```
set up .env file for open ai key and mongo db connection string

Commmand to start mongo db server
```
docker compose up -d
```


## Command to start backend server
```
uvicorn app.main:app --reload --port 8001
```
