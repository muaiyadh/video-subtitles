from datetime import datetime
import os
import re
import logging

def shift_timestamp(timestamp, seconds_to_shift):
	"""
	Shift a timestamp by a given amount of seconds
	:param timestamp: Timestamp to shift
	:param seconds_to_shift: Amount to shift in seconds
	:return: Shifted timestamp
	"""
	timestamp = timestamp.strip()
	# timestamp format: 00:07:35,000    (%H:%M:%S,%MM) where MM is milliseconds
	timestamp_to_sec = datetime.strptime(timestamp, '%H:%M:%S,%f')
	# convert to seconds
	timestamp_to_sec = timestamp_to_sec.second + timestamp_to_sec.minute*60 + timestamp_to_sec.hour*3600
	# shift
	shifted = timestamp_to_sec + seconds_to_shift
	# convert back to timestamp
	shifted_timestamp = datetime.utcfromtimestamp(shifted).strftime('%H:%M:%S')+timestamp[timestamp.rindex(','):]
	return shifted_timestamp


def main(input_file, output_file, shift_amount, logger):
	"""
	Shift subtitles by a given amount of seconds
	:param input_file: Input file
	:param output_file: Output file
	:param shift_amount: Amount to shift in seconds
	:return: None
	"""
	logger.info("Input file: {}".format(input_file))
	logger.info("Output file: {}".format(output_file))
	logger.info("Shift amount: {} seconds".format(shift_amount))
	logger.info("Starting...")

	# expand user path
	input_file = os.path.expanduser(input_file)
	output_file = os.path.expanduser(output_file)

	# check files properly
	if not os.path.isfile(input_file):
		logger.error("Input file does not exist!")
		exit()
	elif not input_file.endswith(".srt"):
		logger.error("Input file is not an .srt file!")
		exit()
	if os.path.isfile(output_file):
		logger.error("Output file already exists!")
		exit()

	with open(input_file, "r") as input_srt:
		with open(output_file, "w+") as output_srt:
			for line in input_srt:
				# check if timestamp line
				if re.match(r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d", line):
					line = line.split(" --> ")
					line[0] = shift_timestamp(line[0], shift_amount)
					line[1] = shift_timestamp(line[1], shift_amount)
					line = " --> ".join(line) + "\n"
				output_srt.write(line)
	logger.info("Done!")

if __name__=="__main__":
	# parse args
	import argparse
	parser = argparse.ArgumentParser(description="Shift subtitles by a given amount of seconds")
	parser.add_argument("--input_file", "-i", help="Input file", required=True)
	parser.add_argument("--output_file", "-o", help="Output file", required=True)
	parser.add_argument("--shift_amount", "-s", help="Amount to shift in seconds", type=int, required=True)
	args = parser.parse_args()
	
	# init logger stuff
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	# run main
	main(args.input_file, args.output_file, args.shift_amount, logger)
