'''
A simple script to transcribe a .wav audio file and give a .srt output file.
Uses OpenAI's Whisper model and faster_whisper implementation.
'''

# For more color in the program's life
import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(color_scheme='Linux', call_pdb=False)


import os
import time
import logging
from pathlib import Path

from faster_whisper import WhisperModel


"""
Helper functions
"""

def sec_to_timestamp(sec):
    '''
        Converts seconds to the time format used in SRT files (i.e. 00:00:00,000)
    '''
    main_part = time.strftime('%H:%M:%S', time.gmtime(sec))
    ms_part = f"{(sec%1):.3f}"[2:]
    return f"{main_part},{ms_part}"

def segment_to_srt(line_number, segment):
    '''
        Takes the current line number and the transcription segment and returns the data properly formatted
        according to SRT file format:
        LINE_NUM
        START --> END
        Content
	
	
    '''
    lines = f"{line_number}\n{sec_to_timestamp(segment.start)} --> {sec_to_timestamp(segment.end)}\n{segment.text.strip()}\n\n"
    return lines


def write_segments_to_srt(segments, srt_path, logger):
    '''
        Takes the transcribed segments and output SRT file path and writes the segments data to the SRT file
    '''
    with open(srt_path, 'w') as srt_file:
        for idx, segment in enumerate(segments):
            lines = segment_to_srt(idx+1, segment)  # Add 1 to index to start count from 1
            # Print what's currently being written to SRT file if in debug mode, else print current segment number
            logger.info(f"Segment {idx+1}")
            logger.debug(lines)
            
            # Write to SRT file
            srt_file.write(lines)

def main(args, logger):
    ##  To download and convert the normal models to ct2 ones, use the following command
    #  $ ct2-transformers-converter --model openai/whisper-medium.en --output_dir whisper-medium.en-ct2 \
    #     --copy_files tokenizer.json --quantization float16
    
    device = args.device
    device_index = args.device_index
    compute_type= args.compute_type
    
    model_path = Path(args.model).expanduser().as_posix()
    input_file_path = Path(args.input).expanduser()
    output_srt_path = input_file_path.with_suffix('.srt')
    
    # Handle if SRT file already exists
    if os.path.exists(output_srt_path):
        if not args.ignore_if_exists:
            # If SRT file already exists, raise error to avoid overwriting data
            raise FileExistsError("The SRT file for this audio already exists. Try manually choosing the file name using --output or -o.")
        else:
            logger.info("The SRT file for this audio already exists. Exiting...")
            return
    
    # Load model
    logger.info("Loading model")
    model = WhisperModel(model_path, device=device, device_index=device_index, compute_type=compute_type)
    
    # Starts transcription
    logger.debug(type(input_file_path))
    logger.debug(input_file_path)
    logger.info(f"Starting transcription for file {input_file_path.stem}")
    segments, info = model.transcribe(input_file_path.as_posix(), beam_size=args.beam_size)
    
    # Write transcribed data to SRT file
    write_segments_to_srt(segments, output_srt_path, logger)


if __name__=="__main__":
    import argparse

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Transcribe audio file using Faster Whisper library.')
    
    # Add arguments
    parser.add_argument('--input', '-i', type=str, help='Path to input WAV audio file', required=True)
    parser.add_argument('--model', '-m', default="large-v2", type=str, help='Name of/Path to CT2 Whisper model')
    parser.add_argument('--output', '-o', type=str, help='Path to output SRT file. Uses the input file with SRT extension if not specified')
    parser.add_argument('--device', type=str, default="cuda", help='Device to use during transcription ("cuda" or "cpu")')
    parser.add_argument('--device_index', type=int, default=0, help='Device ID to use during transcription')
    parser.add_argument('--compute_type', type=str, default="auto", help='Compute type to use during transcription ("default", "auto", "int8", "int8_float16", "int16", "float16", "float32')
    parser.add_argument('--beam_size', type=int, default=5, help='Beam size to use for decoding')
    parser.add_argument('--ignore_if_exists', action='store_true', help='Exit program if SRT file for it or chosen output already exist')
    parser.add_argument('--debug', action='store_true', help='Enable debug (prints full SRT to terminal)')
    
    args = parser.parse_args()
    
    # init logger stuff
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger(__name__)
    
    main(args, logger)
