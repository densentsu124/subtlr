import sys
from random import choice, randrange
from string import ascii_letters

import pygame as pg

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import google_api as ga
import gpt_api_tagalog as gt


transcript_data = ""
screen = pg.display.set_mode((1280, 720))


def random_letters(n):
    """Pick n random letters."""
    return ''.join(choice(ascii_letters) for _ in range(n))


def main():
    info = pg.display.Info()
    # screen = pg.display.set_mode((1280, 720))
    # screen_rect = screen.get_rect()
    # font = pg.font.Font(None, 45)
    clock = pg.time.Clock()
    # color = (randrange(256), randrange(256), randrange(256))
    # txt = font.render(random_letters(randrange(5, 21)), True, color)
    timer = 10
    done = False

    record_audio()

    # while not done:
    #     for event in pg.event.get():
    #         if event.type == pg.KEYDOWN:
    #             if event.key == pg.K_ESCAPE:
    #                 done = True

    #     timer -= 1
    #     # Update the text surface and color every 10 frames.
    #     if timer <= 0:
    #         timer = 10
    #         color = (255, 255, 255)
    #         # color = (randrange(256), randrange(256), randrange(256))
    #         txt = font.render(random_letters(randrange(5, 21)), True, color)

    #     # screen.fill((30, 30, 30)
    #     screen.fill((0, 255, 0))
    #     screen.blit(txt, txt.get_rect(center=screen_rect.center))

    #     pg.display.flip()
    #     clock.tick(30)

def record_audio(segment_duration=1.0, silence_threshold=60):
    # Configure audio recording parameters
    sample_rate = 44100  # Sample rate (Hz)

    # Initialize variables
    segment = np.array([], dtype=np.float32)
    silent_duration = 40
    silent_frames = 0
    state = 0
    def audio_callback(indata, frames, time, status):
        nonlocal segment, silent_frames, state

        volume_norm = np.linalg.norm(indata)*10
        # print("volume: {0} || silent_frames: {1}".format(int(volume_norm), silent_frames))
        # print(rms)

        if volume_norm < silence_threshold:
            silent_frames += 1
            if state == 0:
                segment = np.array([], dtype=np.float32)
        else:
            silent_frames = 0
            state = 1

        # Append the current audio segment to the list if it contains enough samples
        segment = np.concatenate([segment, indata[:, 0]])
        if silent_frames >= silent_duration and state == 1:
            segment = float2pcm(segment)
            save_audio_segment(segment)
            # print("Segment Saved")
            state = 0
            segment = np.array([], dtype=np.float32)

    # Start audio recording
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, device=1):
        print("Recording audio... Press Ctrl+C to stop.")
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit(0)
            try:
                # sd.sleep(100)
                if silent_frames >= sample_rate * segment_duration:
                    break
            except KeyboardInterrupt:
                break
    return

def save_audio_segment(segment):
    global transcript_data


    try:
        filename = f"D:\\subtlr\\ay_lmao.wav"
        wavfile.write(filename, 44100, segment)
        transcript = ga.transcribe("D:\\subtlr\\ay_lmao.wav")
        transcript_data = gt.translate(transcript)
    except:
        transcript_data = "None"
    finally:
        print("Transcript: {}".format(transcript_data))
        screen.fill((0, 255, 0))
        font = pg.font.Font(None, 64)
        color = (255, 255, 255)
        txt = font.render(transcript_data, True, color)

        screen.blit(txt, txt.get_rect(center=screen_rect.center))
        pg.display.flip()


def float2pcm(sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)



if __name__ == '__main__':
    pg.init()
    info = pg.display.Info()
    # screen = pg.display.set_mode((1280, 720))
    screen_rect = screen.get_rect()
    screen.fill((0, 255, 0))
    main()
    pg.quit()
    sys.exit()