# Project Overview	#
The main goal of this project is to build and deploy an ELT pipeline on AWS using the skills we learned in our data engineering bootcamp. We use the Spotify API to collect data on tracks, albums, and artists, then load it into a database to run basic analyses.

## Consumers
The users of our dataset will be the data analytics team, hobbyists, or students.

## Questions
* Which artists have the most albums?
* What is the average number of tracks on an album?
* What are the top 5 popular tracks in each album?
* Which album has the highest average track popularity? Which album has the longest average track duration?
* How many songs does each artist have? What is an artist's average length of a song versus their longest song?

## Source Datasets
The table below lists where we sourced our datasets from. The csv file is the only static file. 

| Source name | Source type | Source documentation |
| - | - | - |
| track_ids.csv | csv |https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset|
| Spotify Tracks API| REST API |https://developer.spotify.com/documentation/web-api|
| Spotify Albums API| REST API |https://developer.spotify.com/documentation/web-api|
| Spotify Artists API  | REST API |https://developer.spotify.com/documentation/web-api|
| Spotify Categories API  | REST API |https://developer.spotify.com/documentation/web-api|
| Spotify Markets API  | REST API |https://developer.spotify.com/documentation/web-api|

## Solution Architecture 	
TBA

## Lessons Learnt
* What is the average number of tracks on an album?

## Docker Container Deployed to AWS Screenshots

### Elastic Container Service (ECS)
<img width="1616" height="688" alt="ScheduledTaskinECSRunning" src="https://github.com/user-attachments/assets/dd217867-9d8f-4dcb-bf8a-816170449db4" />
<img width="1641" height="751" alt="LogofTaskRunningSuccessfully" src="https://github.com/user-attachments/assets/b0650195-2da7-4892-a14d-cfc6159ebe7e" />

### Elastic Container Registry (ECR)
<img width="1639" height="241" alt="ECR" src="https://github.com/user-attachments/assets/38e08505-5799-425d-bdf6-e950ccfe3c59" />

### RDS - Dataset in Target Storage
<img width="1883" height="788" alt="AuroraAndRDS" src="https://github.com/user-attachments/assets/11353fa4-e3b7-461d-ab51-e0181f57fdb3" />
<img width="1132" height="884" alt="PGAdminConnectedtoRDS" src="https://github.com/user-attachments/assets/a66a3a56-67b1-437c-9e87-d1e1b3b84189" />

### IAM Role
<img width="1619" height="631" alt="IAMRole" src="https://github.com/user-attachments/assets/b854085c-4f37-4999-800f-25eb935d5d70" />

### S3 .env file
<img width="1614" height="357" alt="S3env" src="https://github.com/user-attachments/assets/58a18220-18d0-4a49-be74-c70d5ade92fc" />
