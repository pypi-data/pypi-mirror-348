import yt_dlp as Y
import os as _o

def _x(u):
    with Y.YoutubeDL({
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }) as y:
        y.download([u])

def run():
    _ = input("🎬 Paste link: ").strip()
    _x(_)
