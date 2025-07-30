import websocket  # Use the same websocket library as the original
import threading
import json
import base64
import queue
import pyaudio
import sys
import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

class HumeClient:
    """Client for Hume API that mirrors the original perfect implementation"""
    
    def __init__(
        self,
        api_url: str = "wss://hume-8cac.onrender.com",  # For connecting to our API proxy
        access_token: str = None,
        config_id: str = "449da3e0-521e-44ea-b086-099eba6410de",
        enable_audio: bool = True,
        instructions: str = ""
    ):
        self.api_url = api_url
        self.access_token = access_token
        self.config_id = config_id
        self.enable_audio = enable_audio
        self.instructions = instructions
        
        # Audio settings - exactly as original
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 24000  # Hume audio is usually 24 kHz
    
    @dataclass
    class Response:
        """Response from Hume API"""
        output_text: str
    
    def chat(self, prompt: str) -> List[str]:
        """Have a chat with Hume and return all responses"""
        responses = []
        self._run_chat(prompt, responses)
        return responses
    
    def _run_chat(self, prompt: str, responses: List[str]):
        """Run the chat using the exact same approach as the original working code"""
        # Queue for audio data
        audio_queue = queue.Queue()
        # Event to sync input and output
        input_ready = threading.Event()
        input_ready.set()
        # Reference to websocket for closure
        ws_ref = {}
        
        # Build WebSocket URL
        if self.api_url.startswith("wss://hume-"):
            # Connect to our proxy server
            ws_url = f"{self.api_url}/chat/stream?access_token={self.access_token}&config_id={self.config_id}"
            if self.instructions:
                ws_url += f"&instructions={self.instructions}"
        else:
            # Direct connection to Hume (like original code)
            ws_url = (
                f"wss://api.hume.ai/v0/evi/chat?"
                f"fernSdkLanguage=Python&fernSdkVersion=0.8.9"
                f"&accessToken={self.access_token}"
                f"&config_id={self.config_id}"
                f"&verbose_transcription=true"
            )
        
        # Audio playback function - EXACTLY as original
        def play_audio_stream(audio_queue):
            p = pyaudio.PyAudio()
            stream = None
            while True:
                audio_data = audio_queue.get()
                if audio_data is None:  # Signal to stop
                    break
                if not audio_data:
                    continue
                pcm_data = audio_data[44:]  # skip 44-byte WAV header
                if stream is None:
                    stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True)
                stream.write(pcm_data)
            
            # Clean up
            if stream:
                stream.stop_stream()
                stream.close()
            p.terminate()
        
        # WebSocket callbacks - similar to original but adapted for our use case
        def on_message(ws, message):
            try:
                # Try to parse as JSON; if fails, treat as raw audio
                if isinstance(message, str):
                    try:
                        msg = json.loads(message)
                        if msg.get("type") == "audio_output":
                            audio_data = base64.b64decode(msg["data"])
                            if self.enable_audio:
                                audio_queue.put(audio_data)
                        elif msg.get("type") == "assistant_message":
                            response_text = msg['message']['content']
                            responses.append(response_text)
                            print(f"\n[Assistant]: {response_text}\n")
                        elif msg.get("type") == "user_message":
                            print(f"[You]: {msg['message']['content']}")
                        else:
                            pass
                    except Exception:
                        # Not JSON, treat as text response
                        responses.append(message)
                        print(f"\n[Assistant]: {message}\n")
                elif isinstance(message, bytes) and self.enable_audio:
                    audio_queue.put(message)
            except Exception as e:
                print(f"Message error: {e}")
        
        def on_error(ws, error):
            print(f"[WebSocket Error]: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print("[WebSocket closed]")
            # Signal audio thread to stop
            if self.enable_audio:
                audio_queue.put(None)
        
        def on_open(ws):
            print("[WebSocket connected]")
            
            # If connecting directly to Hume API, send instructions
            if self.instructions and not self.api_url.startswith("wss://hume-"):
                ws.send(json.dumps({
                    "type": "session_settings",
                    "instructions": self.instructions
                }))
            
            # Send the prompt
            try:
                ws.send(prompt if self.api_url.startswith("wss://hume-") else 
                       json.dumps({"type": "user_input", "text": prompt}))
                print(f"[You]: {prompt}")
            except Exception as e:
                print(f"[Send Error]: {e}")
        
        # Create and start WebSocket
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws_ref['ws'] = ws
        
        # Start audio thread if audio enabled
        if self.enable_audio:
            audio_thread = threading.Thread(target=play_audio_stream, args=(audio_queue,), daemon=True)
            audio_thread.start()
        
        # Run the WebSocket in the current thread until closed
        ws.run_forever(ping_interval=30, ping_timeout=10)
    
    def generate(self, prompt: str) -> str:
        """Generate a response from Hume and return the text"""
        responses = self.chat(prompt)
        return responses[0] if responses else ""
    
    def responses_create(self, model: Optional[str] = None, input: str = "") -> Response:
        """OpenAI-like interface for generating responses"""
        text = self.generate(input)
        return self.Response(output_text=text)
