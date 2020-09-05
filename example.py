#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# Built with pjproject (fork py37) - https://github.com/DiscordPhone/pjproject/tree/py37

import sys
import logging
from os import environ as env
from time import sleep
from dotenv import load_dotenv
from softphone.Softphone import Softphone
from softphone.AudioCallbacks import EchoAudioCB, SystemAudioCB

load_dotenv(dotenv_path='.env')

logging.basicConfig(
    filename='example.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

softphone = Softphone()
softphone.set_null_sound_device()
#inbound = self.softphone.register(...) # Registration of account for incoming calls
outbound = softphone.register(
    server   = env.get('SIP_OUTBOUND_HOST'),
    port     = env.get('SIP_OUTBOUND_PORT'),
    username = env.get('SIP_OUTBOUND_USER'),
    password = env.get('SIP_OUTBOUND_PASS')
)

# There are some cases when you need this, read the documentation for it. It is used when having python threads.
# softphone.lib.thread_register("python worker")

print("Softphone is now ready...")

while True:
    sleep(2) # Just wait for the call state messages for a bit.. :)
    print("")
    print("+-Menu-------------+")
    print("| m  = make call   |")
    print("| h  = hangup call |")
    print("| a  = answer call |")
    print("| q  = quit        |")
    print("+------------------+")
    choice = input("> ")

    if choice == 'm':
        number = input("Number with country code 00x (ex: 0014446665555)> ")
        sip_uri = f"sip:{number}@{env.get('SIP_OUTBOUND_HOST')}:{env.get('SIP_OUTBOUND_PORT')}"

        # TODO: Check if instantiating audio_buffer without self. gives less lag.
        audio_buffer = EchoAudioCB() # Alternatively an AudioCB with two buffers if relaying between two systems.
        softphone.create_audio_stream(audio_buffer) # Move this inside call maybe?
        softphone.call(outbound, sip_uri)
        #softphone.wait_for_active_audio() # Wait for active audio before we listen. Use this if you are using threads. Blocking operation.

        # If two systems, connect them below. 
        #system2.listen(audio_buffer)
        #system2.play(audio_buffer)

    if choice == 'a':
        # TODO: Must be implemented.
        pass

    if choice == 'h':
        softphone.end_call()
        softphone.destroy_audio_stream()

    if choice == 'q':
        print('Exiting...')
        #softphone.unregister(inbound)
        softphone.unregister(outbound)
        sys.exit()

#end