# livetranscriber

A zero-dependency **single-file** helper that streams microphone audio to Deepgram for real-time speech-to-text. This is available as a package on PyPI.

## Features

*   **Simple API** - single `LiveTranscriber` class.
*   **Configurable** - every Deepgram *LiveOptions* parameter can be overridden via keyword arguments; sensible Nova-3 defaults are provided.
*   **Mandatory callback** - forces the calling code to supply a function that will be invoked for every *final* transcript chunk (empty / interim chunks are ignored).
*   **Output capture** - optional `output_path` writes each final transcript line to disk.
*   **Pause / resume** - you may call `pause` or `resume` from your callback.
*   **Graceful shutdown** - Ctrl-C or `stop` shuts everything down and releases resources.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install livetranscriber
```

Alternatively, if you are working with the source code or a specific requirements file, you can install the dependencies listed in `requirements.txt`:

```
deepgram-sdk>=4,<5
numpy>=1.24  # build-time requirement of sounddevice
sounddevice>=0.4
```

Install with `uv` (preferred) or plain `pip`:

```bash
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt
```
or
```bash
pip install -r requirements.txt
```

2.  **Python Version:**

    Python 3.11 is required.

## Environment Setup

Export your Deepgram API key (see https://console.deepgram.com):

```bash
export DEEPGRAM_API_KEY="dg_…"
```

## Example Usage

```python
from livetranscriber import LiveTranscriber

def on_text(text: str):
    print("NEW>", text)

tr = LiveTranscriber(callback=on_text, model="nova-3-general", language="en-US")
tr.run()  # blocks until you press Ctrl-C
```

## API

### `LiveTranscriber` Class

High-level wrapper around Deepgram live transcription.

**Parameters:**

*   `callback`: A function that will be invoked for every final transcript. Must accept a single `str` argument. May be sync or async.
*   `output_path` (Optional): Path to a text file that will receive each final transcript line (UTF-8).
*   `api_key` (Optional): Your Deepgram API key. If omitted, the `DEEPGRAM_API_KEY` environment variable is used; failing both raises `RuntimeError`.
*   `keepalive` (Optional): If `True` (default) the WebSocket client sends keepalive pings.
*   `**live_options_overrides` (Optional): Any keyword argument that matches a *LiveOptions* field overrides the built-in defaults. For example, `punctuate=False`.

**Methods:**

*   `run()`: Run until `.stop()` or Ctrl-C.
*   `stop()`: Public request to shut down; may be called from any thread.
*   `pause()`: Pause writing transcripts to `output_path` (callback still runs).
*   `resume()`: Resume writing transcripts to `output_path`.

## Dependencies

*   `deepgram-sdk`
*   `numpy`
*   `sounddevice`
