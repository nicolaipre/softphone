#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# coding=utf-8

import pjsua as pj
import logging

logger = logging.getLogger(__name__)
logging.addLevelName(5, "TRACE")

class CallHandler(pj.CallCallback):
    """ Class to handle callback events from a call. Handles everything that happens within the call.
    """

    def __init__(self, lib, call=None, audio_cb_slot=None):
        pj.CallCallback.__init__(self, call)
        self.lib = lib
        # self.call = call # TODO: Look at this.. pj.CallCallback has this thing set... Is it needed here?
        self.audio_cb_slot = audio_cb_slot


    def on_state(self):
        """ Notifies when a call state has changed.
        """
        if self.call.info().state == pj.CallState.CONNECTING:
            logger.info("Call is connecting.")

        elif self.call.info().state == pj.CallState.CONFIRMED:
            logger.info("Receiver answered the outgoing call.")

        elif self.call.info().state == pj.CallState.DISCONNECTED:
            logger.info("Call disconnected.")

        #else:
        logger.info(f"Call with {self.call.info().remote_uri} is {self.call.info().state_text}. Last code: {self.call.info().last_code} ({self.call.info().last_reason}).")


    def on_media_state(self):
        """ Notifies when a calls media state has changed.
        """
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            
            # TODO: No point connecting these if using null_snd_dev, but no audio if we dont?? Cant remember..
            self.lib.conf_connect(0, self.call.info().conf_slot)
            self.lib.conf_connect(self.call.info().conf_slot, 0)
            
            # If we are also streaming audio, connect that...
            if self.audio_cb_slot != None:
                self.lib.conf_connect(self.call.info().conf_slot, self.audio_cb_slot)
                self.lib.conf_connect(self.audio_cb_slot, self.call.info().conf_slot)
            
            logger.info("Media is now active.")
        else:
            logger.info("Media is inactive.")


    # TODO: Add call transfers
    #def on_transfer_status(self, code, reason, final, cont):
    #def on_transfer_request(self, dst, code):

    # TODO: Add some cool DTMF dial codes here that we can use
    def on_dtmf_digit(self, digits):
        logger.info(f"Got DTMF digits: {digits}.")
        pass
        """
        if digits == '#':
            self.wait_for_hash = False
            logging.info("Collected DTMF: %s" % self.collection)
        if self.wait_for_hash:
            self.collection += digits
            return
        if digits == '7':
            self.play_file("../audio/default.wav", enforce_playback=True)
            self.wait_for_hash = True
            self.action = "newcall"
        """