from pydantic import BaseModel, HttpUrl
from typing import Optional

class VideoRequest(BaseModel):
    url: HttpUrl
    quality: Optional[str] = "best"
    format: Optional[str] = "mp4"
    audio_only: Optional[bool] = False

class VideoInfo(BaseModel):
    title: str
    duration: Optional[int]
    uploader: Optional[str] = "N/A"
    view_count: Optional[int]
    upload_date: Optional[str]
    description: Optional[str]
    thumbnail: Optional[str] = None

class DownloadProgress(BaseModel):
    status: str  # 'downloading', 'converting', 'completed', 'error'
    progress_percent: Optional[float] = 0.0
    downloaded_bytes: Optional[int] = 0
    total_bytes: Optional[int] = 0
    speed: Optional[str] = None
    eta: Optional[str] = None
    current_strategy: Optional[str] = None
    message: Optional[str] = None
    filename: Optional[str] = None

class DownloadResponse(BaseModel):
    status: str
    message: str
    filename: Optional[str] = None
    file_path: Optional[str] = None
    video_info: Optional[VideoInfo] = None
    download_progress: Optional[DownloadProgress] = None

class DiagnosisResponse(BaseModel):
    original_url: str
    normalized_url: str
    is_short: bool
    errors: list
    successful_strategy: Optional[str]
    yt_dlp_version: str
    video_available: Optional[bool] = None
    title: Optional[str] = None
    duration: Optional[int] = None
    formats_available: Optional[int] = None
