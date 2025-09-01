import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import threading
import re

cookies_file_path = ""

def select_cookies_file():
    global cookies_file_path
    cookies_file_path = filedialog.askopenfilename(
        title="Select Cookies File",
        filetypes=[("Text Files", "*.txt")]
    )
    if cookies_file_path:
        lbl_cookies.config(text=f"Cookies: {os.path.basename(cookies_file_path)}")

def colorize_line(line):
    if re.search(r'\[download\] Destination', line):
        return 'green'
    elif re.search(r'has already been downloaded', line):
        return 'orange'
    elif re.search(r'ERROR|failed', line, re.IGNORECASE):
        return 'red'
    else:
        return 'black'

def download_playlist_thread(url, output_dir):
    try:
        command = [
            "yt-dlp",
            "--cookies", cookies_file_path,
            "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--embed-metadata",
            "--embed-thumbnail",
            "--add-metadata",
            "--parse-metadata", "playlist_title:%(album)s",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            url
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            color = colorize_line(line)
            txt_output.insert(tk.END, line, color)
            txt_output.see(tk.END)
        
        process.wait()
        if process.returncode == 0:
            messagebox.showinfo("Success", "Playlist downloaded successfully!")
        else:
            messagebox.showerror("Error", "Download failed. Check the output for details.")

    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{str(e)}")

def download_playlist():
    url = entry_url.get().strip()
    output_dir = filedialog.askdirectory(title="Select Download Folder")

    if not url or not output_dir or not cookies_file_path:
        messagebox.showerror(
            "Error",
            "Please enter a playlist URL, select a folder, and select a cookies file."
        )
        return

    txt_output.delete(1.0, tk.END)
    threading.Thread(target=download_playlist_thread, args=(url, output_dir), daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("YouTube Playlist to MP3 Downloader")

tk.Label(root, text="Enter YouTube Playlist URL:").pack(pady=5)
entry_url = tk.Entry(root, width=60)
entry_url.pack(pady=5)

btn_cookies = tk.Button(root, text="Select Cookies File", command=select_cookies_file)
btn_cookies.pack(pady=5)

lbl_cookies = tk.Label(root, text="No cookies selected")
lbl_cookies.pack(pady=5)

btn_download = tk.Button(root, text="Download Playlist", command=download_playlist)
btn_download.pack(pady=10)

tk.Label(root, text="Download Output:").pack(pady=5)
txt_output = scrolledtext.ScrolledText(root, width=80, height=20)
txt_output.pack(pady=5)

txt_output.tag_config('green', foreground='green')
txt_output.tag_config('orange', foreground='orange')
txt_output.tag_config('red', foreground='red')
txt_output.tag_config('black', foreground='black')

root.mainloop()
