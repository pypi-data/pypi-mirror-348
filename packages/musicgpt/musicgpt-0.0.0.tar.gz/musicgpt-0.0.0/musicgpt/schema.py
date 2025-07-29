from pydantic import BaseModel

from enum import Enum

class GetConversionResponse(BaseModel):
    success: bool
    conversion: dict

class SearchVoicesResponse(BaseModel):
    success: bool
    voices: list
    limit: int
    page: int
    total: int
    

class ResponseStatus(str, Enum): 
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    IN_QUEUE = "IN_QUEUE"
    ERROR = "ERROR"

class MusicGPTConversionType(str, Enum):
    TEXT_TO_SPEECH = "TEXT_TO_SPEECH"
    VOICE_CHANGER = "VOICE_CHANGER"
    MUSIC_AI = "MUSIC_AI"
    EXTRACTION = "EXTRACTION"
    COVER = "COVER"

class GenerateMusicRequest(BaseModel):
    music_style: str | None = None
    lyrics: str | None = None
    prompt: str | None = None
    negative_tags: str | None = None
    make_instrumental: bool = False
    vocal_only: bool = False
    webhook_url: str | None = None
    voice_id: str | None = None

class TextToSpeechRequest(BaseModel):
    text: str
    voice_id: str | None = None
    gender: str | None = None
    language: str | None = "en"
    webhook_url: str | None = None


class GenerateMusicResponse(BaseModel):
    success: bool
    message: str | None = None
    task_id: str
    conversion_id_1: str | None = None
    conversion_id_2: str | None = None
    eta: int
    task_status: ResponseStatus = ResponseStatus.IN_QUEUE
    conversion_type: MusicGPTConversionType


class ConversionResponse(BaseModel):
    success: bool
    message: str | None = None
    task_id: str
    conversion_id: str | None = None
    eta: int
    task_status: ResponseStatus = ResponseStatus.IN_QUEUE
    conversion_type: MusicGPTConversionType