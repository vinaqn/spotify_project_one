with avg_album_stats as (
  select 
    track.album_id, 
    round(
      avg(track.popularity), 
      1
    ) as "avg_track_pop", 
    ROUND(
      AVG(track.duration_ms)/ 60000.0, 
      1
    ) as "avg_track_len_min" 
  from 
    public.tracks track 
  group by 
    1
) 
select 
  album.album_id, 
  album.album_name, 
  artist.artist, 
  left(album.album_release_date, 4) as album_release_year, 
  album.popularity as "album_popularity", 
  aas."avg_track_pop", 
  aas."avg_track_len_min" 
from 
  public.album album 
  left join avg_album_stats aas on aas.album_id = album.album_id 
  left join public.artist artist on artist.artist_id = album.artist_id 
order by 
  aas."avg_track_pop" desc