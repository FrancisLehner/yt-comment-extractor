from dotenv import load_dotenv
import os
import googleapiclient.discovery
from utils.comments import make_csv, process_comments
from iteration_utilities import unique_everseen
import requests
from datetime import datetime as dt
import json


load_dotenv()
API_KEY = os.getenv('API_KEY')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

def comment_threads(videoID, to_csv=False):

    comments_list = []
    error = None
    try:
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
        
    except googleapiclient.errors.HttpError as e:
        error = e
        try:
            error_content = e.content.decode('utf-8')
            error_data = json.loads(error_content)
            if error.resp.status == 403:
                error_reason = error_data['error']['errors'][0]['reason']
                if error_reason == 'commentsDisabled':
                    print("BEEBOOO")
                else:
                    print("ERR")
            else:
                print("ERROR")

        except json.JSONDecodeError:
            print('Error decoding JSON content')

    return comments_list, error




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
    # publish_date(videoID)

if __name__ == "__main__":
    main()

