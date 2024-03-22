from dotenv import load_dotenv
import os
import googleapiclient.discovery
from utils.comments import make_csv, process_comments
from iteration_utilities import unique_everseen
import requests
from datetime import datetime as dt
from datetime import date


load_dotenv()
API_KEY = os.getenv('API_KEY')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

def comment_threads(videoID, to_csv=False):

    comments_list = []

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = API_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet,replies",
        maxResults=5,
        order="relevance",
        videoId = videoID
    )

    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,snippet,replies',
            order='relevance',
            videoId = videoID,
            pageToken = response['nextPageToken']   
        )

        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    
    comments_list = list(unique_everseen(comments_list))
    # print(comments_list)

    if to_csv:
        make_csv(comments_list, videoID)


def automated_comment_fetch(videoId):
    pass



def publish_date(videoID):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={videoID}&key={API_KEY}&part=snippet'
    response = requests.get(url)
    data = response.json()
    upload_date = data['items'][0]['snippet']['publishedAt']

    upload_date = dt.strptime(upload_date, '%Y-%m-%dT%H:%M:%SZ').date()
    upload_date = upload_date.strftime('%d-%m-%Y')
    print("Upload Date:", upload_date)

def main():
    videoID = input(('Input Video ID:'))
    comment_threads(videoID, to_csv=True)
    publish_date(videoID)

if __name__ == "__main__":
    main()

