import csv
from datetime import datetime as dt

today = dt.today().strftime('%d-%m-%Y')

comments = []
def process_comments(response_items, csv_output=False):
    # Handle Replies

    for res in response_items:
        if 'replies' in res.keys():
            for reply in res['replies']['comments']:
                comment = reply['snippet']
                comment['commentId'] = reply['id'] 
                comments.append(comment)

    # Non-Handle Replies
    for res in response_items:
        comment = {}
        comment['snippet'] = res['snippet']['topLevelComment']['snippet']
        comment['snippet']['parentId'] = None
        comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
        
        comments.append(comment['snippet'])

    if csv_output:
        make_csv(comments)

    print(f'Finished Processing {len(comments)} comments.')
    return comments
    

def make_csv(comments, videoId = None):
    header = comments[0].keys()
    if videoId:
        filename = f'comments_{videoId}_{today}.csv'
    else:
        filename = f'comments_{today}.csv'

    with open(filename, 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(comments)

