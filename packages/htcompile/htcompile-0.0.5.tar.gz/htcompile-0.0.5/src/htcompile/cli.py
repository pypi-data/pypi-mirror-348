
"""
HTCompile
	by KittKat
	https://kittkat.xyz

Designed to be an easy way to compile a website with import statements.

Ussage:
	htcompile ./source ./dest
		source is the source directory
		dest is the output directory
"""

import sys
import os
from .parser import Parser

def app():
	# List of CLI args
	args: list[str] = sys.argv[1:]

	# The source and destination directory
	srcDir = ""
	dstDir = ""

	# Loop through all params
	while len(args) > 0:
		a = args[0]
		args = args[1:]

		# Help flag
		if (a == '-h' or a == '--help'):
			print(__doc__)
			exit()
		# Others
		else:
			if len(srcDir) == 0:
				srcDir = a
			elif len(dstDir) == 0:
				dstDir = a
			else: 
				print("Extra param: " + a)
				exit()

	# If not enough params, exit
	if len(srcDir) == 0 or len(dstDir) == 0:
		print("Missing source directory and destination directory")
		exit()

	if not os.path.exists(srcDir):
		print("Source directory is not a valid path!")
		exit()

	if not os.path.exists(dstDir):
		print("Destination directory is not a valid path!")
		exit()

	def list_files_recursive(src: str, path: str) -> list[str]:
		print(src, path)
		files: list[str] = []
		for entry in os.listdir(os.path.join(src, path)):
			full_path: str = os.path.join(path, entry)
			if os.path.isdir(os.path.join(src, full_path)):
				files += list_files_recursive(src, full_path)
			else:
				files.append(full_path)
		return files



	srcFiles = list_files_recursive(srcDir, "./")

	fileStack: list[str] = []

	parser: Parser = Parser(srcDir, dstDir, srcFiles)

	debug = True

	try:
		parser.parse()
	except Exception as e:
		print(e)
		if debug:
			raise e

	 

