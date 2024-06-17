import logging
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from concurrent.futures import ThreadPoolExecutor
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pytube import YouTube
from utils import download_and_combine_video

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR
)

class YouTubeDownloader(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Initialize the window with a theme
        self.youtube = None
        self.quality_options = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.downloading = False

        self.setup_ui()

    def setup_ui(self):
        self.title("YouTube Video Downloader")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # URL Frame
        self.url_frame = ttk.Frame(self)
        self.url_frame.pack(pady=10)
        
        self.url_label = ttk.Label(self.url_frame, text="YouTube URL:")
        self.url_label.pack(side=tk.LEFT, padx=5)
        
        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        
        self.fetch_button = ttk.Button(
            self.url_frame, text="Fetch Video Details", command=self.fetch_video_details, bootstyle="primary")
        self.fetch_button.pack(side=tk.LEFT, padx=5)
        
        # Update clear_button to be a cross 'X'
        self.clear_button = ttk.Button(
            self.url_frame, text="X", command=self.clear_url, bootstyle="secondary")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Quality Frame
        self.quality_frame = ttk.Frame(self)
        self.quality_frame.pack(pady=10)
        
        self.quality_label = ttk.Label(self.quality_frame, text="Select Quality:")
        self.quality_label.pack(side=tk.LEFT, padx=5)
        
        self.quality_combobox = ttk.Combobox(self.quality_frame, state="readonly", width=40)
        self.quality_combobox.pack(side=tk.LEFT, padx=5)
        
        self.download_button = ttk.Button(
            self.quality_frame, text="Download", command=self.download_video, state=tk.DISABLED, bootstyle="success")
        self.download_button.pack(side=tk.LEFT, padx=5)
        
        self.open_dir_button = ttk.Button(
            self.quality_frame, text="Open Directory", command=self.open_download_directory, bootstyle="info")
        self.open_dir_button.pack(side=tk.LEFT, padx=5)

        # Audio Options
        self.audio_frame = ttk.Frame(self)
        self.audio_frame.pack(pady=10)
        
        self.download_audio_var = tk.BooleanVar(value=True)
        self.download_audio_check = ttk.Checkbutton(
            self.audio_frame, text="Download Audio", variable=self.download_audio_var, bootstyle="primary", command=self.toggle_audio_options)
        self.download_audio_check.pack(side=tk.LEFT, padx=5)

        self.audio_separate_var = tk.BooleanVar(value=False)
        self.audio_separate_check = ttk.Checkbutton(
            self.audio_frame, text="Separate Audio", variable=self.audio_separate_var, bootstyle="secondary")
        self.audio_separate_check.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(pady=10)
        
        self.progressbar = Progressbar(self.progress_frame, mode="determinate", length=400)
        self.progressbar.pack(pady=10)
        
        self.clear_console_button = ttk.Button(
            self.progress_frame, text="Clear Console", command=self.clear_console, bootstyle="warning")
        self.clear_console_button.pack(pady=10)

        # Status Message
        self.status_label = ttk.Label(self, text="", bootstyle="success")
        self.status_label.pack(pady=10)

        # Detailed Status
        self.detailed_status = tk.Text(self, height=10, wrap='word', state=tk.DISABLED, background="#333", foreground="#ffffff")
        self.detailed_status.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def log_status(self, message):
        self.detailed_status.config(state=tk.NORMAL)
        self.detailed_status.insert(tk.END, message + "\n")
        self.detailed_status.see(tk.END)
        self.detailed_status.config(state=tk.DISABLED)
        self.update_idletasks()

    def clear_url(self):
        self.url_entry.delete(0, tk.END)
        self.log_status("URL cleared.")
        self.download_button.config(state=tk.DISABLED)
        self.clear_quality()

    def clear_quality(self):
        self.quality_combobox.set('')
        self.quality_combobox["values"] = []
        self.log_status("Quality cleared.")

    def open_download_directory(self):
        download_directory = os.getcwd()
        webbrowser.open(download_directory)
        self.log_status(f"Opened directory: {download_directory}")

    def clear_console(self):
        self.detailed_status.config(state=tk.NORMAL)
        self.detailed_status.delete(1.0, tk.END)
        self.detailed_status.config(state=tk.DISABLED)
        self.log_status("Console cleared.")

    def fetch_video_details(self):
        if self.downloading:
            messagebox.showwarning("Warning", "A download is already in progress.")
            return

        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL.")
            return

        self.log_status(f"Fetching video details for {url}...")
        try:
            self.youtube = YouTube(url, on_progress_callback=self.show_progress)
            streams = self.youtube.streams.filter(file_extension="mp4").order_by("resolution").desc()
            self.quality_options = {f"{stream.resolution} {stream.abr or ''}".strip(): stream for stream in streams if stream.resolution or stream.abr}
            self.quality_combobox["values"] = list(self.quality_options.keys())
            if not self.quality_options:
                raise ValueError("No MP4 streams available")
            self.status_label.config(text="Video details fetched successfully", bootstyle="success")
            self.log_status("Video details fetched successfully.")
            self.quality_combobox.current(0)
            self.download_button.config(state=tk.NORMAL)
        except Exception as e:
            logging.error(f"Error fetching video details: {e}")
            self.status_label.config(text="Error fetching video details", bootstyle="danger")
            messagebox.showerror("Error", f"Unable to fetch video details: {e}")

    def toggle_audio_options(self):
        if self.download_audio_var.get():
            self.audio_separate_check.config(state=tk.NORMAL)
        else:
            self.audio_separate_check.config(state=tk.DISABLED)
            self.audio_separate_var.set(False)

    def download_video(self):
        if self.downloading:
            messagebox.showwarning("Warning", "A download is already in progress.")
            return

        selected_quality = self.quality_combobox.get()
        if not selected_quality:
            messagebox.showwarning("Warning", "Please select a quality")
            return

        self.downloading = True
        self.log_status(f"Starting download in {selected_quality} quality...")
        try:
            self.progressbar["value"] = 0
            self.status_label.config(text="Downloading...", bootstyle="info")
            download_audio = self.download_audio_var.get()
            separate_audio = self.audio_separate_var.get()
            self.executor.submit(download_and_combine_video, self.youtube, self.quality_options, selected_quality, download_audio, separate_audio,
                                 self.log_status, self.progressbar, self.success_callback, self.error_callback)
        except Exception as e:
            logging.error(f"Error starting download: {e}")
            self.progressbar.stop()
            self.downloading = False
            self.status_label.config(text="Error starting download", bootstyle="danger")
            messagebox.showerror("Error", f"An error occurred while starting the download: {e}")

    def success_callback(self, final_file):
        self.downloading = False
        self.status_label.config(text="Download completed successfully", bootstyle="success")
        self.log_status("Download completed successfully.")
        messagebox.showinfo("Success", f"Video downloaded successfully as {final_file}")
        self.clear_url()  # Clear the URL entry box and reset the quality combobox after download success

    def error_callback(self, error_message):
        self.downloading = False
        self.status_label.config(text="Error during download", bootstyle="danger")
        self.log_status(f"An error occurred: {error_message}")
        messagebox.showerror("Error", f"An error occurred while downloading the video: {error_message}")

    def show_progress(self, stream, chunk, remaining):
        try:
            total_size = stream.filesize
            bytes_downloaded = total_size - remaining
            percentage_of_completion = (bytes_downloaded / total_size) * 100
            self.progressbar["value"] = percentage_of_completion
            self.update_idletasks()
            self.log_status(f"Downloaded {percentage_of_completion:.2f}%")
        except Exception as e:
            logging.error(f"Error showing progress: {e}")
            self.status_label.config(text="Error showing progress", bootstyle="danger")
            self.log_status("Error showing progress")

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()