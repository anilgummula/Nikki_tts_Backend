# 🎙️ N.I.K.K.I TTS Studio - Backend

FastAPI backend for **N.I.K.K.I (Neural Intelligent Knowledge & Interaction Interface)** Text-to-Speech Studio.

Generate high-quality speech audio using Microsoft's Neural Voices through Edge-TTS.

---

## ✨ Features

* 🎤 Text-to-Speech generation
* 🌍 Multiple languages and accents
* 🇮🇳 Indian voices (Hindi, Telugu, Tamil, Kannada, English)
* 🇺🇸 American voices
* 🇬🇧 British voices
* 🎚️ Adjustable Rate, Pitch, and Volume
* 📁 Automatic MP3 generation
* 🔗 Direct audio download URLs
* 📚 Swagger API Documentation
* ⚡ FastAPI-powered high-performance backend

---

## 🛠️ Tech Stack

* Python 3.12+
* FastAPI
* Edge-TTS
* Uvicorn
* Pydantic

---

## 📂 Project Structure

backend/

├── main.py

├── requirements.txt

├── tts_output/

└── README.md

---

## 🚀 Installation

Clone the repository:

```bash
git clone <repo-url>
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## 📡 API Endpoints

### Get Voices

```http
GET /voices
```

Returns available voice catalog.

---

### Generate Speech

```http
POST /generate
```

Request:

```json
{
  "text": "Hello world",
  "voice_id": "en-IN-NeerjaNeural",
  "rate": "+0%",
  "pitch": "+0Hz",
  "volume": "+0%"
}
```

Response:

```json
{
  "filename": "nikki_20260625_205733.mp3",
  "audio_url": "/audio/nikki_20260625_205733.mp3",
  "duration_hint": "~5s",
  "characters": 123
}
```

---

## 🌐 Deployment

Backend is designed to be deployed on:

* Render
* Railway
* VPS
* Docker

Recommended production setup:

```text
https://api.yourdomain.com
```

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built as part of the N.I.K.K.I AI ecosystem.
