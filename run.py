import subprocess
import sys
import time
import webbrowser


print("Starting FastAPI backend...")

backend = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "app.api:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ]
)


print("Waiting for FastAPI to start...")

time.sleep(5)


print("Starting Streamlit frontend...")

frontend = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app/frontend.py",
        "--server.port",
        "8501"
    ]
)


time.sleep(5)


print("Opening Enterprise AI Knowledge Assistant...")

webbrowser.open(
    "http://localhost:8501"
)


try:

    backend.wait()
    frontend.wait()

except KeyboardInterrupt:

    print("\nStopping application...")

    backend.terminate()
    frontend.terminate()

    print("Application stopped.")