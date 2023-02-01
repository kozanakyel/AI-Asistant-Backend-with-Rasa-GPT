import io

def mp3_to_bytearray(file):
    with io.open(file, "rb") as f:
        return bytearray(f.read())

mp3_file = "audios/ChatGPTizG.mp3"
byte_array = mp3_to_bytearray(mp3_file)
print(byte_array)