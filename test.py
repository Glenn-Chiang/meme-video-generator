from moviepy.editor import VideoFileClip, AudioFileClip

def main():    
    video_filepath = f'tmp/video.mp4'
    video = VideoFileClip(video_filepath)
    audio = AudioFileClip('assets/music.mp3')
    final_video: VideoFileClip = video.set_audio(audio)
    final_video.write_videofile(f'tmp/video_final.mp4')


if __name__=='__main__':
    main()