import subprocess
import sys
import signal
import atexit
import shutil
import os
import platform
import requests
import stat
from pathlib import Path
import time
import socket
import errno
import re

_cloudflared_process = None
_jlab_process = None

# Define a directory to store the downloaded binary
DOWNLOAD_DIR = Path.home() / ".jovyanai" / "bin"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
CLOUDFLARED_PATH = DOWNLOAD_DIR / "cloudflared"


def _get_cloudflared_download_url():
    """Determines the cloudflared download URL for the current OS/Arch."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine == "aarch64":
            arch = "arm64"
        else:
            return None, f"Unsupported Linux architecture: {machine}"
        filename = f"cloudflared-linux-{arch}"
    elif system == "darwin": # macOS
        if machine == "x86_64":
            arch = "amd64"
        elif machine == "arm64": # Apple Silicon
             arch = "arm64"
        else:
            return None, f"Unsupported macOS architecture: {machine}"
        filename = f"cloudflared-darwin-{arch}.tgz" # Needs extraction later
    elif system == "windows":
        if machine in ["x86_64", "amd64"]:
             arch = "amd64"
        else:
             return None, f"Unsupported Windows architecture: {machine}"
        filename = f"cloudflared-windows-{arch}.exe"
    else:
        return None, f"Unsupported operating system: {system}"

    url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/{filename}"
    return url, filename


def _download_and_extract(url, filename, dest_path):
    """Downloads and extracts/saves the cloudflared binary."""
    print(f"Downloading cloudflared from {url}...", file=sys.stderr)
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        temp_download_path = dest_path.parent / (filename + ".tmp")

        with open(temp_download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Download complete.", file=sys.stderr)

        if filename.endswith(".tgz"):
             print(f"Extracting {temp_download_path}...", file=sys.stderr)
             import tarfile
             with tarfile.open(temp_download_path, "r:gz") as tar:
                 # Find the binary within the archive (common names)
                 binary_member = None
                 for member in tar.getmembers():
                     if member.name == 'cloudflared' or member.name.endswith('/cloudflared'):
                         binary_member = member
                         break
                 if not binary_member:
                     raise RuntimeError("Could not find 'cloudflared' binary in the downloaded archive.")
                 binary_member.name = dest_path.name # Extract directly with the final name
                 tar.extract(binary_member, path=dest_path.parent)
             print("Extraction complete.", file=sys.stderr)
             temp_download_path.unlink() # Clean up archive
        else:
            # For non-archives (Linux .deb/.rpm, Windows .exe), just rename
            temp_download_path.rename(dest_path)

        # Make executable
        current_stat = os.stat(dest_path)
        os.chmod(dest_path, current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"cloudflared saved to {dest_path} and made executable.", file=sys.stderr)
        return dest_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading cloudflared: {e}", file=sys.stderr)
        if temp_download_path.exists():
             temp_download_path.unlink()
        return None
    except Exception as e:
        print(f"Error processing downloaded file: {e}", file=sys.stderr)
        if temp_download_path.exists():
             temp_download_path.unlink()
        if dest_path.exists(): # Clean up partially extracted file
            dest_path.unlink()
        return None


def ensure_cloudflared():
    """Checks for cloudflared, downloads if needed, returns executable path."""
    # 1. Check PATH
    cloudflared_path = shutil.which("cloudflared")
    if cloudflared_path:
        print(f"Found cloudflared in PATH: {cloudflared_path}", file=sys.stderr)
        return cloudflared_path

    # 2. Check local download directory
    if CLOUDFLARED_PATH.exists() and os.access(CLOUDFLARED_PATH, os.X_OK):
        print(f"Found downloaded cloudflared: {CLOUDFLARED_PATH}", file=sys.stderr)
        return str(CLOUDFLARED_PATH)

    # 3. Download
    print(f"cloudflared not found, attempting download to {DOWNLOAD_DIR}...", file=sys.stderr)
    url, filename = _get_cloudflared_download_url()
    if not url:
        print(f"Error: {filename}", file=sys.stderr) # filename contains the error message here
        return None

    executable_path = _download_and_extract(url, filename, CLOUDFLARED_PATH)
    return executable_path


def _cleanup_processes(signum=None, frame=None):
    """Gracefully terminate child processes."""
    global _cloudflared_process, _jlab_process

    processes_to_stop = []
    if _jlab_process and _jlab_process.poll() is None:
        processes_to_stop.append(("JupyterLab", _jlab_process))
    if _cloudflared_process and _cloudflared_process.poll() is None:
        processes_to_stop.append(("cloudflared", _cloudflared_process))

    if not processes_to_stop:
        return

    for name, proc in processes_to_stop:
        print(f"Stopping {name} (PID {proc.pid})...", file=sys.stderr, end="")
        if proc.poll() is None: # Check again if it terminated in the meantime
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print(" stopped.", file=sys.stderr)
            except subprocess.TimeoutExpired:
                print(" timeout, killing...", file=sys.stderr, end="")
                proc.kill()
                proc.wait(timeout=5)
                print(" killed.", file=sys.stderr)
            except Exception as e:
                print(f" error: {e}", file=sys.stderr)
                if proc.poll() is None:
                    print(f" {name} (PID {proc.pid}) seems to have stopped despite signal error.", file=sys.stderr)

    _cloudflared_process = None
    _jlab_process = None
    # Add a small delay to allow terminal output to flush
    time.sleep(0.1)


def _find_available_port(start_port=8888, max_tries=100):
    """Finds an available TCP port starting from start_port."""
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                print(f"Found available port: {port}", file=sys.stderr)
                return port
            except OSError as e:
                if e.errno == errno.EADDRINUSE: # Address already in use
                    print(f"Port {port} is in use, trying next...", file=sys.stderr)
                    continue
                else:
                    # Other socket error, re-raise
                    raise
    print(f"Could not find an available port after {max_tries} tries starting from {start_port}.", file=sys.stderr)
    return None

def _start_jlab(jlab_port):
    """Starts JupyterLab on the given port."""
    jlab_command = ["jupyter", "lab",
        "--ip=0.0.0.0",
        f"--port={jlab_port}",
        "--no-browser",
        "--ServerApp.token=''",
        "--ServerApp.allow_origin='*'"]
    print(f"Starting JupyterLab on port {jlab_port}...", file=sys.stderr)

    log_file_handle = open("jlab.log", "w")
    # Note: Consider making log_file_handle global and closing it in _cleanup_processes
    _jlab_process = subprocess.Popen(
        jlab_command,
        stdout=log_file_handle,
        stderr=log_file_handle
    )

    # wait 15s check every second the log to see if JupyterLab is running
    max_wait_time = 15 # seconds
    start_time = time.time()
    jlab_started = False
    log_file_path = "jlab.log"

    print(f"Waiting up to {max_wait_time}s for JupyterLab to start...", file=sys.stderr)
    while time.time() - start_time < max_wait_time:
        try:
            with open(log_file_path, "r") as f:
                log_content = f.read()
                # Check for the success message indicating the server is ready
                if "Use Control-C to stop this server" in log_content:
                    print("JupyterLab is running.", file=sys.stderr)
                    jlab_started = True
                    break # Exit the loop on success
                # Optional: Check for common early error indicators if needed
                # elif "ERROR" in log_content or "Traceback" in log_content:
                #     print("Detected potential error during JupyterLab startup.", file=sys.stderr)
                #     # Decide if you want to break early on error or let the timeout handle it
                #     # break

        except FileNotFoundError:
            # Log file might not be created yet, just wait
            pass
        except Exception as e:
            # Handle other potential file reading errors gracefully
            print(f"Warning: Error reading log file {log_file_path}: {e}", file=sys.stderr)

        # Wait for 1 second before checking again
        time.sleep(1)

    if not jlab_started:
        error_message = f"JupyterLab failed to start within {max_wait_time} seconds. "
        error_message += f"Please check the log file '{log_file_path}' for more information. "
        error_message += "And contact Jovyan AI's support if the problem persists."
        # Try to provide the tail of the log for easier debugging
        try:
            with open(log_file_path, "r") as f:
                # Read last N lines or characters
                log_tail = "".join(f.readlines()[-20:]) # Get last 20 lines
                if log_tail:
                     error_message += f"\n\n--- Last part of {log_file_path} ---\n{log_tail}\n--------------------------"
        except Exception: # Catch FileNotFoundError or other read errors
            error_message += f"\nCould not read the log file '{log_file_path}'."

        # Ensure the process is cleaned up if startup failed
        if _jlab_process and _jlab_process.poll() is None:
            print("Terminating non-responsive JupyterLab process...", file=sys.stderr)
            _jlab_process.terminate()
            try:
                _jlab_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                _jlab_process.kill()
                _jlab_process.wait(timeout=2)

        raise RuntimeError(error_message)

    # Return the process handle only if successful startup was confirmed
    return _jlab_process


def _start_cloudflared(port):
    """Starts a cloudflared tunnel for the given URL."""
    cloudflared_executable = ensure_cloudflared()

    if not cloudflared_executable:
        raise RuntimeError("Could not find or install cloudflared. Exiting.")

    tunnel_url = f"http://localhost:{port}"
    log_file_handle = open("cloudflared.log", "w")
    try:
        print(f"Creating a Cloudflare URL to access JupyterLab at port {port}...", file=sys.stderr)
        _cloudflared_process = subprocess.Popen(
            [str(cloudflared_executable), "tunnel", "--url", tunnel_url,
             "--protocol", "http2", "--no-autoupdate"],
            stdout=log_file_handle,
            stderr=log_file_handle
        )
        time.sleep(5)
        # Check the log file and retrieve the tunnel URL
        cloudflared_url = None
        max_wait_time = 15 # seconds
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            try:
                with open("cloudflared.log", "r") as f:
                    log_content = f.read()
                    # Regex to find the specific URL format
                    # Match the line starting with 'Visit it at...', skip to the next line, find 'INF |', spaces, and capture the URL
                    match = re.search(r"Visit it at \(it may take some time to be reachable\):[\s|]*\n.*?INF\s+\|\s+(https://[\w.-]+\.trycloudflare\.com)", log_content)
                    if match:
                        cloudflared_url = match.group(1).strip()
                        break # Found the URL
            except FileNotFoundError:
                pass # Log file might not exist yet
            time.sleep(1) # Wait a bit before checking again

        if cloudflared_url:
            print(f"Cloudflare URL created. Access your JupyterLab at {cloudflared_url}", file=sys.stderr)
            return _cloudflared_process
        else:
             # Check log again for errors if URL not found
             error_message = "Cloudflared tunnel URL not found in logs after waiting."
             try:
                 with open("cloudflared.log", "r") as f:
                     log_content = f.read()
                     if "error" in log_content.lower() or "failed" in log_content.lower():
                         error_message += f" Found potential errors in cloudflared.log:\n{log_content[-500:]}" # Show last 500 chars
             except FileNotFoundError:
                 error_message += " cloudflared.log file not found."
             raise RuntimeError(error_message)

    except Exception as e:
        raise RuntimeError(f"Error starting cloudflared: {e}")
    

def start_jlab():
    """Starts JupyterLab and a cloudflared tunnel."""
    global _cloudflared_process, _jlab_process

    # Find an available port for JupyterLab
    jlab_port = _find_available_port()
    if jlab_port is None:
        raise RuntimeError("Could not find an available port for JupyterLab. Exiting.")

    # Register cleanup handlers *after* we know we can proceed
    atexit.register(_cleanup_processes)
    signal.signal(signal.SIGTERM, _cleanup_processes)
    signal.signal(signal.SIGINT, _cleanup_processes) # Handle Ctrl+C

    jlab_port = str(jlab_port) # Ensure it's a string for f-string and command arg
    
    try:
        _jlab_process = _start_jlab(jlab_port)
        _cloudflared_process = _start_cloudflared(jlab_port)
        _jlab_process.wait()

    except KeyboardInterrupt:
        raise KeyboardInterrupt("\nJupyterLab interrupted by user.")

        # Cleanup will be handled by the signal handler and atexit
    except Exception as e:
        raise RuntimeError(f"Error running JupyterLab: {e}")
    finally:
        # Explicitly call cleanup when JLab finishes or fails.
        # atexit handles normal exit, signal handlers handle interruption.
        # This ensures cloudflared stops if JLab crashes.
        _cleanup_processes()
        sys.exit(0) # Ensure clean exit code after cleanup


if __name__ == "__main__":
    start_jlab() 