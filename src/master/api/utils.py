from email.mime import audio
from http.client import InvalidURL
import pytube
import math

# def convert_size(kb):
#    if kb == 0:
#        return "0KB"
#    size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
#    i = int(math.floor(math.log(kb, 1024)))
#    p = math.pow(1024, i)
#    s = round(kb / p, 2)
#    return "%s %s" % (s, size_name[i])
suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def convert_size(nbytes):
    i = 0
    if nbytes == 0:
        return "None"
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def convert_to_preferred_format(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    if hour >= 1:
        return "%02d:%02d Hour" % (hour, min) 
    elif min >=1:
        return "%02d:%02d Minutes" % (min, sec) 
    else:
        return "%02d:%02d Seconds" % (sec) 



def format(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000}M'
        return f'{round(num / 1000000, 1)}M'
    return f'{num // 1000}K'

def  get_video_streams(youtube_link):
    # yt = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}")
    try:
        yt = pytube.YouTube(youtube_link)
        mystreams = yt.streams
    except Exception as e:
        raise InvalidURL({
            "status":400,
            "msg":"Provided link is invalid or video maybe removed.."
        })
    response = {}
    response["title"] = yt.title
    response["thumbnail_url"] = yt.thumbnail_url
    response["sample_video"] = yt.streams.get_highest_resolution().url
    response["views"] = format(yt.views)
    response["length"] = convert_to_preferred_format(yt.length)
    response["description"] = yt.description
    response["channel"] = {
        "name":yt.author,
        "url":yt.channel_url
    }
    response["audio_streams"] = []
    response["video_streams"] = []

    for stream in mystreams:
        if stream.itag <= 251 and stream.itag >= 249:
            audio_obj = {}
            audio_obj["type"] = stream.type
            audio_obj["filesize"] = convert_size(stream._filesize)
            audio_obj["abr"] = stream.abr
            audio_obj["url"] = stream.url
            response["audio_streams"].append(audio_obj)
        
        elif stream.itag == 17 or stream.itag == 18 or stream.itag == 22:
            video_obj = {}
            video_obj["type"] = stream.type
            video_obj["filesize"] =  convert_size(stream._filesize)
            video_obj["resolution"] = stream.resolution
            video_obj["url"] = stream.url
            response["video_streams"].append(video_obj)
    return response