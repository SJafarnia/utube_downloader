import os 
import random
import string
import time
from resources.utils import get_dwonload_progressbar

try:
    from pytube import Playlist, YouTube, Channel
    from pytube.exceptions import VideoUnavailable
except ImportError:
    raise ImportError(
        "No module named 'pytube' (pip install pytube) to install the package"
    )


cwd = os.getcwd()
inp = input("\n\nplease enter a youtube link...\n\n")
LINK = YouTube(inp)
# LINK = YouTube("http://www.youtube.com/watch?v=CrkvuW5Mw4s")


def random_string_generator():
    
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(12))
    
    return result_str


def get_streams(link):

    return link.streams.filter(progressive=True)


def get_vid_info(streams):
    items = []
    for i in streams:
        items.append({"resolution":i.resolution, "size":i.filesize_mb, "id":i.itag})
    
    return items


def dl_vid(streams, res):
    # streams.get_by_itag(int(itag)).download(output_path=f"{cwd}\media", filename_prefix=f"{random_string_generator()}_!_")
    vid = streams.filter(res=res).first()        
    vid.download(output_path=f"{cwd}\media", filename_prefix=f"{random_string_generator()}_!_")
    get_dwonload_progressbar(LINK, res)

def start_app():
    print("\n\napp is running, looking for available videos, this might take a few seconds...\n\n")
    
    try: 
        streams = get_streams(LINK)
    except VideoUnavailable:
        raise "Video URL invalid"

    results = get_vid_info(streams)

    print(f"search results for ***{LINK.title}*** : ")
    time.sleep(.5)
    for item in results:
        time.sleep(.5)
        print(
            f"    resolution: {item['resolution']}, size: {item['size']} Mbytes"
            )
            
    time.sleep(.5)
    chosen_q = input("\n\nenter your desired resolution (eg. :360 or 360p):\n\n     ")


    def avail_q(quality):
        
        
        q_list = []
        for item in results:
            q_list.append(item["resolution"])
        
        if quality[-1] != "p":
            quality = quality + "p"
        
        if quality in q_list:
            return quality
        else:
            print(f"\n\n sorry, '{quality}' is not a valid resolution, try again...\n\n")
            time.sleep(2)
            start_app()  
    
        
    def check_quality(quality):
                
        for item in results:
            if item["resolution"] == quality:
                time.sleep(.5)
                print(f"\n\n***selected resolution is {item['resolution']} with size of {item['size']} MegaBytes***")
                time.sleep(2)
                ans = input("\n\nproceed to downloading this file?(Y/n)\n\n   ") 
                return ans
        
    def check_rerun(answer, quality):
        time.sleep(1)
        if answer.lower() == "n":
            time.sleep(.5)
            rr = input('\n\ndownload declined, do you wish to run the script again?(y/n)\n\n  ')
            if rr.lower() == "n":
                pass
            elif rr.lower() == "y":
                start_app()
            else:
                print("\n\nsorry, couldn't understand that, please respond again")
                time.sleep(1)
                start_app()    
        elif answer.lower() == "y":    
            dl_vid(streams, quality)
        else:
            print("\n\nsorry, couldn't understand that, please respond again")
            time.sleep(1)
            start_app()

    # if chosen_q:
        # quality_check = check_quality(chosen_q)
        # check_rerun(quality_check, chosen_q)

    q_check = avail_q(chosen_q)
    if q_check:
        answer = check_quality(q_check)
        if answer :
            check_rerun(answer, q_check)



start_app()  
