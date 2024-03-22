from dotenv import load_dotenv
import os
import googleapiclient.discovery
from utils.comments import make_csv, process_comments
from iteration_utilities import unique_everseen
import requests
from datetime import datetime as dt
from datetime import date
import json
from urllib.request import urlopen
import shutil


load_dotenv()
API_KEY = os.getenv('API_KEY')


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

today = dt.today().strftime('%d-%m-%Y')

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

    except requests.exceptions.HTTPError as e:
        error = e

    return comments_list, error

def publish_date(videoID):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={videoID}&key={API_KEY}&part=snippet'
    response = requests.get(url)
    data = response.json()
    upload_date = data['items'][0]['snippet']['publishedAt']

    upload_date = dt.strptime(upload_date, '%Y-%m-%dT%H:%M:%SZ').date()
    upload_date = upload_date.strftime('%d-%m-%Y')
    print("Upload Date:", upload_date)



def automated_comment_fetch(ChannelIdentifier, API_KEY):
    videoMetadata = [] 
    nextPageToken = None
    processed_video_ids = set()

    while True:
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={ChannelIdentifier}&maxResults=50&type=video&key={API_KEY}'
        if nextPageToken:
            url +=f'&pageToken={nextPageToken}'
            
        response = urlopen(url) 
        videos = json.load(response) 

        for video in videos['items']:
            if video['id']['kind'] == 'youtube#video':
                videoMetadata.append({'videoId' : video['id']['videoId'], 'publish_date': video['snippet']['publishedAt']}) 
        
        nextPageToken = videos.get('nextPageToken')
        if not nextPageToken:
            break
        
    #Date Parameters

    apr_24 = dt(2024, 4, 30, 23, 59, 59)  
    jan_24 = dt(2024, 1, 1, 0, 0, 0)
    dec_23 = dt(2023, 12, 31, 23, 59, 59)  
    sep_23 = dt(2023, 9, 1, 0, 0, 0)
    aug_23 = dt(2023, 8, 30, 23, 59, 59)  
    may_23 = dt(2023, 5, 1, 0, 0, 0)
    apr_23 = dt(2023, 4, 30, 23, 59, 59)  
    jan_23 = dt(2023, 1, 1, 0, 0, 0)
    dec_22 = dt(2022, 12, 31, 23, 59, 59)  
    sep_22 = dt(2022, 9, 1, 0, 0, 0)
    aug_22 = dt(2022, 8, 30, 23, 59, 59)  
    may_22 = dt(2022, 5, 1, 0, 0, 0)
    apr_22 = dt(2022, 4, 30, 23, 59, 59)  
    jan_22 = dt(2022, 1, 1, 0, 0, 0)
    dec_22 = dt(2022, 12, 31, 23, 59, 59)  
    sep_22 = dt(2022, 9, 1, 0, 0, 0)
    aug_22 = dt(2022, 8, 30, 23, 59, 59)  
    may_22 = dt(2022, 5, 1, 0, 0, 0)
    apr_22 = dt(2022, 4, 30, 23, 59, 59)  
    jan_22 = dt(2022, 1, 1, 0, 0, 0)
    dec_21 = dt(2021, 12, 31, 23, 59, 59)  
    sep_21 = dt(2021, 9, 1, 0, 0, 0)
    aug_21 = dt(2021, 8, 30, 23, 59, 59)  
    may_21 = dt(2021, 5, 1, 0, 0, 0)
    apr_21 = dt(2021, 4, 30, 23, 59, 59)  
    jan_21 = dt(2021, 1, 1, 0, 0, 0)
    dec_20 = dt(2020, 12, 31, 23, 59, 59)  
    sep_20 = dt(2020, 9, 1, 0, 0, 0)
    aug_20 = dt(2020, 8, 30, 23, 59, 59)  
    may_20 = dt(2020, 5, 1, 0, 0, 0)
    apr_20 = dt(2020, 4, 30, 23, 59, 59)  
    jan_20 = dt(2020, 1, 1, 0, 0, 0)
    dec_19 = dt(2019, 12, 31, 23, 59, 59)  
    sep_19 = dt(2019, 9, 1, 0, 0, 0)

    # for videoId in videoMetadata:
    #     for date in videoId['publish_date']:
    #         date = dt.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    #         if jan_24 <= date <= apr_24:
    #             shutil.move(f"C:/Users/Editor PC 2/Desktop/francis/Python/YT_cretivox/task.txt", f"C:/Users/Editor PC 2/Desktop/francis/Python/YT_cretivox/extracted_comments/Jan24 - Apr24/task.txt")

    for video_id in videoMetadata:
        videoId = video_id['videoId']
        publish_date = dt.strptime(video_id['publish_date'], "%Y-%m-%dT%H:%M:%SZ")
        if videoId not in processed_video_ids:
            try:
                print(f"Processing comments for video ID: {videoId}")
                comment_threads(videoId, to_csv=True)

                if jan_24 <= publish_date <= apr_24:
                    destination_folder = "Jan24-Apr24"
                elif sep_23 <= publish_date <= dec_23:
                    destination_folder = "Sep23-Dec23"
                elif may_23 <= publish_date <= aug_23:
                    destination_folder = "May23-Aug23"
                elif jan_23 <= publish_date <= apr_23:
                    destination_folder = "Jan23-Apr23"
                elif sep_22 <= publish_date <= dec_22:
                    destination_folder = "Sep22-Dec22"
                elif may_22 <= publish_date <= aug_22:
                    destination_folder = "May22-Aug22"
                elif jan_22 <= publish_date <= apr_22:
                    destination_folder = "Jan22-Apr22"
                elif sep_21 <= publish_date <= dec_21:
                    destination_folder = "Sep21-Dec21"
                elif may_21 <= publish_date <= aug_21:
                    destination_folder = "May21-Aug21"
                elif jan_21 <= publish_date <= apr_21:
                    destination_folder = "Jan21-Apr21"
                elif sep_20 <= publish_date <= dec_20:
                    destination_folder = "Sep20-Dec20"
                elif may_20 <= publish_date <= aug_20:
                    destination_folder = "May20-Aug20"
                elif jan_20 <= publish_date <= apr_20:
                    destination_folder = "Jan20-Apr20"
                else:
                    destination_folder = "Sep19-Dec19"

                destination_path = os.path.join(f"C:/Users/Editor PC 2/Desktop/francis/Python/YT_cretivox/extracted_comments/{destination_folder}", f"comments_{videoId}_{today}.csv")

                if os.path.exists(destination_path):
                    os.remove(destination_path)
                shutil.copy(f"C:/Users/Editor PC 2/Desktop/francis/Python/YT_cretivox/comments_{videoId}_{today}.csv", destination_path)
                
            except requests.exceptions.HTTPError as e:
            # Check if the exception is due to a 403 error (Forbidden or Disabled Comments)
                if e.response.status_code == 403:
                    error_message = e.response.json()["error"]["errors"][0]['reason']
                    if error_message == 'commentsDisabled':
                        print("Comments are disabled for this video. Skipping this request.")
                        continue
                    else:
                        print(f"403 Forbidden: {error_message}. Skipping this request.")
                        continue
                else:
                    # Handle other HTTP errors
                    print(f"HTTP error occurred: {e}")
                    
            except requests.exceptions.RequestException as e:
                # Handle other exceptions (e.g., network errors)
                print(f"Error making API request: {e}")
                

        processed_video_ids.add(videoId)


def main():
    try:
        automated_comment_fetch('UC4DogC2xftpKFlF-XgZoRBg', API_KEY)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


