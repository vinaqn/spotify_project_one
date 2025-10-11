with avg_artist_stats as (
select 
track.artist_id,
ROUND(AVG(track.duration_ms)/60000.0,1) as "avg_track_len_min",
round(max(track.duration_ms)/60000.0,1) as "max_track_length_min"
from public.tracks track
group by 1
)
select 
artist.artist_id,
artist.artist,
artist.popularity,
aas."max_track_length_min",
aas."avg_track_len_min",
(aas."max_track_length_min"-aas."avg_track_len_min") as "diff_between_max_and_avg"
from public.artist artist
inner join avg_artist_stats aas on artist.artist_id=aas.artist_id
order by "avg_track_len_min" desc