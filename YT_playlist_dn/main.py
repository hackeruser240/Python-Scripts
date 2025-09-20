import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth 2.0 setup
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
CLIENT_SECRETS_FILE = 'client_secret.json'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080)
    return build('youtube', 'v3', credentials=credentials)

def get_watch_later_videos(youtube):
    playlist_id = 'WL'  # Watch Later playlist ID
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append({'Title': title, 'URL': url})

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def save_to_csv(videos, filename='watch_later.csv'):
    df = pd.DataFrame(videos)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Saved {len(videos)} videos to {filename}")

if __name__ == '__main__':
    youtube = get_authenticated_service()
    video_data = get_watch_later_videos(youtube)
    save_to_csv(video_data)