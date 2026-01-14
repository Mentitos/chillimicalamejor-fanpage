import os
import json
import requests
import re

API_KEY = os.environ["YOUTUBE_API_KEY"]
CHANNEL_ID = "UCboXCsBUZvek5T5cCltHS5w"

def parse_duration(duration_str):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return (hours * 3600) + (minutes * 60) + seconds

def obtener_avatar():
    url_channel = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={CHANNEL_ID}&key={API_KEY}"
    try:
        resp = requests.get(url_channel)
        data = resp.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
    except Exception:
        pass
    return None

def buscar_video_real():
    avatar_url = obtener_avatar()
    
    uploads_id = CHANNEL_ID.replace("UC", "UU", 1)
    
    url_playlist = f"https://www.googleapis.com/youtube/v3/playlistItems?key={API_KEY}&playlistId={uploads_id}&part=contentDetails&maxResults=10"
    
    resp = requests.get(url_playlist)
    data = resp.json()
    
    if "items" not in data:
        return

    video_ids = [item["contentDetails"]["videoId"] for item in data["items"]]
    ids_string = ",".join(video_ids)

    url_details = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={ids_string}&part=snippet,contentDetails,liveStreamingDetails"
    
    resp_details = requests.get(url_details)
    items_details = resp_details.json().get("items", [])

    video_final = None

    for item in items_details:
        titulo = item["snippet"]["title"]
        
        if "liveStreamingDetails" in item:
            continue

        duracion = parse_duration(item["contentDetails"]["duration"])
        if duracion < 60:
            continue

        video_final = {
            "id": item["id"],
            "title": titulo,
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "date": item["snippet"]["publishedAt"],
            "channel_avatar": avatar_url
        }
        break

    if video_final:
        with open("video_data.json", "w") as f:
            json.dump(video_final, f)

if __name__ == "__main__":
    buscar_video_real()