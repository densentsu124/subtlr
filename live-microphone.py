import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import google_api as ga
import gpt_api_tagalog as gt

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
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, device=2):
        print("Recording audio... Press Ctrl+C to stop.")
        while True:
            try:
                sd.sleep(100)
                if silent_frames >= sample_rate * segment_duration:
                    break
            except KeyboardInterrupt:
                break
    return

def save_audio_segment(segment):
    filename = f"ay_lmao.wav"
    wavfile.write(filename, 44100, segment)
    transcript = ga.transcribe("ay_lmao.wav")
    print("Transcript: {}".format(gt.translate(transcript)))

def float2pcm(sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)

record_audio()

