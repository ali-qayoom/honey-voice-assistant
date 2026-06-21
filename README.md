# honey-voice-assistant
# Honey - Automated Python Voice Assistant with Cloud API Integration

A high-performance, localized Python voice assistant named **Honey** that integrates cloud-based language models for fast, intelligent responses and utilizes natural-sounding text-to-speech rendering. This project demonstrates modular software engineering patterns, local runtime command routing, and asynchronous processing loop design.

## Core Technology Stack
* **Language:** Python
* **LLM Orchestration:** Groq Cloud API (`llama-3.1-8b-instant`)
* **Speech Recognition:** Google Speech Recognition API via `speech_recognition`
* **Text-to-Speech Engine:** `edge-tts` (Microsoft Azure Cognitive Communication framework)
* **Audio Engineering:** `sounddevice` & `numpy` for handling low-level live microphone byte arrays

## Logic Architecture & Features
* **Wake-Word Processing:** Operates a continuous, low-overhead listening loop looking for a specific audio interrupt keyword ("hello") in short 1.5-second capture windows.
* **Localized Command Routing:** Features an instantaneous static command handling system to open frequently used applications natively (Google, YouTube, WhatsApp, Typing Master, and custom music playlists via `ML.py`) without incurring latency from cloud processing.
* **Dynamic AI Overflow:** Leverages cloud-based NLP inference via the Groq API to securely handle complex, unstructured conversational commands when local matching blocks are bypassed.
* **Asynchronous Voice Generation:** Implements Python's `asyncio` loop handling to generate and process high-fidelity voice profiles natively without blocking or stalling the main system execution thread.

