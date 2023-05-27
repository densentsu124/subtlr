import obspython as obs

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import google_api as ga
import gpt_api_tagalog as gt

interval = 1
source_name = ""
transcript_data = ""

def update_text():
    global interval
    global source_name
    global transcript

    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", transcript_data)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

def refresh_pressed(props, prop):
    print("refresh_pressed()")
    record_audio()

def script_description():
    return "Updates a text source"

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "interval", 5)
    obs.obs_data_set_default_string(settings, "source", "")

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "interval", "Update Interval (seconds)", 1, 3600, 1)

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props

def script_update(settings):
    global interval
    global source_name

    interval    = obs.obs_data_get_int(settings, "interval")
    source_name = obs.obs_data_get_string(settings, "source")

    obs.timer_remove(update_text)

    if source_name != "":
        obs.timer_add(update_text, interval * 1000)


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
            print("Segment Saved")
            state = 0
            segment = np.array([], dtype=np.float32)

    # Start audio recording
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, device=1):
        print("Recording audio... Press Ctrl+C to stop.")
        while True:
            try:
                sd.sleep(100)
                if silent_frames >= sample_rate * segment_duration:
                    break
            except KeyboardInterrupt:
                break
            except Exception:
                break
    return

def save_audio_segment(segment):
    global transcript_data
    try:
        filename = f"D:\\subtlr\\ay_lmao.wav"
        wavfile.write(filename, 44100, segment)
        transcript = ga.transcribe("D:\\subtlr\\ay_lmao.wav")
        transcript_data = gt.translate(transcript)
        print("Transcript: {}".format(transcript_data))
    except Exception:
        transcript_data = "Invalid"
    finally:
        pass

def float2pcm(sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)


