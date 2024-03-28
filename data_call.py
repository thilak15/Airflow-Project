import os
import googleapiclient.discovery
import pandas as pd

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCigcW1xhk9uW02CBUJiejuwjNjhnprPWM"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    video_id = "q8q3OFFfY6c"
    request = youtube.commentThreads().list(
        part="snippet, replies",
        videoId=video_id
    )
    response = request.execute()

    comments_list = []
    if 'items' in response:
        comments_list.extend(process_comments(response['items']))

    # Handling pagination
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='snippet, replies',
            videoId=video_id,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    save_comments_to_csv(comments_list, 'youtube_comments.csv')

    # Displaying processed comments

def process_comments(response_items):
    comments = []
    for item in response_items:
        author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_text = item['snippet']['topLevelComment']['snippet']['textOriginal']
        publish_time = item['snippet']['topLevelComment']['snippet']['publishedAt']
        comments.append({'author': author, 'comment': comment_text, 'published_at': publish_time})
    print(f'Finished processing {len(comments)} comments.')
    return comments
def save_comments_to_csv(comments, filename):
    df = pd.DataFrame(comments)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f'Successfully saved {len(comments)} comments to {filename}')

if __name__ == "__main__":
    main()
