import moviepy.editor as mpy
from moviepy.video.fx.all import crop
import os
from pytube import YouTube 

def YTdownload(id, link):

    SAVE_PATH = "."

    try: 
        yt = YouTube(link) 
    except: 

        return False

    d_video = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()

    try: 
        d_video.download(output_path=SAVE_PATH)
        print('Video downloaded successfully!')

        return d_video.default_filename



    except: 
        print("Some Error!")
   

def cut_video(id, file, start, end):

    clip =  mpy.VideoFileClip(file) 
    clip = clip.subclip(start, end) 
    clip.write_videofile(f'{id}-done.mp4')

    os.remove(file)
    return f'{id}-done.mp4'

def edit_video(id, cutSilence, ratio, speedup, music):

    filename = id

    if cutSilence:
        os.system(f"auto-editor {filename}.mp4 --edit audio:threshold=-19dB")

        filename = f"{filename}_ALTERED.mp4"

    if speedup:
        clip = mpy.VideoFileClip(f'{filename}.mp4')
        duration = clip.duration 
        os.system(f"auto-editor {filename}.mp4 --video-speed {(duration/60)} --silent-speed 99999")

        filename = f"{filename}_ALTERED.mp4"
        
    if ratio:
        clip = mpy.VideoFileClip(f'{filename}.mp4')
        (w, h) = clip.size

        crop_width = h * 9/16
        
        x1, x2 = (w - crop_width)//2, (w+crop_width)//2
        y1, y2 = 0, h
        cropped_clip = crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)

        if not music:
            cropped_clip.write_videofile(f'{id}-done.mp4')
            filename = f'{id}-done'

        
    if music:    
        if not ratio:
            cropped_clip = mpy.VideoFileClip(f'{filename}.mp4')

        audio_background = mpy.AudioFileClip('effect_1.mp3')
        final_audio = mpy.CompositeAudioClip([cropped_clip.audio, audio_background])
        final_clip = cropped_clip.set_audio(final_audio)
        final_clip.write_videofile(f'{id}-done.mp4')

        filename = f'{id}-done'
    
    
    
    if cutSilence and speedup:
        os.remove(f'{id}_ALTERED_ALTERED.mp4')
        os.remove(f'{id}_ALTERED.mp4')
    elif cutSilence or speedup:
        os.remove(f'{id}_ALTERED.mp4')
        
    os.remove(f'{id}.mp4')

    return f'{filename}.mp4'
    


