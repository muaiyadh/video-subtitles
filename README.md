# Whisper subtitles
A couple of helper scripts to generate a .srt file for a given .wav file input.

Uses OpenAI's Whisper and the [faster-whisper](https://github.com/guillaumekln/faster-whisper) implementation.

## Main script
### Usage
1. Install the necessary dependencies.
1. Ensure you have a valid .wav audio file for transcription.
1. Run the script with the desired command-line options and provide the path to the input audio file.
1. The script will transcribe the audio and generate a corresponding .srt subtitle file.
### Example

`python main_faster_whisper.py --input audio.wav --language en --remove-silence`

This will start transcribing the file `audio.wav` while assuming it's in English. Additionally, it will remove silent portions from the audio file longer than 2 seconds, which helps to get a better transcription. The resulting transcription will be written to `audio.srt`.

To get more info, refer to the script's `--help` option:

`python main_faster_whisper.py --help`

## Subtitles shifter
A tool to easily shift timestamps of an .srt file!

The script takes an input file (input_file) which should be an .srt file containing the subtitles you want to shift. The shifted subtitles will be written to the output file (output_file). The shift_amount argument specifies the amount of seconds by which the subtitles should be shifted.

### Example

`python subtitles_shift.py --input_file input.srt --output_file output.srt --shift_amount 5`

This will write to the file `output.srt` where all the timestamps from `input.srt` will be shifted by 5 seconds.
