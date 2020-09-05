#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import os
import time
import logging
import pjsua as pj

from threading import Thread
from .Exceptions import *
from .CallHandler import CallHandler
from .AccountHandler import AccountHandler


logger = logging.getLogger(__name__)
logging.addLevelName(5, "TRACE")

class Softphone:

    ua_cfg = pj.UAConfig()
    log_cfg = pj.LogConfig()
    log_cfg.callback = lambda level, str, len: logger.info(str.strip())
    media_cfg = pj.MediaConfig() # look at the options it takes: https://www.pjsip.org/python/pjsua.htm#MediaConfig

    def __init__(
            self, 
            max_calls=1, # TODO: Add support for multiple simultaneous calls.
            nameserver=['1.1.1.1'], 
            user_agent='Python Softphone', 
            log_level=5,
            sample_rate=48000, 
            duration_ms=20,
            channel_count=2,
            max_media_ports=8,
            thread=True
        ):
        """
        :param max_calls: Integer - Maximum simultaneous calls.
        :param nameserver: List - A list of DNS server(s) to use.
        :param user_agent: String - User-agent.
        :param log_level: Integer - Level to use for the logger.
        :sample_rate: Integer - Sample rate (hz) to capture and playback audio.
        :duration_ms: Integer - Milliseconds per audio frame.
        :channel_count: Integer - Number of channels to use. 1 for Mono, 2 for Stereo.
        :max_media_ports: Integer - PJSIP maximum media ports.
        :thread: Boolean - Use a threaded instance of softphone.
        """

        self.pid = os.getpid()

        # Media config
        self.media_cfg.clock_rate    = sample_rate
        self.media_cfg.channel_count = channel_count 

        #self.media_cfg.snd_clock_rate = sample_rate# Clock rate to be applied when opening the sound device. If value is zero, conference bridge clock rate will be used.
        self.media_cfg.audio_frame_ptime = duration_ms # Default: 20 ms audio data
        #self.media_cfg.no_vad = True # disable voice activation detection
        #self.media_cfg.enable_ice = False
        self.media_cfg.max_media_ports = max_media_ports

        # User-agent config
        self.ua_cfg.max_calls = max_calls
        self.ua_cfg.nameserver = nameserver
        self.ua_cfg.user_agent = user_agent

        # Log config
        self.log_cfg.level = log_level

        # Lib settings (put this in run() instead when using multiprocessing.Process)
        self.lib = pj.Lib() # Singleton instance
        self.lib.init(ua_cfg=self.ua_cfg, log_cfg=self.log_cfg, media_cfg=self.media_cfg)
        self.lib.start(with_thread=thread)

        # Playback / Recording varaibles
        self.player = None
        self.recorder = None

        # Stream callback id and slot
        self.audio_cb_id   = None
        self.audio_cb_slot = None

        # Call variables
        self.call_handler = True
        self.current_call = None
        
        logger.info(f"Object created.")


    def __del__(self):
        self.lib.destroy()
        logger.info(f"Object destroyed.")


    def register(self, server, port, username, password, default_account=False, proxy=None, protocol='UDP', bind_address='127.0.0.1', bind_port=0):
        """ Register an account at i.e. Asterisk PBX, and set network transport options.
            Returns: Account registered, account callback handler.
        """
        if   protocol == 'UDP': protocol = pj.TransportType.UDP
        elif protocol == 'TCP': protocol = pj.TransportType.TCP
        elif protocol == 'TLS': protocol = pj.TransportType.TLS
        else: logger.info(f"Error: Invalid protocol type.")

        logger.info("Creating transport and generating SIP URI.")
        transport = self.lib.create_transport(
            protocol,
            pj.TransportConfig(0) # TransportConfig(host=bind_address, port=bind_port) # TODO: Add bind_address and bind_port here.
        )

        public_sip_uri = f"sip:{username}@{str(transport.info().host)}:{str(transport.info().port)}"
        logger.info(f"Listening on {transport.info().host}:{transport.info().port} for {public_sip_uri}.")
        logger.info(f"Attempting registration for {public_sip_uri} at {server}:{port}.")

        account_cfg = pj.AccountConfig(
            domain   = server + ":" + port,
            username = username,
            password = password
        )

        account_cfg.id = public_sip_uri

        account = self.lib.create_account(acc_config=account_cfg, set_default=default_account)
        account.set_transport(transport)

        account_handler = AccountHandler(lib=self.lib, account=account)
        account.set_callback(account_handler)

        logger.info(f"Waiting for registration...")
        account_handler.wait()
        logger.info(f"Successfully registered {public_sip_uri}, status: {account.info().reg_status} ({account.info().reg_reason}).")

        return account


    def unregister(self, account):
        """ Unregister a registered account.
        """
        logger.info(f"Attempting to unregister account by deletion: {account}.")
        account.delete()
        logger.info(f"Successfully unregistered and deleted account.")


    def call(self, account, sip_uri):
        """ Make a new outgoing call to sip_uri from SIP account.
        """
        try:
            if self.current_call:
                logger.info(f"Already have a call.")
                return

            if self.lib.verify_sip_url(sip_uri) != 0:
                logger.info(f"Invalid SIP URI.")
                return

            logger.info(f"Attempting new call to {sip_uri}")
            lck = self.lib.auto_lock() # To prevent deadlocks

            call_handler = CallHandler(
                lib = self.lib, 
                audio_cb_slot = self.audio_cb_slot
            )
            self.current_call = account.make_call(sip_uri, cb=call_handler)
            logger.info(f"Current call is {self.current_call}.")
            del lck

        except pj.Error as e:
            logger.info(f"Error: {e}")
            self.current_call = None
            self.lib.destroy()


    def end_call(self):
        """ Hang up an ongoing call for SIP account.
        """
        try:
            if not self.current_call:
                logger.info("There is no call.")
                return
            
            if not self.current_call.is_valid(): # Is this needed? Used by g-farrow, but might be handled already.
                logger.info("Call has already ended.")
                return

            self.current_call.hangup()
            self.current_call = None
            logger.info(f"Call ended.")                

        except pj.Error as e:
            logger.info(f"Error: {e}")


    def wait_for_active_audio(self):
        """ Wait until call audio is activated.
        """
        while self.current_call.info().media_state != pj.MediaState.ACTIVE:
            time.sleep(0.5)


    def wait_for_confirmed_call(self):
        """ Wait until call has been confirmed.
        """
        while self.current_call.info().state != pj.CallState.CONFIRMED:
            time.sleep(0.5)


    def get_call_length(self):
        """ Get the length of the current call in seconds. 
        :return call_length, total_length: Tuple (Call Connection length (seconds), Total Length (seconds))
        """
        if not self.current_call:
            raise PhoneCallNotInProgress("The call does not exist")
        
        call_length = self.current_call.info().call_time
        total_length = self.current_call.info().total_time
        logger.info("Call duration information: connection '{call_length}' second(s), total '{total_length}' second(s).")

        return call_length, total_length


    def send_dtmf_key_tones(self, digits):
        """ Send DTMF keypad tones to the call.
        :param digits: String - Digits to send over the call
        """
        logger.debug("Sending DTMF key tones: '{digits}'")
        self.current_call.dial_dtmf(digits)
        logger.debug("DTMF tones sent")


    def get_sound_devices(self):
        """ Get a detailed list of available sound devices.
            Returns a list of available sound devices.
        """
        sounddevices = []

        snd_devs = self.lib.enum_snd_dev()

        i = 0
        for snd_dev in snd_devs:
            dev = {}
            dev['index'] = i
            dev['name'] = snd_dev.name
            dev['input_channels'] = snd_dev.input_channels
            dev['output_channels'] = snd_dev.output_channels
            dev['sample_rate'] = snd_dev.default_clock_rate
            sounddevices.append(dev)
            i+=1

        return sounddevices


    def set_null_sound_device(self):
        """ Set NULL sound device / Do not use system audio device.
        """
        self.lib.set_null_snd_dev()
        logger.info(f"Using NULL sound device.")


    def get_capture_device(self):
        """ Get capture device ID currently in use.
        """
        capture_id, playback_id = self.lib.get_snd_dev()
        return capture_id


    def set_capture_device(self, capture_id):
        """ Set capture device ID to be used.
        """
        _, playback_id = self.lib.get_snd_dev()
        self.lib.set_snd_dev(capture_id, playback_id)
        logger.info(f"Capture device set to: {capture_id}")


    def get_playback_device(self):
        """ Get playback device ID currently in use.
        """
        capture_id, playback_id = self.lib.get_snd_dev()
        return playback_id


    def set_playback_device(self, playback_id):
        """ Set playback device ID to be used.
        """
        capture_id, _ = self.lib.get_snd_dev()
        self.lib.set_snd_dev(capture_id, playback_id)
        logger.info(f"Playback device set to: {playback_id}")


    def capture(self, file_name):
        """ Save call audio to WAV file.
        """
        if os.path.exists(file_name):
            raise FileExistsError("A file with this name already exists: {file_name}")

        self.recorder = self.lib.create_recorder(file_name)
        recorder_slot = self.lib.recorder_get_slot(self.recorder)
        #self.lib.conf_connect(recorder_slot, self.current_call.info().conf_slot) # not needed? or?
        self.lib.conf_connect(self.current_call.info().conf_slot, recorder_slot)
        logger.info(f"Started audio capture.")


    def stop_capturing(self):
        """ Stop capturing call audio to file
        """
        recorder_slot = self.lib.recorder_get_slot(self.recorder)
        self.lib.conf_disconnect(self.current_call.info().conf_slot, recorder_slot)
        self.lib.recorder_destroy(self.recorder)
        self.recorder = None
        logger.info(f"Stopped audio capture.")


    def playback(self, file_name):
        """ Playback a WAV file into call.
        :param file_path: String - path to the audio (WAV) file to be played to the call.
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError("Cannot find audio file: {file_name}")

        if not os.path.isfile(file_name):
            raise FileNotFoundError("The audio file is not a file: {file_path}")

        self.player = self.lib.create_player(file_name)
        player_slot = self.lib.player_get_slot(self.player)
        self.lib.conf_connect(player_slot, self.current_call.info().conf_slot)
        logger.info(f"Started audio playback.")


    def stop_playback(self):
        """ Stop playing audio file to call
        """
        player_slot = self.lib.player_get_slot(self.player)
        self.lib.conf_disconnect(player_slot, self.current_call.info().conf_slot)
        self.lib.player_destroy(self.player)
        self.player = None
        logger.info(f"Stopped audio playback.")


    def create_audio_stream(self, audio_callback):
        self.audio_cb_id   = self.lib.create_audio_cb(audio_callback)
        self.audio_cb_slot = self.lib.audio_cb_get_slot(self.audio_cb_id)
        logger.info(f"Created audio callback.")


    def destroy_audio_stream(self):
        self.lib.audio_cb_destroy(self.audio_cb_id)
        self.audio_cb_id = None
        self.audio_cb_slot = None
        logger.info(f"Destroyed audio callback.")
