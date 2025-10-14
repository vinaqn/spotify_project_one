# Project Overview	#
The main goal of this project is to build and deploy an ELT pipeline on AWS using the skills we learned in our data engineering bootcamp. We use the Spotify API to collect data on tracks, albums, and artists, then load it into a database to run basic analyses.

## Consumers
The users of our dataset will be the data analytics team, hobbyists, or students.

## Source Datasets
The table below lists where we sourced our datasets from. The csv file is the only static file. 

| Source name | Source type | Source documentation | Extract Type | Load Type
| - | - | - | - | - |
| track_ids.csv | csv |https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset| Full Extract | Full Load |
| Spotify Tracks API| REST API |https://developer.spotify.com/documentation/web-api| Full Extract | Upsert|
| Spotify Albums API| REST API |https://developer.spotify.com/documentation/web-api| Full Extract | Upsert|
| Spotify Artists API  | REST API |https://developer.spotify.com/documentation/web-api| Full Extract| Upsert|
| Spotify Categories API  | REST API |https://developer.spotify.com/documentation/web-api| Full Extract | Upsert |
| Spotify Markets API  | REST API |https://developer.spotify.com/documentation/web-api| Full Extract | Upsert |

## Solution Architecture 	

<img width="1850" height="1034" alt="DataArchitectureDiagram" src="https://github.com/user-attachments/assets/e6e40a52-706f-46cb-b76e-450f2e28c743" />

## Questions
* Which artists have the most albums?
  ```
  SELECT
    COUNT(album_name) as number_of_albums, 
    artist
  FROM public.album
    join public.artist ON album.artist_id = artist.artist_id
  GROUP BY artist
  ORDER BY number_of_albums DESC
  ```
* What is the average number of tracks on an album?
  ```
  select AVG(total_tracks) from album
  ```
* What are the top 3 popular tracks in each album?
  ```
  SELECT
    t.album_name,
    t.track_name,
    t.popularity,
    rank() over (partition by t.album_id order by t.popularity desc) as popularity_rank
  FROM public.tracks t
  ORDER BY t.album_name, popularity_rank
  ```
* Which album has the highest average track popularity? Which album has the longest average track duration?
  ```
  WITH avg_album_stats as (
  SELECT 
    track.album_id, 
    round(avg(track.popularity), 1) as "avg_track_pop", 
    ROUND(AVG(track.duration_ms)/ 60000.0, 1) as "avg_track_len_min" 
  FROM public.tracks track 
  GROUP by 1
  ) 
  SELECT 
    album.album_id, 
    album.album_name, 
    artist.artist, 
    left(album.album_release_date, 4) as album_release_year, 
    album.popularity as "album_popularity", 
    aas."avg_track_pop", 
    aas."avg_track_len_min" 
  FROM public.album album 
    LEFT JOIN avg_album_stats aas on aas.album_id = album.album_id 
    LEFT JOIN public.artist artist on artist.artist_id = album.artist_id 
  ORDER BY
    aas."avg_track_pop" desc
  ```
* How many songs does each artist have? What is an artist's average length of a song versus their longest song?
  ```
  WITH avg_artist_stats as (
  SELECT 
    track.artist_id,
    ROUND(AVG(track.duration_ms)/60000.0,1) as "avg_track_len_min",
    round(max(track.duration_ms)/60000.0,1) as "max_track_length_min",
    count(track.track_id) as "total_songs"
  FROM public.tracks track
  GROUP BY 1
  )
  SELECT 
    artist.artist_id,
    artist.artist,
    artist.popularity,
    aas."total_songs",
    aas."max_track_length_min",
    aas."avg_track_len_min",
    (aas."max_track_length_min"-aas."avg_track_len_min") as "diff_between_max_and_avg"
  FROM public.artist artist
    INNER JOIN avg_artist_stats aas on artist.artist_id=aas.artist_id
  ORDER BY "avg_track_len_min" desc
  ```
## Lessons Learnt
* We realized how important it is to maintain a clear `requirements.txt` file and manage package versions to keep deployments smooth and consistent.  
* Working with Git taught us the importance of following a clear order of operations — such as pulling before making changes, committing frequently, and creating branches for new features — to keep the team’s workflow organized and avoid conflicts.
* Reading through the Spotify API documentation helped us become more comfortable navigating technical docs and understanding rate limits.  
* Implementing chunked data extraction pushed us to think about scalability and how to handle large datasets efficiently.

## Appendix - Spotify Pipeline Deployed to AWS

### Elastic Container Registry (ECR)
Stored our Docker image in ECR
<img width="1639" height="241" alt="ECR" src="https://github.com/user-attachments/assets/38e08505-5799-425d-bdf6-e950ccfe3c59" />


### Elastic Container Service (ECS)
Created an ECS to manage our pipeline app
<img width="1616" height="688" alt="ScheduledTaskinECSRunning" src="https://github.com/user-attachments/assets/dd217867-9d8f-4dcb-bf8a-816170449db4" />
Log of our scheduled task running successfully
<img width="1641" height="751" alt="LogofTaskRunningSuccessfully" src="https://github.com/user-attachments/assets/b0650195-2da7-4892-a14d-cfc6159ebe7e" />


### Relational Database Services (RDS)
Created an PostgreSQL in RDS to host our raw and transformed tables
<img width="1883" height="788" alt="AuroraAndRDS" src="https://github.com/user-attachments/assets/11353fa4-e3b7-461d-ab51-e0181f57fdb3" />
<img width="1132" height="884" alt="PGAdminConnectedtoRDS" src="https://github.com/user-attachments/assets/a66a3a56-67b1-437c-9e87-d1e1b3b84189" />

### Private S3 Bucket
Stored our .env file in a private bucket so our ECS task can reference the environment variables
<img width="1614" height="357" alt="S3env" src="https://github.com/user-attachments/assets/58a18220-18d0-4a49-be74-c70d5ade92fc" />

### IAM Role
Created IAM Role `Spotify_Task_Operator` and gave the appropriate permissions to read the S3 bucket and schedule the task
<img width="1619" height="631" alt="IAMRole" src="https://github.com/user-attachments/assets/b854085c-4f37-4999-800f-25eb935d5d70" />


