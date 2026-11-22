import json
import os
import subprocess
from pathlib import Path

RAW_DIR = Path("raw_tracks")
OUT_DIR = Path("processed_tracks")
MANIFEST_PATH = Path("songs_manifest.json")

# Speeds to pre-render (1.0 = 100% normal speed)
SPEEDS = [1.0, 0.95, 0.90, 0.85]


def build_atempo_filter(speed: float) -> str:
    """
    ffmpeg's atempo filter accepts values between 0.5 and 2.0 per stage.
    Chain stages if ever needed outside [0.5, 2.0].
    """
    if speed <= 0:
        raise ValueError("Speed must be positive")
    filters = []
    remaining = speed
    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5
    while remaining > 2.0:
        filters.append("atempo=2.0")
        remaining /= 2.0
    filters.append(f"atempo={remaining:.4f}")
    return ",".join(filters)


def render_speed_variant(src_file: Path, dst_file: Path, speed: float) -> None:
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(src_file),
        "-vn",
        "-af", build_atempo_filter(speed),
        "-ar", "48000",
        "-ac", "2",
        "-c:a", "pcm_s16le",
        str(dst_file),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def load_or_init_manifest(audio_files: list[Path]) -> dict:
    if MANIFEST_PATH.exists():
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    else:
        data = {"songs": []}

    existing_ids = {s["id"] for s in data["songs"]}

    for f in audio_files:
        song_id = f.stem
        if song_id not in existing_ids:
            # Customize checkpoints per song in songs_manifest.json after generation
            data["songs"].append({
                "id": song_id,
                "title": song_id.replace("_", " ").title(),
                "source": str(f),
                "default_speed": 1.0,
                "checkpoints": [
                    {"name": "Full Track", "start": 0.0, "end": None},
                    {"name": "Section A", "start": 0.0, "end": 15.0},
                    {"name": "Section B", "start": 15.0, "end": 30.0},
                ],
            })

    MANIFEST_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def main() -> None:
    RAW_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)

    exts = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
    audio_files = sorted([p for p in RAW_DIR.iterdir() if p.is_file() and p.suffix.lower() in exts])

    if not audio_files:
        print(f"No audio files found in '{RAW_DIR}/'. Add recordings and re-run.")
        return

    manifest = load_or_init_manifest(audio_files)

    for song in manifest["songs"]:
        src = Path(song["source"])
        if not src.exists():
            print(f"Skipping missing source: {src}")
            continue

        song_out_dir = OUT_DIR / song["id"]
        song["rendered_files"] = {}

        for spd in SPEEDS:
            pct = int(round(spd * 100))
            out_wav = song_out_dir / f"speed_{pct}.wav"
            print(f"Rendering {song['title']} @ {pct}% -> {out_wav}")
            render_speed_variant(src, out_wav, spd)
            song["rendered_files"][str(pct)] = str(out_wav)

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nDone. Please edit '{MANIFEST_PATH}' to customize per-song loop checkpoints.")


if __name__ == "__main__":
    main()