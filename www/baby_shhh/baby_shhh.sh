#!/bin/bash

# 0. Get the audio codec
ffmpeg -i baby_shhh.MOV

# 1. Extract the audio
ffmpeg -i baby_shhh.MOV -f mp3 -ab 192000 -vn baby_shhh1.mp3

# 2. Create a text file that contains this filename repeated 60 times
for i in {1..60}; do echo "file 'baby_shhh1.mp3'" >> baby_shhh.txt; done

# 3. Loop the audio clip 60 times
ffmpeg -t 3600.0 -f concat -i baby_shhh.txt -c copy -t 3600.0 baby_shhh2.mp3

# 4. Make it louder
ffmpeg -i baby_shhh2.mp3 -filter:a "volume=3.0" baby_shhh.mp3
