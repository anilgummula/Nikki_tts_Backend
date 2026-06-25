"""
╔══════════════════════════════════════╗
║      N.I.K.K.I — TTS Studio         ║
║        FastAPI Backend               ║
╚══════════════════════════════════════╝

Requirements:
    pip install fastapi uvicorn edge-tts python-multipart
"""
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import Request
import asyncio
import os
from datetime import datetime
from pathlib import Path

# ─── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(title="N.I.K.K.I TTS Studio API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_FOLDER = BASE_DIR / "tts_output"
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Serve generated audio files
# app.mount("/audio", StaticFiles(directory=str(OUTPUT_FOLDER)), name="audio")
app.mount(
    "/audio",
    StaticFiles(directory=OUTPUT_FOLDER),
    name="audio"
)

# ─── Voice catalogue ──────────────────────────────────────────────────────────
VOICES = [
    # Indian
    {"id": "en-IN-NeerjaNeural",   "name": "Neerja",   "lang": "English (India)",  "flag": "🇮🇳", "group": "Indian"},
    {"id": "hi-IN-SwaraNeural",    "name": "Swara",    "lang": "Hindi",             "flag": "🇮🇳", "group": "Indian"},
    {"id": "te-IN-ShrutiNeural",   "name": "Shruti",   "lang": "Telugu",            "flag": "🇮🇳", "group": "Indian"},
    {"id": "ta-IN-PallaviNeural",  "name": "Pallavi",  "lang": "Tamil",             "flag": "🇮🇳", "group": "Indian"},
    {"id": "kn-IN-SapnaNeural",    "name": "Sapna",    "lang": "Kannada",           "flag": "🇮🇳", "group": "Indian"},
    # American
    {"id": "en-US-AriaNeural",     "name": "Aria",     "lang": "English (US)",      "flag": "🇺🇸", "group": "American"},
    {"id": "en-US-JennyNeural",    "name": "Jenny",    "lang": "English (US)",      "flag": "🇺🇸", "group": "American"},
    {"id": "en-US-MichelleNeural", "name": "Michelle", "lang": "English (US)",      "flag": "🇺🇸", "group": "American"},
    {"id": "en-US-SaraNeural",     "name": "Sara",     "lang": "English (US)",      "flag": "🇺🇸", "group": "American"},
    # British
    {"id": "en-GB-SoniaNeural",    "name": "Sonia",    "lang": "English (UK)",      "flag": "🇬🇧", "group": "British"},
    {"id": "en-GB-LibbyNeural",    "name": "Libby",    "lang": "English (UK)",      "flag": "🇬🇧", "group": "British"},
    # Other
    {"id": "en-AU-NatashaNeural",  "name": "Natasha",  "lang": "English (AU)",      "flag": "🇦🇺", "group": "Other"},
    {"id": "en-CA-ClaraNeural",    "name": "Clara",    "lang": "English (CA)",      "flag": "🇨🇦", "group": "Other"},
    {"id": "de-DE-KatjaNeural",    "name": "Katja",    "lang": "German",            "flag": "🇩🇪", "group": "Other"},
    {"id": "fr-FR-DeniseNeural",   "name": "Denise",   "lang": "French",            "flag": "🇫🇷", "group": "Other"},
    {"id": "es-ES-ElviraNeural",   "name": "Elvira",   "lang": "Spanish",           "flag": "🇪🇸", "group": "Other"},
    {"id": "ja-JP-NanamiNeural",   "name": "Nanami",   "lang": "Japanese",          "flag": "🇯🇵", "group": "Other"},
    {"id": "ko-KR-SunHiNeural",    "name": "SunHi",    "lang": "Korean",            "flag": "🇰🇷", "group": "Other"},
    {"id": "zh-CN-XiaoxiaoNeural", "name": "Xiaoxiao", "lang": "Chinese (Mandarin)","flag": "🇨🇳", "group": "Other"},
    {"id": "ar-EG-SalmaNeural",    "name": "Salma",    "lang": "Arabic",            "flag": "🇪🇬", "group": "Other"},
]

# ─── Schemas ──────────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    text: str
    voice_id: str
    rate: str   = "+0%"   # e.g. "+20%" or "-10%"
    pitch: str  = "+0Hz"  # e.g. "+5Hz"  or "-10Hz"
    volume: str = "+0%"   # e.g. "+30%"  or "-20%"

class GenerateResponse(BaseModel):
    filename: str
    audio_url: str
    duration_hint: str   # rough estimate
    characters: int

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "N.I.K.K.I TTS Studio API is running 🎙️"}


@app.get("/voices")
def get_voices():
    """Return grouped voice catalogue."""
    groups: dict[str, list] = {}
    for v in VOICES:
        groups.setdefault(v["group"], []).append(v)
    return {"voices": VOICES, "groups": groups}


@app.post("/generate", response_model=GenerateResponse)
async def generate_tts(req: GenerateRequest, request: Request):
    """Generate TTS audio and return a URL to download it."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    # Validate voice id
    valid_ids = {v["id"] for v in VOICES}
    if req.voice_id not in valid_ids:
        raise HTTPException(status_code=400, detail=f"Unknown voice id: {req.voice_id}")

    filename  = f"nikki_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.mp3"
    out_path  = OUTPUT_FOLDER / filename

    try:
        communicate = edge_tts.Communicate(
            text=req.text,
            voice=req.voice_id,
            rate=req.rate,
            pitch=req.pitch,
            volume=req.volume,
        )
        await communicate.save(str(out_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

    # Rough duration estimate: ~150 wpm average
    word_count    = len(req.text.split())
    est_seconds   = max(1, round(word_count / 2.5))
    duration_hint = f"~{est_seconds}s"

    return GenerateResponse(
        filename=filename,
        audio_url = str(request.base_url) + f"audio/{filename}",
        duration_hint=duration_hint,
        characters=len(req.text),
    )


# @app.get("/audio/{filename}")
# def download_audio(filename: str):
#     """Direct download route (fallback if static mount is unavailable)."""
#     path = OUTPUT_FOLDER / filename
#     if not path.exists():
#         raise HTTPException(status_code=404, detail="File not found.")
#     return FileResponse(str(path), media_type="audio/mpeg", filename=filename)


@app.delete("/audio/{filename}")
def delete_audio(filename: str):
    """Optionally clean up a generated file."""
    path = OUTPUT_FOLDER / filename
    if path.exists():
        path.unlink()
        return {"deleted": filename}
    raise HTTPException(status_code=404, detail="File not found.")



@app.get("/debug")
def debug():
    return {
        "base_dir": str(BASE_DIR),
        "output_folder": str(OUTPUT_FOLDER),
        "exists": OUTPUT_FOLDER.exists(),
        "files": [f.name for f in OUTPUT_FOLDER.glob("*.mp3")]
    }