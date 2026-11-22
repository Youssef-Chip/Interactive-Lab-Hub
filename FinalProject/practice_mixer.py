import json
import os
import subprocess
import time
from pathlib import Path

import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from adafruit_seesaw import seesaw, rotaryio, digitalio as seesaw_dio
import qwiic_joystick

MANIFEST_PATH = Path("songs_manifest.json")
SPEED_STEPS = [100, 95, 90, 85]


class AudioPlayer:
    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.current_key: tuple | None = None

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None
        self.current_key = None

    def sync(
        self,
        is_playing: bool,
        wav_path: str | None,
        volume: int,
        start: float,
        end: float | None,
    ):
        if not is_playing or not wav_path or not os.path.exists(wav_path):
            self.stop()
            return

        key = (
            wav_path,
            volume,
            round(start, 3),
            round(end, 3) if end is not None else None,
        )
        if key == self.current_key and self.proc and self.proc.poll() is None:
            return

        self.stop()
        cmd = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel", "quiet",
            "-volume", str(max(0, min(100, volume))),
            "-ss", f"{max(0.0, start):.2f}",
        ]
        # Looping is default while playing
        if end is not None and end > start:
            cmd += ["-t", f"{(end - start):.2f}"]
        cmd += ["-loop", "0", wav_path]

        self.proc = subprocess.Popen(cmd)
        self.current_key = key


def init_hardware():
    i2c = busio.I2C(board.SCL, board.SDA)

    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.fill(0)
    oled.show()
    font = ImageFont.load_default()

    ss = seesaw.Seesaw(i2c, addr=0x36)
    encoder = rotaryio.IncrementalEncoder(ss)
    enc_btn = seesaw_dio.DigitalIO(ss, 24)
    enc_btn.switch_to_input(pull=digitalio.Pull.UP)

    joy = qwiic_joystick.QwiicJoystick()
    if not joy.is_connected():
        raise RuntimeError("Qwiic Joystick not detected on I2C")
    joy.begin()

    return oled, font, encoder, enc_btn, joy


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def draw_marquee_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    max_width: int,
    font: ImageFont.ImageFont,
    now: float,
):
    w = text_width(draw, text, font)
    if w <= max_width:
        draw.text((0, y), text, font=font, fill=255)
        return

    overflow = w - max_width
    speed_px_per_sec = 22.0
    pause_sec = 1.0
    travel_time = overflow / speed_px_per_sec
    cycle = 2 * pause_sec + 2 * travel_time
    t = now % cycle

    if t < pause_sec:
        offset = 0.0
    elif t < pause_sec + travel_time:
        offset = (t - pause_sec) * speed_px_per_sec
    elif t < 2 * pause_sec + travel_time:
        offset = float(overflow)
    else:
        offset = max(0.0, overflow - (t - 2 * pause_sec - travel_time) * speed_px_per_sec)

    draw.text((-int(round(offset)), y), text, font=font, fill=255)


def draw_oled(
    oled,
    font,
    now: float,
    song_title: str,
    cp_name: str,
    is_playing: bool,
    speed_pct: int,
    vol: int,
):
    img = Image.new("1", (128, 32))
    draw = ImageDraw.Draw(img)

    state_tag = "LOOP" if is_playing else "PAUS"
    status_line = f"{state_tag}: {cp_name}"

    draw_marquee_line(draw, song_title, y=0, max_width=128, font=font, now=now)
    draw_marquee_line(draw, status_line, y=11, max_width=128, font=font, now=now)
    draw.text((0, 22), f"SPD:{speed_pct}%  VOL:{vol}%", font=font, fill=255)

    oled.image(img)
    oled.show()


def main():
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError("Run preprocess_tracks.py first to generate songs_manifest.json")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    songs = manifest.get("songs", [])
    if not songs:
        raise RuntimeError("No songs found in songs_manifest.json")

    oled, font, encoder, enc_btn, joy = init_hardware()
    player = AudioPlayer()

    song_idx = 0
    last_enc_pos = encoder.position
    last_enc_btn = False
    last_joy_btn = False
    last_speed_move = 0.0
    last_vol_move = 0.0

    song = songs[song_idx]
    cp_idx = 0
    is_playing = False
    default_spd = int(round(song.get("default_speed", 1.0) * 100))
    speed_pct = default_spd if default_spd in SPEED_STEPS else SPEED_STEPS[0]
    volume = 75

    try:
        while True:
            now = time.monotonic()
            song = songs[song_idx]
            checkpoints = song.get("checkpoints", [{"name": "Full", "start": 0.0, "end": None}])
            cp_idx = max(0, min(cp_idx, len(checkpoints) - 1))
            cp = checkpoints[cp_idx]
            start_sec = float(cp.get("start", 0.0))
            end_raw = cp.get("end", None)
            end_sec = float(end_raw) if end_raw is not None else None

            # 1. Encoder Rotation: Select Checkpoint (never changes play/pause state)
            enc_pos = encoder.position
            if enc_pos != last_enc_pos:
                delta = enc_pos - last_enc_pos
                cp_idx = (cp_idx + delta) % len(checkpoints)
                cp = checkpoints[cp_idx]
                start_sec = float(cp.get("start", 0.0))
                end_raw = cp.get("end", None)
                end_sec = float(end_raw) if end_raw is not None else None
                last_enc_pos = enc_pos
                if is_playing:
                    player.stop()

            # 2. Encoder Click: Toggle Play / Pause (cues back to start of current checkpoint)
            enc_pressed = not enc_btn.value
            if enc_pressed and not last_enc_btn:
                is_playing = not is_playing
                player.stop()  # Always resets/starts cleanly from start_sec
            last_enc_btn = enc_pressed

            # 3. Joystick: Speed (X), Volume (Y), Next Song (Click)
            x_val = joy.horizontal
            y_val = joy.vertical
            joy_btn_pressed = (joy.button == 0)

            if joy_btn_pressed and not last_joy_btn:
                song_idx = (song_idx + 1) % len(songs)
                song = songs[song_idx]
                cp_idx = 0
                is_playing = False
                player.stop()
                default_spd = int(round(song.get("default_speed", 1.0) * 100))
                speed_pct = default_spd if default_spd in SPEED_STEPS else SPEED_STEPS[0]
                time.sleep(0.2)
            last_joy_btn = joy_btn_pressed

            if now - last_speed_move > 0.28:
                s_i = SPEED_STEPS.index(speed_pct)
                if x_val < 300 and s_i > 0:
                    speed_pct = SPEED_STEPS[s_i - 1]
                    last_speed_move = now
                    if is_playing:
                        player.stop()
                elif x_val > 700 and s_i < len(SPEED_STEPS) - 1:
                    speed_pct = SPEED_STEPS[s_i + 1]
                    last_speed_move = now
                    if is_playing:
                        player.stop()

            if now - last_vol_move > 0.12:
                if y_val > 700:
                    volume = min(100, volume + 5)
                    last_vol_move = now
                elif y_val < 300:
                    volume = max(0, volume - 5)
                    last_vol_move = now

            # 4. OLED & Audio Sync
            cp_display_name = cp.get("name", "Section")
            draw_oled(
                oled,
                font,
                now,
                song.get("title", "Untitled"),
                cp_display_name,
                is_playing,
                speed_pct,
                volume,
            )

            wav_path = song.get("rendered_files", {}).get(str(speed_pct))
            player.sync(is_playing, wav_path, volume, start_sec, end_sec)

            time.sleep(0.03)

    except KeyboardInterrupt:
        pass
    finally:
        player.stop()
        oled.fill(0)
        oled.show()


if __name__ == "__main__":
    main()