#!/usr/bin/env python3

from googleapiclient.discovery import build
import re
import json

# Replace with your YouTube API key
api_key = YOUTUBE_API_KEY
# Replace with your YouTube channel ID
channel_id = 'UCZG5IMQCnvmEGZHLcZxgd3g'

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to convert DMS to Decimal Degrees
def dms_to_decimal(degree, direction):
    decimal = float(degree)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# Function to get video details
def get_video_details(youtube, **kwargs):
    results = youtube.videos().list(**kwargs).execute()
    return results

# Function to get videos from a channel
def get_videos(youtube, **kwargs):
    video_details = []
    next_page_token = None

    while True:
        try:
            if next_page_token:
                kwargs['pageToken'] = next_page_token
            results = youtube.search().list(**kwargs).execute()
            for item in results.get('items', []):
                if item['id']['kind'] == 'youtube#video':
                    video_id = item['id']['videoId']
                    video_info = get_video_details(youtube, part='snippet', id=video_id)
                    video_title = video_info['items'][0]['snippet']['title']
                    video_description = video_info['items'][0]['snippet']['description']
                    coordinates = re.search(r'(-?\d+\.\d+)[°º]?\s*([NS]),\s*(-?\d+\.\d+)[°º]?\s*([EW])', video_description)
                    if coordinates:
                        latitude = dms_to_decimal(coordinates.group(1), coordinates.group(2))
                        longitude = dms_to_decimal(coordinates.group(3), coordinates.group(4))
                        video_details.append({
                            'title': video_title,
                            'video_url': f'https://www.youtube.com/embed/{video_id}',
                            'latitude': latitude,
                            'longitude': longitude
                        })
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return video_details

# Fetch video list and details
video_list = get_videos(youtube, part='snippet', channelId=channel_id, maxResults=50)

# Print video details (optional)
if not video_list:
    print("No videos found or an error occurred.")
else:
    for video in video_list:
        print(f"Title: {video['title']}")
        print(f"Video URL: {video['video_url']}")
        print(f"Coordinates: ({video['latitude']}, {video['longitude']})")
        print()

# Save video details to a JSON file
with open('video_data.json', 'w') as outfile:
    json.dump(video_list, outfile, indent=4)
