import argparse
from pathlib import Path
from yt_dlp import YoutubeDL
class YouTubeDownloader:
   """
   A class to download YouTube videos using yt-dlp without requiring ffmpeg.
   """
   def __init__(self, url, output_path=None, quality=None):
       self.url = url
       self.output_path = output_path or str(Path.cwd())
       # Only select formats that already include both video and audio
       self.quality = quality or "best[ext=mp4]/best"
       self.ydl_opts = {
           'format': self.quality,
           'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',
           'progress_hooks': [self._hook],
           'quiet': False,
           # No postprocessors, no ffmpeg
       }
   def download(self):
       try:
           with YoutubeDL(self.ydl_opts) as ydl:
               ydl.download([self.url])
       except Exception as e:
           print(f"❌ Download failed: {e}")
   def _hook(self, d):
       if d['status'] == 'downloading':
           print(f"⬇️ Downloading: {d['_percent_str']} of {d['_total_bytes_str']}")
       elif d['status'] == 'finished':
           print(f"✅ Download completed: {d['filename']}")
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="YouTube Downloader using yt-dlp (no ffmpeg)")
   parser.add_argument("url", help="YouTube video URL")
   parser.add_argument("-q", "--quality", help="Video quality (e.g. best, 720p)", default=None)
   parser.add_argument("-o", "--output_path", help="Output directory", default=None)
   args = parser.parse_args()
   downloader = YouTubeDownloader(
       url=args.url,
       quality=args.quality,
       output_path=args.output_path,
   )
   downloader.download()