# YouTube Video Downloader 🎥

**YouTube Video Downloader** is a Python application using Tkinter and ttkbootstrap to download YouTube videos in MP4 format. This application has a modern interface and enables users to download videos and audio with various quality options.

## Features ✨

- **YouTube Video Download:** Enter the video URL and download it with a few clicks.
- **Audio Download:** Option to download only the audio track of the video.
- **Video Quality:** Select from the available video qualities.
- **Modern User Interface:** Utilizes ttkbootstrap for a modern and attractive look.
- **Open Download Directory:** Easily access the folder where videos are downloaded.
- **Clear Fields:** Automatically clears URL and quality fields after downloading for new use.

## Installation 🛠

1. Clone the repository:
   ```sh
   git clone https://github.com/x64maincpp/YouTube-Downloader.git
   cd YouTube-Downloader
   ```

2. Create and activate a virtual environment (Optional but recommended):
   ```sh
   python -m venv myenv
   source myenv/bin/activate # On Windows: myenv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

   *Ensure you have `ffmpeg` installed for audio-video conversion with `moviepy`.*

4. Run the application:
   ```sh
   python main.py
   ```

## Usage 🚀

1. Enter the YouTube video URL.
2. Click the "Fetch Video Details" button to retrieve the video's details.
3. Select the video quality.
4. (Optional) Check the option to download audio only.
5. Click "Download" to start downloading.
6. Once the download is complete, the URL and quality will be automatically cleared, ready for a new download.

## Code Overview 🧩

### Main Window (`YouTubeDownloader` class)

1. **Initializing the UI:** The application window is created using Tkinter and styled with ttkbootstrap. 
2. **Fetching Video Details:** When the user inputs a YouTube URL and clicks "Fetch Video Details," the `fetch_video_details` method connects to YouTube, retrieves video streams, and populates the quality options.
3. **Downloading Video:** When the "Download" button is pressed, the `download_video` method starts the download process based on the selected video quality and audio options.
4. **Showing Progress:** The `show_progress` method updates the progress bar during the download.
5. **Callbacks:** `success_callback` and `error_callback` handle the completion status of the download.

### Downloading Logic (`download_and_combine_video` function)

1. **Stream Download:** Download the selected stream based on user’s quality choices.
2. **Audio Handling:** Depending on the user’s choice, download audio separately or combine it with the video stream.
3. **Combining Video and Audio:** If separate audio is downloaded, the `moviepy` library is used to combine them into a single video file.

## Contributing 🔧

Contributions are welcome! Please create a pull request to propose changes.

## Acknowledgements 🙏

- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- [pytube](https://github.com/pytube/pytube)
- [moviepy](https://github.com/Zulko/moviepy)
