import os
from googleapiclient.discovery import build

# Replace with your API key
API_KEY = 'YOUR_API_KEY'

# Create a service object
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query, max_results=5):
    #Use the search.list method to retrieve results matching the specified query term
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )

    response = request.execute()

    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        url = f'https://www.youtube.com/watch?v={video_id}'
        print(f'Title: {title}')
        print(f'URL: {url}')
        print('---')

if __name__ == '__main__':
    search_videos('Python programming', max_results=5)
