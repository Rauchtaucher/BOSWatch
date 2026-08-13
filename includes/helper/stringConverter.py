#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
little Helper for converting strings

@author: Jens Herrmann
"""

import logging

#
# local helper function to decode a string...
#
def decodeString(inputString = b""):
	"""
	Returns given bytes decoded as str (unicode)

	@type    inputString: bytes
	@param   inputString: bytes to convert to str

	@return:    string decoded to str
	@exception: Exception if decoding failed
	"""
	decodedString = ""
	logging.debug("call decodeString('%s')", inputString)
	# try to find out encoding:
	encodings = ('utf-8', 'windows-1250', 'windows-1252', 'latin_1', 'cp850', 'cp852', 'iso8859_2', 'iso8859_15', 'mac_latin2', 'mac_roman')
	for enc in encodings:
		try:
			decodedString = inputString.decode(enc)
			logging.debug("-- string was encoded in: %s", enc)
			break
		except Exception:
			# if exception for last encoding entry fail, raise exception
			if enc == encodings[-1]:
				logging.warning("no encoding found")
				logging.debug("no encoding found", exc_info=True)
				# no fixing possible, raise exception
				raise
	return decodedString


def convertToUnicode(inputString = ""):
	"""
	Returns given string as str (unicode)

	@type    inputString: str or bytes
	@param   inputString: string to convert to str

	@return:    string as str
	@exception: Exception if converting failed
	"""

	decodedString = ""
	logging.debug("call convertToUnicode('%s')", inputString)

	# nothing to do if inputString is empty
	if len(inputString) > 0:
		# 1. check if integer
		try:
			if int(inputString):
				logging.debug("-- integer")
				# ... then return it
				return inputString
		except ValueError:
			# ... no integer is okay...
			pass

		# 2. Check if inputString is already str (unicode)...
		if isinstance(inputString, str):
			logging.debug("-- unicode")
			return inputString

		try:
			# try to decoding:
			decodedString = decodeString(inputString)
		except:
			logging.warning("decoding string failed")
			logging.debug("encoding string failed", exc_info=True)
			# no fixing possible, raise exception
			raise
	return decodedString



def convertToUTF8(inputString = ""):
	"""
	Returns given string as UTF-8 encoded bytes

	@type    inputString: str or bytes
	@param   inputString: string to convert to UTF-8

	@return:    string as UTF-8 encoded bytes
	@exception: Exception if converting to UTF-8 failed
	"""

	utf8String = b""
	logging.debug("call convertToUTF8('%s')", inputString)

	# nothing to do if inputString is empty
	if len(inputString) > 0:
		try:
			# 1. check if integer
			try:
				if int(inputString):
					logging.debug("-- integer")
					# ... then return it
					return inputString
			except ValueError:
				pass

			# 2. Check if inputString is str (unicode)...
			if isinstance(inputString, str):
				logging.debug("-- unicode")
				# ... then return it encoded as UTF-8
				utf8String = inputString.encode('UTF-8')
				return utf8String

			# 3. check given inputString (bytes) is already UTF-8...
			inputString.decode('UTF-8', 'strict')
			# ... no UnicodeDecodeError exception, inputString ist UTF-8
			logging.debug("-- UTF-8")
			return inputString

		except UnicodeDecodeError:
			# inputString contains non-UTF-8 character
			logging.debug("string contains non-UTF-8 characters: %s", inputString)

			try:
				# try to decoding:
				decodedString = decodeString(inputString)
			except:
				logging.warning("decoding string failed")
				logging.debug("encoding string failed", exc_info=True)
				# no fixing possible, raise exception
				raise

			# inputString should now be decoded...

			try:
				# encode decodedString to UTF-8
				utf8String = decodedString.encode('UTF-8')
			except:
				logging.warning("encoding to UTF-8 failed")
				logging.debug("encoding to UTF-8 failed", exc_info=True)
				# no fixing possible, raise exception
				raise

			# Now we must have an utf8-string, check it:
			try:
				utf8String.decode('UTF-8', 'strict')
				logging.debug("string converting succeeded: %s", utf8String)
			except:
				logging.warning("converting to UTF-8 failed")
				logging.debug("converting to UTF-8 failed", exc_info=True)
				# no fixing possible, raise exception
				raise

			# End of exception UnicodeDecodeError: check given string is already UTF-8

		except:
			logging.warning("error checking given string")
			logging.debug("error checking given string", exc_info=True)
			# no fixing possible, raise exception
			raise

	return utf8String
