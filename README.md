# frontend-template-flask
Frontend template using flask.

## Build the docker image
To build the docker image, run  
```
docker build -t flask-frontend:latest 
```
inside the `frontend-template-flask` directory.

## Run the docker container
To run the container, execute  
```
docker run -d -p 8000:8000 flask-frontend
```
You can check that it is running correctly by opening `127.0.0.1:8000` in your browser.