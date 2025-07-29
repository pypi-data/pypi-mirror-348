# musicgpt

A Python wrapper for the musicgpt public api endpoints.

## Installation

```sh
pip install musicgpt
```

## Usage

```python
from musicgpt import MusicGPTClient

client = MusicGPTClient("api_key_here")
conv= client.music_ai(prompt = "create song about generating music using ai")
result = client.wait_for_completion(task_id = conv.task_id, conversion_type = conv.conversion_type)
print(result)
```

## Development

- Install dev dependencies:
  ```sh
  pip install -r dev-requirements.txt
  ```
- Run tests:
  ```sh
  pytest
  ```
