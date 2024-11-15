#!/usr/bin/env python3

"""
Advanced audio streaming example with real-time playback and prebuffering.

This example shows how to stream the audio data from the TTS engine
and play it in real-time while saving to a file. It properly handles
MP3 decoding and implements prebuffering for smoother playback.
"""

import asyncio
import io
import pyaudio
import pydub
import edge_tts
from collections import deque

class AudioPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.buffer = io.BytesIO()
        self.prebuffer = deque()
        self.prebuffer_size = 2048
        self.is_prebuffering = True
        
    def initialize_stream(self, sample_rate=24000, channels=1):
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            output=True
        )
    
    def play_chunk(self, mp3_chunk):
        # Append the MP3 chunk to our buffer
        self.buffer.write(mp3_chunk)
        
        # If we're still prebuffering
        if self.is_prebuffering:
            total_buffered = self.buffer.tell()
            if total_buffered >= self.prebuffer_size:
                print(f"Prebuffer filled ({total_buffered} bytes). Starting playback...")
                self.is_prebuffering = False
            else:
                print(f"Prebuffering... {total_buffered}/{self.prebuffer_size} bytes")
                return
        
        # If we have accumulated enough data, convert and play it
        if self.buffer.tell() > 2048:  # Process in larger chunks for efficiency
            # Convert MP3 data to WAV
            self.buffer.seek(0)
            try:
                audio_segment = pydub.AudioSegment.from_mp3(self.buffer)
                
                # Convert to raw audio data
                raw_audio = audio_segment.raw_data
                
                # Play the audio
                if self.stream and raw_audio:
                    self.stream.write(raw_audio)
            except Exception as e:
                print(f"Error processing audio chunk: {e}")
            
            # Clear the buffer and prepare for new data
            self.buffer = io.BytesIO()
    
    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

async def tts_stream(text, voice = "en-GB-SoniaNeural") -> None:
    """Main function"""

    OUTPUT_FILE = "test.mp3"
    PREBUFFER_SIZE = 4096  # Size of prebuffer in bytes

    print("Starting text-to-speech streaming...")
    print(f"Prebuffering {PREBUFFER_SIZE} bytes before playback...")
    
    # Create player with default audio settings
    player = AudioPlayer()
    player.initialize_stream(sample_rate=24000, channels=1)  # Standard audio settings
    player.prebuffer_size = PREBUFFER_SIZE
    
    try:
        communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%", pitch="+0Hz")
        with open(OUTPUT_FILE, "wb") as file:
            print("Speaking:")
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    # Write to file
                    file.write(chunk["data"])
                    # Play the audio chunk
                    player.play_chunk(chunk["data"])

                # for WORD BOUNDARY
                # elif chunk["type"] == "WordBoundary":
                #     # Only print word boundaries after prebuffering is complete
                #     if not player.is_prebuffering:
                #         print(f"{chunk['text']} ", end="", flush=True)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        player.cleanup()
        print("Streaming completed!")

# TEST 
if __name__ == "__main__":

    TEXT = """
    Welcome to this demonstration of real-time text-to-speech streaming. 
    This is a longer sample text that will help us better understand how the streaming works.
    We can talk about interesting topics like science, technology, or nature.
    For example, did you know that honeybees can recognize human faces? 
    They use the same techniques as humans, building up a pattern from smaller pieces of the face.
    This kind of pattern recognition is fascinating and shows how complex even small brains can be.
    """
    
    asyncio.run(tts_stream(TEXT))
