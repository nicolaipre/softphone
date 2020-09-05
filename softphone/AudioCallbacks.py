#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import logging
import sounddevice as sd
from collections import deque

logger = logging.getLogger(__name__)

class EchoAudioCB:
    """ Echo phone audio (input -> output).
    """
    def __init__(self, duration_ms=20, sample_rate=48000.0, channel_count=2):
        self.duration_ms = duration_ms
        self.sample_rate = sample_rate
        self.channel_count = channel_count
        self.sample_period_sec = 1.0/self.sample_rate
        self.samples_per_frame = int((duration_ms/1000.0) / self.sample_period_sec)
        self.audio_buffer = deque()


    def cb_put_frame(self, frame): # WRITE
        """ Listen to the audio coming from phone, and write to audio_buffer.
        """
        self.audio_buffer.append(frame)

        # Return an integer; 0 means success, but this does not matter now
        return 0


    def cb_get_frame(self, size): # READ
        """ Read from audio_buffer, and send audio to phone speaker.
        """
        if len(self.audio_buffer):
            frame = self.audio_buffer.popleft()
            return frame
        else:
            return None


class SystemAudioCB:
    """ Relay system audio using buffers.
    """
    def __init__(self, duration_ms=20, sample_rate=48000.0, channel_count=2):
        self.duration_ms = duration_ms
        self.sample_rate = sample_rate
        self.channel_count = channel_count
        self.sample_period_sec = 1.0/self.sample_rate
        self.samples_per_frame = int((duration_ms/1000.0) / self.sample_period_sec)
        self.input_stream = sd.RawInputStream(samplerate=self.sample_rate, channels=channel_count, dtype='int16', blocksize=self.samples_per_frame)
        self.output_stream = sd.RawOutputStream(samplerate=self.sample_rate, channels=channel_count, dtype='int16', blocksize=self.samples_per_frame)
        self.input_stream.start()
        self.output_stream.start()


    def cb_put_frame(self, frame): # WRITE
        """ Listen to the audio coming from phone, and write to output_stream.
        """
        self.output_stream.write(frame)

        # Return an integer; 0 means success, but this does not matter now
        return 0


    def cb_get_frame(self, size): # READ
        """ Read from input_stream, and send audio to phone speaker.
        """
        ret = self.input_stream.read(self.samples_per_frame)
        raw_samples = bytes(ret[0])
        return raw_samples
