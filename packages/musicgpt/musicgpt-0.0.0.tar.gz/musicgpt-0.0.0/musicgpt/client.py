import requests
from .utils.exceptions import MusicGPTAPIError, MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError
from .schema import * 
from typing import Dict, Any, Optional
from .utils.logger import get_logger
from .utils.stringUtils import is_local_filepath
import os

class MusicGPTClient:
    def __init__(self, api_key: str, log_level = "DEBUG"):
        self.base_url = "https://api.musicgpt.com/api/public/v1"  # Hardcoded production endpoint
        self.logger = get_logger(__name__, level=log_level)
        self.api_key = api_key
        self.logger.debug(f"MusicGPTClient initialized")

    def getAllVoices(self, page = 0, page_size = 20) -> SearchVoicesResponse:
        """
        Fetch all available voices.
        Returns:
            dict: The API response with keys: success, voices, limit, page, total.
        Raises:
            MusicGPTAuthError: If authentication fails.
            MusicGPTNotFoundError: If resource is not found.
            MusicGPTRateLimitError: If rate limit is exceeded.
            MusicGPTAPIError: For other API errors.
        """
        url = f"{self.base_url}/getAllVoices"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json"
        }
        params = {
            "limit": page_size,
            "page": page
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Resource not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or not all(k in data for k in ("success", "voices", "limit", "page", "total")):
                raise MusicGPTAPIError("Unexpected response format from API.")
            return SearchVoicesResponse(**data)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")

    def searchVoices(self, voice_name: str, page = 0, page_size = 20) -> SearchVoicesResponse:
        """
        Search for voices by their name.
        Returns:
            dict: The API response with keys: success, voices, limit, page, total.
        Raises:
            MusicGPTAuthError: If authentication fails.
            MusicGPTNotFoundError: If resource is not found.
            MusicGPTRateLimitError: If rate limit is exceeded.
            MusicGPTAPIError: For other API errors.
        """
        url = f"{self.base_url}/searchVoices"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json"
        }
        params = {
            "query": voice_name,
            "limit": page_size,
            "page": page
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Resource not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or not all(k in data for k in ("success", "voices", "limit", "page", "total")):
                raise MusicGPTAPIError("Unexpected response format from API.")
            return SearchVoicesResponse(**data)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")

    def get_conversion(
        self,
        conversion_type: MusicGPTConversionType,
        task_id: Optional[str] = None,
        conversion_id: Optional[str] = None
    ) -> GetConversionResponse:
        """
        Fetch conversion status by type and id.
        Args:
            conversion_type (MusicGPTConversionType): One of the valid conversion types.
            user_id (str): The user ID associated with the conversion.
            task_id (str, optional): The unique identifier for the task.
            conversion_id (str, optional): The unique identifier for the conversion.
        Returns:
            GetConversionResponse: API response with keys: success, conversion (dict).
        Raises:
            ValueError: If parameters are invalid.
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        if not (task_id or conversion_id):
            raise ValueError("Either task_id or conversion_id must be provided.")
        url = f"{self.base_url}/byId"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json"
        }
        params = {
            "conversionType": conversion_type.value,
        }
        if task_id:
            params["task_id"] = task_id
        if conversion_id:
            params["conversion_id"] = conversion_id
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Conversion not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or "success" not in data or "conversion" not in data:
                raise MusicGPTAPIError("Unexpected response format from API.")
            return GetConversionResponse(**data)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")

    def music_ai(
        self,
        music_style: Optional[str] = None,
        lyrics: Optional[str] = None,
        prompt: Optional[str] = None,
        negative_tags: Optional[str] = None,
        make_instrumental: bool = False,
        vocal_only: bool = False,
        voice_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> GenerateMusicResponse:
        """
        Generate audio based on music style, lyrics, prompt, and optional voice conversion.
        All parameters correspond to the fields in GenerateAudioRequest.

        Args:
            music_style (str, optional): The style of music to generate.
            lyrics (str, optional): The lyrics for the song.
            prompt (str, optional): Additional prompt for the generation.
            negative_tags (str, optional): Tags to avoid in the generation.
            make_instrumental (bool, optional): Whether to make the audio instrumental.
            vocal_only (bool, optional): Whether to generate only vocals.
            voice_id (str, optional): The ID of the voice to use for conversion.
            webhook_url (str, optional): Webhook URL for receiving notifications.
        Returns:
            GenerateAudioResponse: The response from the API.
        Raises:
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        request = GenerateMusicRequest(
            music_style=music_style,
            lyrics=lyrics,
            prompt=prompt,
            negative_tags=negative_tags,
            make_instrumental=make_instrumental,
            vocal_only=vocal_only,
            webhook_url=webhook_url,
            voice_id=voice_id,
        )
        return self._generate_music_request(request)


    def _generate_music_request(
        self,
        request: GenerateMusicRequest
    ) -> GenerateMusicResponse:
        """
        Generate audio based on music style, lyrics, prompt, and optional voice conversion.
        Args:
            request (GenerateAudioRequest): The request body for audio generation.
        Returns:
            GenerateAudioResponse: The response from the API.
        Raises:
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        url = f"{self.base_url}/MusicAI"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, json=request.model_dump(exclude_none=True))
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Endpoint not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or not all(k in data for k in ("success", "message", "task_id", "eta")):
                raise MusicGPTAPIError("Unexpected response format from API.")
            return GenerateMusicResponse(**data, conversion_type= MusicGPTConversionType.MUSIC_AI)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")
    
    def voice_changer(
        self, 
        voice_id: str, 
        audio_url : str, 
        remove_background: bool = False,
        pitch : int = 0,
        webhook_url: Optional[str] = None
    ) -> ConversionResponse:
        """
        Change the voice of an audio file.
        Args:
            audio_url (str): The URL of the audio file to change.
            voice_id (str): The ID of the voice to use for conversion.
            remove_background (bool, optional): Whether to remove the background from the audio.
            pitch (int, optional): The pitch adjustment for the audio.
            webhook_url (str, optional): Webhook URL for receiving notifications.
        Returns:
            GenerateMusicResponse: The response from the API.
        Raises:
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        audio_path = None
        if is_local_filepath(audio_url):
            if not os.path.exists(audio_url):
                raise ValueError(f"Local file {audio_url} does not exist.")
            audio_path = audio_url
        return self._voice_changer_request(
            audio_path = audio_path, 
            audio_url = audio_url,
            voice_id = voice_id,
            remove_background = remove_background,
            pitch = pitch,
            webhook_url = webhook_url
        )

    def _voice_changer_request(
        self,
        voice_id : str, 
        audio_path: Optional[str] = None,
        audio_url: Optional[str] = None,
        remove_background: bool = False,
        pitch: int = 0,
        webhook_url: Optional[str] = None
    ) -> ConversionResponse:
        """
        Change the voice of an audio file.
        Always send multipart/form-data. If audio_path is provided, send it as 'audio_file'. Otherwise, send audio_url as a form field.
        """
        url = f"{self.base_url}/VoiceChanger"
        headers = {
            "Authorization": self.api_key
            }
        files = {}
        data = {
            "voice_id": voice_id,
            "remove_background": 1 if remove_background else 0,
            "pitch": pitch
        }
        if webhook_url:
            data["webhook_url"] = webhook_url
        if audio_path:
            files["audio_file"] = open(audio_path, "rb")
        elif audio_url:
            data["audio_url"] = audio_url
        try:
            response = requests.post(url, headers=headers, files=files if files else None, data=data)
            if files:
                files["audio_file"].close()
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Endpoint not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or not all(k in data for k in ("success", "message", "task_id", "eta")):
                raise MusicGPTAPIError("Unexpected response format from API.")
            return ConversionResponse(**data, conversion_type=MusicGPTConversionType.VOICE_CHANGER)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")
        
    def cover(
            self, 
            voice_id: str,
            audio_url: str,
            pitch: int = 0,
            webhook_url: Optional[str] = None
    ) -> ConversionResponse:
        """
        Create a cover song using a specific voice. 
        Args:
            audio_url (str): The URL of the audio file to cover.
            voice_id (str): The ID of the voice to use for conversion.
            pitch (int, optional): The pitch adjustment for the audio.
            webhook_url (str, optional): Webhook URL for receiving notifications.
        Returns:
            ConversionResponse: The response from the API.
        Raises:
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        audio_path = None
        if is_local_filepath(audio_url):
            if not os.path.exists(audio_url):
                raise ValueError(f"Local file {audio_url} does not exist.")
            audio_path = audio_url
        return self._cover_request(
            audio_path=audio_path,
            audio_url=audio_url,
            voice_id=voice_id,
            pitch=pitch,
            webhook_url=webhook_url
        )
    def _cover_request(
        self,
        voice_id: str,
        audio_path: Optional[str] = None,
        audio_url: Optional[str] = None,
        pitch: int = 0,
        webhook_url: Optional[str] = None
    ) -> ConversionResponse:
        """
        Create a cover song using a specific voice.
        Always send multipart/form-data. If audio_path is provided, send it as 'audio_file'. Otherwise, send audio_url as a form field.
        """
        url = f"{self.base_url}/Cover"
        headers = {
            "Authorization": self.api_key
        }
        files = {}
        data = {
            "voice_id": voice_id,
            "pitch": pitch
        }
        if webhook_url:
            data["webhook_url"] = webhook_url
        if audio_path:
            files["audio_file"] = open(audio_path, "rb")
        elif audio_url:
            data["audio_url"] = audio_url
        try:
            response = requests.post(url, headers=headers, files=files if files else None, data=data)
            if files:
                files["audio_file"].close()
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Endpoint not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or not all(k in data for k in ("success", "message", "task_id", "eta")):
                raise MusicGPTAPIError("Unexpected response format from API.")
            return ConversionResponse(**data, conversion_type=MusicGPTConversionType.COVER)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")
        
    def text_to_speech(
            self, 
            text: str,
            voice_id: str = None, 
            gender: str = None,
            language: str = "en",
            webhook_url: Optional[str] = None
    ) -> ConversionResponse:
        """
        Convert text to speech using a specific voice.
        Args:
            text (str): The text to convert to speech.
            voice_id (str, optional): The ID of the voice to use for conversion.
            gender(str, optional): (m/f based on output gender)
            language (str, optional): The language code for the text.
            webhook_url (str, optional): Webhook URL for receiving notifications.
        Returns:
            ConversionResponse: The response from the API.
        Raises:
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        text_to_speech_request = TextToSpeechRequest(
            text=text,
            voice_id=voice_id,
            gender=gender, 
            language=language,
            webhook_url=webhook_url
        )
        return self._text_to_speech_request(text_to_speech_request)
    def _text_to_speech_request(
        self,
        request: TextToSpeechRequest
    ) -> ConversionResponse:
        """
        Convert text to speech using a specific voice.
        Args:
            request (TextToSpeechRequest): The request body for text-to-speech conversion.
        Returns:
            ConversionResponse: The response from the API.
        Raises:
            MusicGPTAuthError, MusicGPTNotFoundError, MusicGPTRateLimitError, MusicGPTAPIError
        """
        url = f"{self.base_url}/TextToSpeech"
        headers = {
            "Authorization": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, json=request.model_dump(exclude_none=True))
            if response.status_code == 401:
                raise MusicGPTAuthError("Invalid or missing API key.")
            if response.status_code == 404:
                raise MusicGPTNotFoundError("Endpoint not found.")
            if response.status_code == 429:
                raise MusicGPTRateLimitError("Rate limit exceeded.")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or not all(k in data for k in ("success", "message", "task_id", "eta")):
                raise MusicGPTAPIError("Unexpected response format from API.")
            return ConversionResponse(**data, conversion_type=MusicGPTConversionType.TEXT_TO_SPEECH)
        except ValueError as e:
            raise MusicGPTAPIError(f"Invalid response format: {e}")
        except Exception as e:
            raise MusicGPTAPIError(f"Unexpected error: {e}")
        except requests.RequestException as e:
            raise MusicGPTAPIError(f"API request failed: {e}")
        


    def wait_for_completion(
        self,
        task_id: str,
        conversion_type: MusicGPTConversionType,
        poll_interval: float = 3.0,
        timeout: float = 300.0,
        verbose: int = 0
    ) -> GetConversionResponse:
        """
        Polls the get_conversion endpoint until the conversion status is COMPLETED, ERROR, or FAILED.
        Args:
            task_id (str): The unique identifier for the task.
            conversion_type (MusicGPTConversionType): The type of conversion.
            poll_interval (float): Seconds to wait between polls (default: 3).
            timeout (float): Maximum seconds to wait before giving up (default: 300).
            verbose (int): 0 = log start/end, 1 = log every 30s, 2 = log every request.
        Returns:
            GetConversionResponse: The final response from the API.
        Raises:
            TimeoutError: If the operation times out.
            MusicGPTAPIError and subclasses for API errors.
        """
        import time
        start_time = time.time()
        last_print = start_time
        if verbose >= 0:
            self.logger.info(f"Polling for completion of task {task_id} (type: {conversion_type.value})...")
        time.sleep(poll_interval)  # Initial wait before the first poll
        while True:
            resp = self.get_conversion(conversion_type=conversion_type, task_id=task_id)
            status = resp.conversion.get("status")
            now = time.time()
            if verbose == 2:
                self.logger.info(f"[{int(now - start_time)}s] Status: {status}")
            elif verbose == 1 and now - last_print >= 30:
                self.logger.info(f"[{int(now - start_time)}s] Status: {status}")
                last_print = now
            if status in {ResponseStatus.COMPLETED, ResponseStatus.ERROR, ResponseStatus.FAILED}:
                if verbose >= 0:
                    self.logger.info(f"Task {task_id} finished with status: {status}")
                return resp
            if now - start_time > timeout:
                self.logger.error(f"Timeout waiting for completion of task {task_id}")
                raise TimeoutError(f"Timeout waiting for completion of task {task_id}")
            time.sleep(poll_interval)

