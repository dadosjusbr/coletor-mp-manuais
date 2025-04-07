# set base image (host OS)
FROM python:3.8-slim-buster

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local directory to the working directory
COPY src/ .

# copy the content of the local directory to the working directory
COPY credentials.json .

# command to run on container start
CMD [ "python", "./main.py" ]