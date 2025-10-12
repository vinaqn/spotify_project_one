FROM python:3.9

#set up directory in docker image
WORKDIR /app 

#copy current local directory {.} to docker directory {/app}
COPY . /app 

ENV API_KEY_ID=""
ENV API_SECRET_KEY=""
ENV DB_SERVER_NAME=""
ENV DB_DATABASE_NAME=spotify_project
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=""
ENV DB_PORT=5432

ENV LOGGING_SERVER_NAME=""
ENV LOGGING_DATABASE_NAME=spotify_logging
ENV LOGGING_USERNAME=postgres
ENV LOGGING_PASSWORD=""
ENV LOGGING_PORT=5432

RUN pip install -r requirements.txt

CMD ["python", "-m","pipeline.pipeline"]

#docker build -t spotify_project_one:1.0 .
#docker run --env-file .env  spotify_project_one:1.0