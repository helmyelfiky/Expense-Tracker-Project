import os
import webbrowser
import time
from multiprocessing import Process
import requests

def start_server():
    # Start the Django development server
    os.system("python manage.py runserver")

def open_browser():
    # Wait for the server to start
    server_url = "http://127.0.0.1:8000"
    while True:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        time.sleep(1)  # Wait for 1 second before checking again

    # Open the Django app in the default web browser
    webbrowser.open(server_url)

if __name__ == "__main__":
    # Start the Django server in a separate process
    server_process = Process(target=start_server)
    server_process.start()

    # Open the browser (ensure this happens only once)
    open_browser()

    # Wait for the server process to terminate
    server_process.join()
