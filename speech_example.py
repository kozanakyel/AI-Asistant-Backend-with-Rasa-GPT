#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START import_libraries]
from __future__ import division

import re
import sys

from datetime import datetime
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
import socket
import thread

import subprocess as sp
from os import read, close, open, O_RDWR

# [END import_libraries]

# Audio recording parameters
RATE = 8000
CHUNK = int(RATE / 10)  # 100ms


def on_new_client(clientsocket, addr):
    language_code = 'en-US'  # a BCP-47 language tag

    # speech recognition code
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        single_utterance=True,
        interim_results=True)

    with Stream(RATE, CHUNK, clientsocket) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        print("First request time", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        responses = client.streaming_recognize(streaming_config, requests)
        # print("current time", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        # Now, put the transcription responses to use.
        listen_print_loop(responses, addr)



    close(clientsocket)


class Stream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk, tcpsocket):
        self._rate = rate
        self._chunk = chunk
        self._tcpsocket = tcpsocket

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""

        in_data = self._tcpsocket.recv(CHUNK)
        self._buff.put(in_data)
        # print('length of data ', len(in_data))
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                    # print('size of data ', len(data))
                except queue.Empty:
                    break

            yield b''.join(data)


# [END audio_stream]


def listen_print_loop(responses, address):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            print("current time", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            # print(address, ">>>>")
            # sys.stdout.write(transcript + overwrite_chars + '\r')
            # print("current time", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            sys.stdout.write(transcript + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            # print(address, ">>>>")
            # print(transcript + overwrite_chars)
            print(transcript)
            print("Last response time", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            break

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    # language_code = 'en-US'  # a BCP-47 language tag

    # next create a socket object
    s = socket.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 8080

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print('socket binded to %s' % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # Establish connection with client.
    # c, addr = s.accept()

    while True:
        c, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        thread.start_new_thread(on_new_client, (c, addr))
        # Note it's (addr,) not (addr) because second parameter is a tuple
        # Edit: (c,addr)
        # that's how you pass arguments to functions when creating new threads using thread module.
    # s.close()

if __name__ == '__main__':
    main()