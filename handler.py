import os

## GOOGLE AUTH LIBS
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

#configs
config_file = 'config.ini' 
from configparser import SafeConfigParser
config = SafeConfigParser()
config.read(config_file)

import sched
import time


video_likes = 9594
comment_likes = 0

# getting video ID from url
video_url = config.get('default','video_url')
video_id =  video_url.split('=')[1]

########################################################################
################### YOUTUBE API SETUP ##################################
########################################################################

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# # Disable OAuthlib's HTTPS verification when running locally.
# # *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "credentials.json"

# # Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, SCOPES)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

##########################################################################

# initlizling the scheduler
s = sched.scheduler(time.time, time.sleep)

def main():
    global video_likes
    global comment_likes
    global comment_id
    global video_id
    
    # Check if comment id exists in config, else create a new comment and add the Id to config
    if config.has_option('default','comment_id'):
        comment_id = config.has_option('default','comment_id')
    else:
        video_likes = int(videoLikes(video_id))
        [thread_id, comment_id] = makeCommentThread(video_id)
        updateConfigWithCommentId(comment_id)
    
    updateComment()

    if config.getboolean('default', 'delete_comment_after'):
        deleteComment(comment_id)

# Udpdate the comment with latest stats
def updateComment():
    global video_likes
    global comment_likes

    video_likes = int(videoLikes(video_id))
    comment_likes = int(getCommentLikes(comment_id))
    updateCommentThread(comment_id)

    # Queue Scheduler
    interval = config.getint('default','polling_interval')
    s.enter(interval, 1, updateComment)
    s.run()


def updateCommentThread(thread_id):
    request = youtube.comments().update(
        part="snippet",
        body={
            "id": thread_id,
            "snippet": {
                "textOriginal": makeCommentText(comment_likes, video_likes)
            }
        }
    )

    response = request.execute()


def makeCommentThread(video_id):
    comment_text = makeCommentText(comment_likes, video_likes)
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    )
    thread_data = request.execute()

    return [thread_data['id'], thread_data["snippet"]['topLevelComment']['id']]


def videoLikes(video_id):
    response = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    ).execute()

    return response["items"][0]['statistics']['likeCount']


def deleteComment(thread_id):
    request = youtube.comments().delete(
        id=thread_id
    )
    request.execute()


def getCommentLikes(thread_id):
    response = youtube.comments().list(part="snippet", id=thread_id).execute()
    return response['items'][0]['snippet']['likeCount']


def makeCommentText(comment_likes, video_likes):
    more_or_less = "more" if(comment_likes > video_likes) else "less"
    like_diff = abs(video_likes - comment_likes)
    _like = "like"
    _like += 's' if(comment_likes > 0) else ''
    return f'This comment has {comment_likes} { _like } which is {like_diff} {more_or_less} than the video!'

def updateConfigWithCommentId(comment_id):
    config.set('default','comment_thread_id', comment_id)
    with open( config_file , 'wb') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    main()
