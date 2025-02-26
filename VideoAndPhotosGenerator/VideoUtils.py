import random
from pytube import Search
import requests
import os

def get_video_url(query):
    search = Search(query)
    if not search.results:
        return "No results found."

    video_url = search.results[random.randint(0, len(search.results) - 1)].watch_url  # Get the first video link

    return video_url

def upload_video(video_url, upload_url):
    # Step 1: Download the video
    response = requests.get(video_url, stream=True)
    if response.status_code != 200:
        print("Failed to download video")
        return None

    # Step 2: Save the video locally
    video_filename = "video.mp4"
    with open(video_filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"Downloaded video: {video_filename}")

    # Step 3: Upload the video
    with open(video_filename, "rb") as file:
        files = {"file": (video_filename, file, "video/mp4")}
        upload_response = requests.post(upload_url, files=files)
    
    os.remove(video_filename)

    if upload_response.status_code == 200:
        print("Upload successful:", upload_response.json())  # Assuming JSON response
        return upload_response.json()
    else:
        print("Upload failed:", upload_response.text)
        return None


# Example usage
# query = input("Enter your search topic: ")
# video_url = get_video_url(query)
#
# upload_url = "https://your-api.com/upload"   # Replace with actual API endpoint
#
# upload_video(video_url, upload_url)
