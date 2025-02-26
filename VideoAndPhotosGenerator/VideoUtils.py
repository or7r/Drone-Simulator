from googleapiclient.discovery import build

API_KEY = "AIzaSyBG0BCSIfLhg4LXLjnZT8ysG3XeUaiOSvU"

class VideoUtils:
    def get_urls_from_query(query: str, maxResults: int):
        youtube = build("youtube", "v3", developerKey=API_KEY)
        
        request = youtube.search().list(
            part="id",
            q=query,
            maxResults=maxResults,  # Get only the top result
            type="video"  # Ensure we only get video results
        )
        
        response = request.execute()

        if response["items"]:
            video_urls = []
            print(response["items"])
            for (item) in response["items"]:
                video_urls.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
        
            return video_urls
        else:
            return "No results found."