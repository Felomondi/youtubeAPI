import os
from googleapiclient.discovery import build
import sqlalchemy as db
import pandas as pd

# Replace with your API key
API_KEY = 'AIzaSyBXPzyA9-6_eztFQs8TQqD5hWRQ2eEOmRo'

# Create a service object
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query, max_results=5):
    # Use the search.list method to retrieve results matching the specified query term
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )

    response = request.execute()

    video_data = {
        'title': [],
        'video_id': [],
        'url': []
    }

    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        url = f'https://www.youtube.com/watch?v={video_id}'
        video_data['title'].append(title)
        video_data['video_id'].append(video_id)
        video_data['url'].append(url)

    return video_data

if __name__ == '__main__':
    video_data = search_videos('Python programming', max_results=5)
    
    # Convert the dictionary into a pandas DataFrame
    df = pd.DataFrame.from_dict(video_data)
    
    # Create an engine object
    engine = db.create_engine('sqlite:///youtube_videos.db')
    
    # Create and send SQL table from the DataFrame
    df.to_sql('videos', con=engine, if_exists='replace', index=False)
    
    # Write a query and print out the results
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM videos;")).fetchall()
        print(pd.DataFrame(query_result, columns=['title', 'video_id', 'url']))