# encoding: UTF-8
# Copyright 2017 Google.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import glob
import sys
import os
import math

import logging

# create logger
module_logger = logging.getLogger('myApp')


class DataTools:
	alphabetSize = 98

	def __init__(self):
		self.alphabetSize = 98
	
	# Specification of the supported alphabet (subset of ASCII-7)
	# 10 line feed LF
	# 32-64 numbers and punctuation
	# 65-90 upper-case letters
	# 91-97 more punctuation
	# 97-122 lower-case letters
	# 123-126 more punctuation
	# <> are now incoded as [] for text mark up in kivy
	def encodeChar(self, a):
		"""Encode a character
		:param a: one character
		:return: the encoded value
		"""
		if a == 60:
			return 61
		if a == 62:
			return 63			
		if a == 9:
			return 1
		if a == 10:
			return 127 - 30  # LF
		elif 32 <= a <= 126:
			return a - 30
		else:
			return 0  # unknown


	# encoded values:
	# unknown = 0
	# tab = 1
	# space = 2
	# all chars from 32 to 126 = c-30
	# LF mapped to 127-30
	def decodeChar(self, c, avoid_tab_and_lf=True):
		"""Decode a code point
		:param c: code point
		:param avoid_tab_and_lf: if True, tab and line feed characters are replaced by '\'
		:return: decoded character
		"""
		if c == 1:
			return 32 if avoid_tab_and_lf else 9  # space instead of TAB
		if c == 127 - 30:
			return 92 if avoid_tab_and_lf else 9  # space instead of LF
		if 32 <= c + 30 <= 126:
			return c + 30
		else:
			return 32  # unknown - changed to space over nul char as causing parse errors


	def encode_text(self, s):
		"""Encode a string.
		:param s: a text string
		:return: encoded list of code points
		"""
		#module_logger.info('encoding text')
		return list(map(lambda a: self.encodeChar(ord(a)), s))


	def decode_text(self, c, avoid_tab_and_lf=False):
		"""Decode an encoded string.
		:param c: encoded list of code points
		:param avoid_tab_and_lf: if True, tab and line feed characters are replaced by '\'
		:return:
		"""
		#module_logger.info('decoding text')
		return "".join(map(lambda a: chr(self.decodeChar(a, avoid_tab_and_lf)), c))


	def sample_from_probabilities(self, probabilities, topn=alphabetSize):
		"""Roll the dice to produce a random integer in the [0..alphabetSize] range,
		according to the provided probabilities. If topn is specified, only the
		topn highest probabilities are taken into account.
		:param probabilities: a list of size alphabetSize with individual probabilities
		:param topn: the number of highest probabilities to consider. Defaults to all of them.
		:return: a random integer
		"""
		p = np.squeeze(probabilities)
		p[np.argsort(p)[:-topn]] = 0
		p = p / np.sum(p)
		return np.random.choice(self.alphabetSize, 1, p=p)[0]

	def convert_bytes(self,size_bytes):
		if size_bytes == 0:
			return "0B"
		size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
		i = int(math.floor(math.log(size_bytes, 1024)))
		p = math.pow(1024, i)
		s = round(size_bytes / p, 2)
		return "%s %s" % (s, size_name[i])	
		
	
	def countNumberOfFiles(self, _path):
		numOfFiles = len([name for name in os.listdir(_path) if os.path.isfile(os.path.join(_path, name))])
		return numOfFiles
		
	def calcFileSizes(self, path='.'):
		total = 0
		for entry in os.scandir(path):
			if entry.is_file():
				total += entry.stat().st_size
			elif entry.is_dir():
				total += calcFileSizes(entry.path)
		return total
		
	def find_book(self, index, bookranges):
		return next(
			book["name"] for book in bookranges if (book["start"] <= index < book["end"]))


	def find_book_index(self, index, bookranges):
		return next(
			i for i, book in enumerate(bookranges) if (book["start"] <= index < book["end"]))

	def print_learning_learned_comparison(self, X, Y, losses, bookranges, batch_loss, batch_accuracy, epoch_size, index, epoch):
		"""Display utility for printing learning statistics"""
		module_logger.info('printing learning comparison')
		print()
		# epoch_size in number of batches
		batch_size = X.shape[0]  # batch_size in number of sequences
		sequence_len = X.shape[1]  # sequence_len in number of characters
		start_index_in_epoch = index % (epoch_size * batch_size * sequence_len)
		for k in range(batch_size):
			index_in_epoch = index % (epoch_size * batch_size * sequence_len)
			decx = self.decode_text(X[k], avoid_tab_and_lf=True)
			decy = self.decode_text(Y[k], avoid_tab_and_lf=True)
			bookname = self.find_book(index_in_epoch, bookranges)
			formatted_bookname = "{: <10.40}".format(bookname)  # min 10 and max 40 chars
			epoch_string = "{:4d}".format(index) + " (epoch {}) ".format(epoch)
			loss_string = "loss: {:.5f}".format(losses[k])
			print_string = epoch_string + formatted_bookname + " │ {} │ {} │ {}"
			print(print_string.format(decx, decy, loss_string))
			index += sequence_len
		# box formatting characters:
		# │ \u2502
		# ─ \u2500
		# └ \u2514
		# ┘ \u2518
		# ┴ \u2534
		# ┌ \u250C
		# ┐ \u2510
		format_string = "└{:─^" + str(len(epoch_string)) + "}"
		format_string += "{:─^" + str(len(formatted_bookname)) + "}"
		format_string += "┴{:─^" + str(len(decx) + 2) + "}"
		format_string += "┴{:─^" + str(len(decy) + 2) + "}"
		format_string += "┴{:─^" + str(len(loss_string)) + "}┘"
		footer = format_string.format('INDEX', 'BOOK NAME', 'TRAINING SEQUENCE', 'PREDICTED SEQUENCE', 'LOSS')
		print(footer)
		# print statistics
		batch_index = start_index_in_epoch // (batch_size * sequence_len)
		batch_string = "batch {}/{} in epoch {},".format(batch_index, epoch_size, epoch)
		stats = "{: <28} batch loss: {:.5f}, batch accuracy: {:.5f}".format(batch_string, batch_loss, batch_accuracy)
		print()
		print("TRAINING STATS: {}".format(stats))





	def read_data_files(self,directory, validation=True):
		"""Read data files according to the specified glob pattern
		Optionnaly set aside the last file as validation data.
		No validation data is returned if there are 5 files or less.
		:param directory: for example "data/*.txt"
		:param validation: if True (default), sets the last file aside as validation data
		:return: training data, validation data, list of loaded file names with ranges
		 If validation is
		"""
		module_logger.info('reading data files')
		codetext = []
		bookranges = []
		cardlist = glob.glob(directory, recursive=True)
		for cardfile in cardlist:
			cardtext = open(cardfile, encoding="latin-1")
			print("Loading file " + cardfile)
			start = len(codetext)
			codetext.extend(self.encode_text(cardtext.read()))
			end = len(codetext)
			bookranges.append({"start": start, "end": end, "name": cardfile.rsplit("/", 1)[-1]})
			cardtext.close()

		if len(bookranges) == 0:
			sys.exit("No training data has been found. Aborting.")

		# For validation, use roughly 90K of text,
		# but no more than 10% of the entire text
		# and no more than 1 book in 5 => no validation at all for 5 files or fewer.

		# 10% of the text is how many files ?
		total_len = len(codetext)
		validation_len = 0
		nb_books1 = 0
		for book in reversed(bookranges):
			validation_len += book["end"]-book["start"]
			nb_books1 += 1
			if validation_len > total_len // 10:
				break

		# 90K of text is how many books ?
		validation_len = 0
		nb_books2 = 0
		for book in reversed(bookranges):
			validation_len += book["end"]-book["start"]
			nb_books2 += 1
			if validation_len > 90*1024:
				break

		# 20% of the books is how many books ?
		nb_books3 = len(bookranges) // 5

		# pick the smallest
		nb_books = min(nb_books1, nb_books2, nb_books3)

		if nb_books == 0 or not validation:
			cutoff = len(codetext)
		else:
			cutoff = bookranges[-nb_books]["start"]
		valitext = codetext[cutoff:]
		codetext = codetext[:cutoff]
		return codetext, valitext, bookranges


	def print_data_stats(self,datalen, valilen, epoch_size):
		datalen_mb = datalen/1024.0/1024.0
		valilen_kb = valilen/1024.0
		print("Training text size is {:.2f}MB with {:.2f}KB set aside for validation.".format(datalen_mb, valilen_kb)
			  + " There will be {} batches per epoch".format(epoch_size))
	
	def data_stats(self,datalen, valilen, epoch_size):
		datalen_mb = datalen/1024.0/1024.0
		valilen_kb = valilen/1024.0
		return ("Training text size is {:.2f}MB with {:.2f}KB set aside for validation.".format(datalen_mb, valilen_kb)
			  + " There will be {} batches per epoch".format(epoch_size))

	def print_validation_header(self,validation_start, bookranges):
		module_logger.info('printing validation header')
		bookindex = self.find_book_index(validation_start, bookranges)
		books = ''
		for i in range(bookindex, len(bookranges)):
			books += bookranges[i]["name"]
			if i < len(bookranges)-1:
				books += ", "
		print("{: <60}".format("Validating on " + books), flush=True)


	def print_validation_stats(self,loss, accuracy):
		print("VALIDATION STATS:                                  loss: {:.5f},       accuracy: {:.5f}".format(loss,
																											   accuracy))


	def print_text_generation_header(self):
		print()
		print("┌{:─^111}┐".format('Generating random text from learned state'))


	def print_text_generation_footer(self):
		print()
		print("└{:─^111}┘".format('End of generation'))


	def frequency_limiter(self,n, multiple=1, modulo=0):
		def limit(i):
			return i % (multiple * n) == modulo*multiple
		return limit
		
		
	
class Progress:
    """Text mode progress bar.
    Usage:
            p = Progress(30)
            p.step()
            p.step()
            p.step(start=True) # to restart form 0%
    The progress bar displays a new header at each restart."""
    def __init__(self, maxi, size=100, msg=""):
        """
        :param maxi: the number of steps required to reach 100%
        :param size: the number of characters taken on the screen by the progress bar
        :param msg: the message displayed in the header of the progress bat
        """
        self.maxi = maxi
        self.p = self.__start_progress(maxi)()  # () to get the iterator from the generator
        self.header_printed = False
        self.msg = msg
        self.size = size

    def step(self, reset=False):
        if reset:
            self.__init__(self.maxi, self.size, self.msg)
        if not self.header_printed:
            self.__print_header()
        next(self.p)

    def __print_header(self):
        print()
        format_string = "0%{: ^" + str(self.size - 6) + "}100%"
        print(format_string.format(self.msg))
        self.header_printed = True

    def __start_progress(self, maxi):
        def print_progress():
            # Bresenham's algorithm. Yields the number of dots printed.
            # This will always print 100 dots in max invocations.
            dx = maxi
            dy = self.size
            d = dy - dx
            for x in range(maxi):
                k = 0
                while d >= 0:
                    print('=', end="", flush=True)
                    k += 1
                    d -= dx
                d += dy
                yield k

        return print_progress	
		

	
