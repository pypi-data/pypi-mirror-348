# =============================================================================
#  Project       : GenomeNinja
#  File          : src/genome_ninja/utils/download_utils.py
#
#  Author        : Qinzhong Tian <tianqinzhong@qq.com>
#  Created       : 2025-05-15 15:52
#  Last Updated  : 2025-05-16 15:52
#     
#  Description   : Provides robust and feature-rich file downloading capabilities.
#                  Key features include:
#                  - Single and concurrent file downloads.
#                  - Resumable downloads for large files.
#                  - Automatic retries for transient network errors.
#                  - Configurable timeouts (connection and read).
#                  - Chunk-based downloading for efficient memory usage.
#                  - Pre-download disk space checking.
#                  - Rich progress bar display for interactive feedback.
#                  - Optional file hash verification (e.g., SHA256, MD5).
#                  - Automatic filename extraction from URL.
#                  - Unique filename generation to prevent overwrites.
#                  - Graceful handling of user interruptions (Ctrl+C).
#                  - Customizable download behavior via DownloadConfig dataclass.
#
#  Dependencies  : requests, rich 
#
#  Python        : Python 3.13.3
#  Version       : 1.0.0
#
#  Usage         : from genome_ninja.utils.download_utils import download_file, download_files
#                  
#                  # Single file download
#                  download_file("https://example.com/file.zip", "data/file.zip")
#                  
#                  # Concurrent download of multiple files
#                  files = [
#                      {"url": "https://example.com/file1.zip", "path": "data/file1.zip"},
#                      {"url": "https://example.com/file2.zip", "path": "data/file2.zip"}
#                  ]
#                  download_files(files)
#
#  Copyright © 2025 Qinzhong Tian. All rights reserved.
#  License       : MIT – see LICENSE in project root for full text.
# =============================================================================
from __future__ import annotations

import os
import sys
import time
import signal
import logging
import hashlib
import threading
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional, Union, Callable, Any, Tuple
from urllib.parse import urlparse, unquote
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rich.console import Console
from rich.progress import (
    Progress, 
    TextColumn, 
    BarColumn, 
    DownloadColumn, 
    TransferSpeedColumn, 
    TimeRemainingColumn,
    TaskID
)
from rich.logging import RichHandler

# Set up logging
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False, show_path=False)]
)
logger = logging.getLogger("download_utils")

# Custom logging function for user-friendly output
def log_info(message: str, url: str = None):
    """User-friendly information logging"""
    if url:
        # Truncate URL for cleaner display
        short_url = url
        if len(short_url) > 60:
            short_url = short_url[:57] + "..."
        logger.info(f"{message}: {short_url}")
    else:
        logger.info(message)

def log_error(message: str, error: Exception = None):
    """User-friendly error logging"""
    if error:
        logger.error(f"{message}: {str(error)}")
    else:
        logger.error(message)

# Console output
console = Console()

# Global variables for signal handling
_INTERRUPT_EVENT = threading.Event()
_ACTIVE_DOWNLOADS = {}  # Type: Dict[str, Tuple[TaskID, Progress]]

# Register signal handler
def _signal_handler(sig, frame):
    """Handle interrupt signal, set interrupt event flag"""
    console.print("\n[yellow]Interrupt signal received, stopping downloads... Please wait![/]")
    _INTERRUPT_EVENT.set()
    
    # Wait for all downloads to finish cleanup
    time.sleep(0.5)
    sys.exit(0)

# Register SIGINT signal handler (Ctrl+C)
signal.signal(signal.SIGINT, _signal_handler)

@dataclass
class DownloadConfig:
    """Download configuration class"""
    # Retry related
    max_retries: int = 3                # Maximum number of retries
    retry_backoff_factor: float = 0.5   # Retry backoff factor
    retry_status_forcelist: List[int] = None  # HTTP status codes to retry
    
    # Timeout related (seconds)
    connect_timeout: int = 10           # Connection timeout
    read_timeout: int = 30              # Read timeout
    
    # Download related
    chunk_size: int = 8192              # Chunk size (bytes)
    min_chunk_size: int = 1024          # Minimum chunk size for resuming
    resume_threshold: int = 1024 * 1024  # Resume threshold (1MB)
    
    # Disk related
    disk_space_buffer: float = 1.2      # Required disk space buffer factor
    
    # Concurrency related
    max_workers: int = 10                # Maximum concurrent downloads
    
    # Display related
    show_progress: bool = True          # Show progress bar
    
    # Verification related
    verify_hash: bool = False           # Verify hash value
    hash_algorithm: str = "sha256"      # Hash algorithm
    expected_hash: Optional[str] = None  # Expected hash value
    
    # Logging related
    log_level: int = logging.INFO       # Logging level
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.retry_status_forcelist is None:
            self.retry_status_forcelist = [429, 500, 502, 503, 504]
        
        # Set logging level
        logger.setLevel(self.log_level)

def get_filename_from_url(url: str) -> str:
    """Extract filename from URL"""
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    filename = os.path.basename(path)
    
    # If filename is empty, use domain + timestamp
    if not filename:
        filename = f"{parsed_url.netloc}_{int(time.time())}"
    
    return filename

def get_unique_filename(path: Path) -> Path:
    """
    Generate a unique filename to avoid name conflicts
    
    Args:
        path: Original file path
    
    Returns:
        Path: Unique file path
    """
    if not path.exists():
        return path
    
    # Split filename and extension
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    
    # Try adding a counter until a unique name is found
    counter = 1
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            log_info(f"Filename conflict, renamed to: {new_path.name}")
            return new_path
        counter += 1

def check_disk_space(path: Path, required_bytes: int, buffer: float = 1.2) -> bool:
    """
    Check if the target path has enough disk space
    
    Args:
        path: Target path
        required_bytes: Required number of bytes
        buffer: Buffer factor (default 1.2, i.e. 120% space required)
    
    Returns:
        bool: Whether there is enough space
    """
    try:
        # Ensure parent directory exists
        parent_dir = path.parent
        parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Get available space
        free_bytes = os.statvfs(parent_dir).f_frsize * os.statvfs(parent_dir).f_bavail
        required_with_buffer = int(required_bytes * buffer)
        
        if free_bytes < required_with_buffer:
            log_error(
                f"Insufficient disk space: Need {required_with_buffer/1024/1024:.2f}MB, "
                f"Available {free_bytes/1024/1024:.2f}MB"
            )
            return False
        return True
    except Exception as e:
        log_error("Error checking disk space", e)
        # If unable to check, assume enough space
        return True

def create_session(config: DownloadConfig) -> requests.Session:
    """Create a session configured with retry strategy"""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=config.max_retries,
        backoff_factor=config.retry_backoff_factor,
        status_forcelist=config.retry_status_forcelist,
        allowed_methods=["GET", "HEAD"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def get_file_size(url: str, session: requests.Session, config: DownloadConfig) -> Optional[int]:
    """Get remote file size"""
    try:
        response = session.head(
            url, 
            timeout=(config.connect_timeout, config.read_timeout),
            allow_redirects=True
        )
        response.raise_for_status()
        
        # Try to get file size from Content-Length header
        content_length = response.headers.get("Content-Length")
        if content_length:
            return int(content_length)
        
        log_info("Unable to get file size from response headers", url)
        return None
    except Exception as e:
        log_error("Error getting file size", e)
        return None

def calculate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """Calculate file hash value"""
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

def download_file(
    url: str, 
    save_path: Union[str, Path],
    config: Optional[DownloadConfig] = None,
    callback: Optional[Callable[[str, Path, bool], Any]] = None
) -> bool:
    """
    Download a single file, supports resuming
    
    Args:
        url: File URL
        save_path: Save path
        config: Download configuration
        callback: Callback function after download, receives (url, save_path, success)
    
    Returns:
        bool: Whether the download was successful
    """
    # Initialize configuration
    if config is None:
        config = DownloadConfig()
    
    # Convert path to Path object
    save_path = Path(save_path)
    
    # If save_path is a directory, get filename from URL
    if save_path.is_dir():
        filename = get_filename_from_url(url)
        save_path = save_path / filename
    
    # Ensure parent directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check for filename conflict and generate unique filename
    save_path = get_unique_filename(save_path)
    
    # Create session
    session = create_session(config)
    
    # Get file size
    file_size = get_file_size(url, session, config)
    if file_size is None:
        log_info("Unable to get file size, will continue downloading but cannot show progress percentage", url)
    # Check disk space
    if file_size and not check_disk_space(save_path, file_size, config.disk_space_buffer):
        if callback:
            callback(url, save_path, False)
        return False
    
    # Check if resuming is possible
    local_size = 0
    headers = {}
    resume_download = False
    
    if save_path.exists() and file_size and file_size > config.resume_threshold:
        local_size = save_path.stat().st_size
        
        # If local file is larger than remote file, delete local file and redownload
        if local_size > file_size:
            log_info(f"Local file ({local_size} bytes) is larger than remote file ({file_size} bytes), redownloading")
            save_path.unlink()
            local_size = 0
        # If local file size matches remote, verify hash if configured
        elif local_size == file_size:
            if config.verify_hash and config.expected_hash:
                actual_hash = calculate_file_hash(save_path, config.hash_algorithm)
                if actual_hash == config.expected_hash:
                    log_info(f"File exists and hash matches: {save_path}")
                    if callback:
                        callback(url, save_path, True)
                    return True
                else:
                    log_info(f"File hash mismatch, redownloading: {save_path}")
                    save_path.unlink()
                    local_size = 0
            else:
                log_info(f"File exists and size matches: {save_path}")
                if callback:
                    callback(url, save_path, True)
                return True
        # If local file is smaller, try to resume
        elif local_size < file_size:
            # Only resume if local file size exceeds minimum chunk size
            if local_size > config.min_chunk_size:
                headers["Range"] = f"bytes={local_size}-"
                resume_download = True
                log_info(f"Resuming download: {save_path.name} ({local_size}/{file_size} bytes downloaded)", url)
            else:
                # File too small, redownload
                save_path.unlink()
                local_size = 0
    
    # Prepare for download
    mode = "ab" if resume_download else "wb"
    success = False
    
    # Create progress bar with more user-friendly display
    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
        console=console,
        transient=True
    )
    
    try:
        with progress:
            # Add task with user-friendly download information
            # Extract last two levels of target directory for cleaner display
            target_dir = str(save_path.parent)
            if len(target_dir) > 30:
                parts = save_path.parent.parts
                if len(parts) >= 2:
                    target_dir = str(Path(parts[-2]) / parts[-1])
                else:
                    target_dir = "..." + target_dir[-27:]
            
            task_id = progress.add_task(
                f"Downloading {save_path.name} to {target_dir}", 
                total=file_size if file_size else None,
                completed=local_size if resume_download else 0
            )
            
            # Register to active downloads
            _ACTIVE_DOWNLOADS[str(save_path)] = (task_id, progress)
            
            # Start download
            response = session.get(
                url,
                headers=headers,
                stream=True,
                timeout=(config.connect_timeout, config.read_timeout)
            )
            response.raise_for_status()
            
            # If file size is not already known, get size from response headers
            if file_size is None:
                content_length = response.headers.get("Content-Length")
                if content_length:
                    file_size = int(content_length) + local_size if resume_download else int(content_length)
                    progress.update(task_id, total=file_size)
            
            with open(save_path, mode) as f:
                for chunk in response.iter_content(chunk_size=config.chunk_size):
                    if _INTERRUPT_EVENT.is_set():
                        log_info(f"Download cancelled: {save_path.name}", url)
                        # Do not delete partially downloaded file to allow next download
                        if callback:
                            callback(url, save_path, False)
                        return False
                    
                    if chunk:
                        f.write(chunk)
                        progress.update(task_id, advance=len(chunk))
            
            # Verify download
            if config.verify_hash and config.expected_hash:
                actual_hash = calculate_file_hash(save_path, config.hash_algorithm)
                if actual_hash != config.expected_hash:
                    log_error(
                        f"Hash mismatch: expected={config.expected_hash}, "
                        f"actual={actual_hash}"
                    )
                    if callback:
                        callback(url, save_path, False)
                    return False
            
            success = True
            log_info(f"Download successful: {save_path.name}", url)
            
    except requests.exceptions.HTTPError as e:
        log_error("HTTP Error", e)
    except requests.exceptions.ConnectionError as e:
        log_error("Connection Error", e)
    except requests.exceptions.Timeout as e:
        log_error("Request Timeout", e)
    except requests.exceptions.RequestException as e:
        log_error("Request Exception", e)
    except IOError as e:
        log_error("IO Error", e)
    except Exception as e:
        log_error("Unknown Error", e)
    finally:
        # Remove from active downloads
        if str(save_path) in _ACTIVE_DOWNLOADS:
            del _ACTIVE_DOWNLOADS[str(save_path)]
        
        # If download failed and was not resuming, delete non-complete file
        if not success and not resume_download and save_path.exists():
            try:
                save_path.unlink()
                log_info(f"Deleted incomplete file: {save_path.name}")
            except OSError as e:
                log_error(f"Could not delete incomplete file {save_path.name}", e)
        
        # Callback
        if callback:
            callback(url, save_path, success)
        
        return success

def download_files(
    files: List[Dict[str, str]],
    config: Optional[DownloadConfig] = None,
    callback: Optional[Callable[[str, Path, bool], Any]] = None
) -> Dict[str, bool]:
    """
    Download multiple files concurrently
    
    Args:
        files: List of files, each file is a dictionary containing 'url' and 'path' keys
        config: Download configuration
        callback: Callback function after each file download completes
    
    Returns:
        Dict[str, bool]: Mapping of URLs to download results
    """
    if config is None:
        config = DownloadConfig()
    
    # Preprocess file paths, check for duplicate target paths
    path_count = {}
    for file_info in files:
        path = str(file_info["path"])
        path_count[path] = path_count.get(path, 0) + 1
    
    # Log if duplicate paths exist
    duplicate_paths = [path for path, count in path_count.items() if count > 1]
    if duplicate_paths:
        log_info(f"Detected {len(duplicate_paths)} duplicate target paths, will auto-rename")
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        future_to_url = {
            executor.submit(
                download_file, 
                file_info["url"], 
                file_info["path"], 
                config, 
                callback
            ): file_info["url"]
            for file_info in files
        }
        
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                success = future.result()
                results[url] = success
            except Exception as e:
                log_error(f"Exception occurred during download: {url}", e)
                results[url] = False
    
    # Summarize results
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    log_info(f"Download completed: {success_count}/{total_count} files successful")
    
    return results
