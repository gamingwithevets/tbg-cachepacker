import sys
import os
import traceback
import binascii
import msvcrt
import math
import decimal
import ntpath
from datetime import datetime

def clear():
	if os.name == 'nt':
		 _ = os.system('cls')
	else:
		_ = os.system('clear')

def mkdir_and_open():
	if not os.path.exists('cachepacker_packed/' + os.path.dirname(exportdir)):
		os.makedirs('cachepacker_packed/' + os.path.dirname(exportdir), exist_ok = True)
	return open('cachepacker_packed/' + exportdir, 'ab')

def draw_screen(draw_pack = True, draw_status = True):
	clear()
	print('CACHEPACKER for The Beginner\'s Guide v1.0.0 - by GamingWithEvets\n')
	if draw_pack:
		print('---------------------------------------------------------\nPacking your files...\n---------------------------------------------------------')
		if draw_status:
			print('\nPacked {0}/{1} file(s) - {2}%\n\nSTATUS:'.format(packed, numfiles, round(packed / numfiles * 100)))
			if packed != numfiles:
				print('Packing {0} - {1} ({2} bytes)...'.format(filename, convert_size(filedatalen), filedatalen))
			else:
				print('Done!')

def get_filelist(directory):
	filelist = os.listdir(directory)
	allfiles = []
	for entry in filelist:
		fullpath = os.path.join(directory, entry)
		if os.path.isdir(fullpath):
			allfiles = allfiles + get_filelist(fullpath)
		else:
			if os.name == 'nt':
				allfiles.append(fullpath.removeprefix(currdir + '\\'))
			else:
				allfiles.append(fullpath.removeprefix(currdir + '/'))
	return allfiles

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0 bytes"
	size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p)

	if i != 0:
		digits = 0
		while(s > 0):
			digits += 1
			s //= 10
		if digits == 1:
			s = round(size_bytes / p, 2)
			if str(s).endswith('.0') or str(s).endswith('.1') or str(s).endswith('.2') or str(s).endswith('.3') or str(s).endswith('.4') or str(s).endswith('.5') or str(s).endswith('.6') or str(s).endswith('.7') or str(s).endswith('.8') or str(s).endswith('.9'):
				return "%s0 %s" % (s, size_name[i])
		elif digits == 2:
			s = round(size_bytes / p, 1)
		elif digits == 3:
			s = round(size_bytes / p)

	return "%s %s" % (s, size_name[i])

def newexportdir(old_dir, set_dir = False):
	newexport = ''
	typedonce = False
	success = False
	while not success:
		draw_screen(False)
		if not typedonce:
			if not set_dir:
				if args.newexport:
					print('Directory {0} exists in cachepacker_packed/.'.format(exportdir))
				print('Please specify a new export filename: ', end = '')
			else:
				print('File {0} also exists in cachepacker_packed/.\nPlease type another export filename: '.format(exportdir), end = '')
		else:
			print('You cannot leave the export filename blank or type the old export filename.\nPlease type another export filename: ', end = '')
		newexport = input()
		if not newexport or newexport == old_dir:
			if not typedonce:
				typedonce = True
		else:
			draw_screen(False)
			print('New export filename: {0}\n\nIs this correct? [Y/N] '.format(newexport), end = '')
			final_choice = msvcrt.getche()
			draw_screen(False)
			if not final_choice.lower() == b'n':
				success = True
				return newexport
			else:
				newexport = ''
				typedonce = False

def pack(numfiles, folder, file, keys, set_global = False):
	if set_global:
		global packed
		global filename
		global filedatalen
	cache = mkdir_and_open()
	if packed == 0:
		cache.write(numfiles.to_bytes(4, 'little'))
	cache.write(len(folder + file).to_bytes(4, 'little'))
	cache.write(binascii.a2b_qp(folder + file))
	curr_file = open(keys + '/' + folder + file, 'rb')
	curr_file_data = curr_file.read()
	filename = folder + file
	filedatalen = len(curr_file_data)
	cache.write((filedatalen).to_bytes(4, 'little'))
	cache.write(curr_file_data)
	packed += 1

def exit_man():
	if args.autoexit:
		exit()
	else:
		print("\nPress Enter twice to exit.")
		input()
		print('Press Enter again to exit!')
		input()
		clear()
		exit()


import argparse
parser = argparse.ArgumentParser(description = 'Packs the contents of one or more folders into a file cache that is compatible with The Beginner\'s Guide.', epilog = '(c) 2022 GamingWithEvets Inc. All rights reserved.', formatter_class=argparse.RawTextHelpFormatter, allow_abbrev = False)
parser.add_argument('filecache_path', nargs = '+', help = 'path to the directory(ies) you want to pack into the file cache')
parser.add_argument('-e', '--export', metavar = 'FILENAME', default = 'filecache.bin', help = 'export filename')
parser.add_argument('-d', '--disablelog', action = 'store_true', help = 'disable logging')
parser.add_argument('-o', '--overwrite', action = 'store_true', help = 'suppresses the export directory overwrite prompt')
parser.add_argument('-n', '--newexport', action = 'store_true', help = 'prompts you to enter a new export directory name if the old one is taken')
parser.add_argument('-p', '--packcont', action = 'store_true', help = 'suppresses prompting to confirm that you want to pack only the folder contents')
parser.add_argument('-a', '--autoexit', action = 'store_true', help = 'the program exits automatically')
args = parser.parse_args()
if args.overwrite and args.newexport:
	parser.error('cannot combine -o/--overwrite with -n/--newexport')
if args.export[1:].startswith(':'):
		parser.error('cannot use file paths with drive letters')

for dirr in args.filecache_path:
	if not os.path.exists(dirr) or not os.path.isdir(dirr):
		parser.error('path {0} doesn\'t exist or is not a directory'.format(dirr))
	elif dirr[1:].startswith(':'):
		parser.error('cannot use file paths with drive letters')

try:
	clear()
	draw_screen(False)

	dirs = args.filecache_path
	exportdir = args.export

	exportdircheck = False
	set_dir = False
	old_export = exportdir
	while not exportdircheck:
		if os.path.exists('cachepacker_packed/' + exportdir):
			if args.newexport:
				exportdir = newexportdir(exportdir, set_dir)
				if not set_dir:
					set_dir = True
			elif args.overwrite:
				os.remove('cachepacker_packed/' + exportdir)
				exportdircheck = True
			else:
				print('File "{0}" in cachepacker_packed/ exists! Do you want to change the export filename?\n[Y: Yes (Default) / N: No] '.format(exportdir), end = '')
				newexport_choice = msvcrt.getche()
				if not newexport_choice.lower() == b'n':
					exportdir = newexportdir(exportdir)
				else:
					os.remove('cachepacker_packed/' + exportdir)
					exportdircheck = True
		else:
			exportdircheck = True

	if len(dirs) == 1:
		if args.packcont:
			packcont_choice = b''
		else:
			clear()
			draw_screen(False)
			print('You\'ve only selected 1 folder! Would you like to only pack the folder contents?\n[Y: Yes (Default) / N: No] ', end = '')
			packcont_choice = msvcrt.getche()
	else:
		packcont_choice = b'n'

	files = {}
	packed = 0
	numfiles = 0

	for directory in dirs:
		currdir = directory
		if packcont_choice.lower() == b'n':
			folder = ntpath.basename(currdir)
		else:
			folder = ''
		files[directory] = get_filelist(directory)
		numfiles += len(files[directory])

	for keys in files:
		for file in files[keys]:
			if packed == 0:
				pack(numfiles, folder, file, keys, True)
			else:
				draw_screen()
				pack(numfiles, folder, file, keys)
			draw_screen()
	print('\nPacking done. You can find the file cache in cachepacker_packed/{0}'.format(exportdir), end='')
	exit_man()

except KeyboardInterrupt:
	print("\nScript exited with a KeyboardInterrupt!\n")
	print(traceback.format_exc())
	print("noice")
	exit()
except Exception:
	print("\nMy my! An error occured!\n")
	print(traceback.format_exc())
	print("If possible, please report it to https://github.com/gamingwithevets/tbg-cacheripper/issues")
	exit_man()