# REAL-TIME EDGE TTS
This is an implementation of Real-Time EDGE TTS that utilizes its streamed audio output.

## Install Dependencies
This script uses  __pyaudio__, __pydub__ and ofcourse __edge-tts__
```
pip install pyaudio pydub edge_tts
```

## Quick Start
Just put the script file to the same directory of your project so you can use it as module.
```
import realtime_edge-tts as rtet
import asyncio

TEXT = "Hello, World! This is a sample text."
asyncio.run(rtet.tts_stream(TEXT))
```

## FROM ME
When searching for TTS, i found __edge-tts__ to be the best free TTS. But along all the REAL-TIME TTS implementations, EDGE-TTS are aways being left away due to its nature in design. I wish this script would be helpful to everyone who will want to use the STREAMING CAPABILITIES of __edge-tts__ module.  

### TO-DO-LIST:
 - remove the choppiness (LISTED DATE: 2024-11-15)
