import os

try:
    from pytube import Playlist, YouTube
    from tqdm import tqdm
except ImportError as err:
    missing_package = str(err).split(' ')[-1]
    print(f"Error: {missing_package} package is not installed.")
    print(f"Please install {missing_package} using 'pip install {missing_package}' and try again.")
    os._exit(1)

def is_playlist_url(url):
    # Check if the URL contains "playlist" in it
    return 'playlist' in url.lower()

def extract_video_links(playlist):
    video_links = set()
    for url in playlist.video_urls:
        video_links.add(url)
    return video_links

def download_video(link, downloaded_videos, progress_bar):
    try:
        yt = YouTube(link)
        title = yt.title
        if title not in downloaded_videos:
            stream = yt.streams.get_highest_resolution()
            stream.download()
            downloaded_videos.add(title)
            progress_bar.update(1)
        else:
            progress_bar.write(f"Skipped: {title} (already downloaded)")
    except Exception as err:
        progress_bar.write(f"Error downloading video with URL {link}: {str(err)}")

def download_videos(video_links):
    downloaded_videos = set()
    with tqdm(total=len(video_links), desc="Overall Progress", dynamic_ncols=True) as overall_progress:
        for link in video_links:
            with tqdm(desc="Downloading", unit="video", dynamic_ncols=True) as progress_bar:
                download_video(link, downloaded_videos, progress_bar)
            overall_progress.update(1)

def main():
    url = input("Enter the URL of the YouTube playlist or video: ")
    if is_playlist_url(url):
        playlist = Playlist(url)
        video_links = extract_video_links(playlist)
    else:
        video_links = {url}
    download_videos(video_links)

if __name__ == "__main__":
    main()
