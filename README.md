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
docker run -d -p 5000:5000 flask-frontend
```
You can check that it is running correctly by opening `localhost:5000` in your browser.