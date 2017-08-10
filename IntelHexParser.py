#!/usr/bin/python

import sys, getopt

def readLines(fullFileName):
	with open(fullFileName) as f:
		lines = f.read().splitlines()
		return lines

class IntelHex:
	len_byteCount = 2
	len_address = 4
	len_typeData = 2
	len_data = 255 # ??? 
	len_checksum = 2
	str_separator = ", "
	str_finalSeparator = "\n"
	str_leftBracket = "<"
	str_rightBracket = ">"
	def __init__(self, byteCount, address, typeData, data, checksum):
		self.byteCount = byteCount
		self.address = address
		self.typeData = typeData
		self.data = data
		self.checksum = checksum
	def __str__(self):
		return self.toString()
	def __repr__(self):
		return self.toString()
	def toString(self):
		# l = []
		# l.append('foo')
		# l.append('bar')
		# s = ''.join(l)
		s = ""
		s += self.str_leftBracket
		s += "byteCount = %d%s" % (self.byteCount, self.str_separator)
		s += "address = %d%s" % (self.address, self.str_separator)
		s += "typeData = %d%s" % (self.typeData, self.str_separator)
		s += "data = %s%s" % (list(self.data), self.str_separator)
		# s += "data = %X%s" % (list(self.data), self.str_separator)
		s += "checksum = %d" % (self.checksum)
		s += self.str_rightBracket
		s += self.str_finalSeparator
		return s



def splitOnIntelHexStructure(line):
	if line[0] == ":":
		byteCount = int(line[1:3], 16)
		if 0 < byteCount <= 255:
			address = int(line[3:7], 16)
			typeData = int(line[7:9], 16)
			
			dataPositionEnd = 9 + (2*byteCount)
			dataLine = line[9:dataPositionEnd]
			data = []
			for i in range(2, len(dataLine)+1, 2): # ? +1
				number = int(dataLine[i-2:i], 16)
				data.append(number)

			checksum = int(line[dataPositionEnd:dataPositionEnd+2], 16)

			realChecksum = 0
			for i in range(2+1, len(line)-1, 2):
				number = int(line[i-2:i], 16)
				realChecksum += number
			realChecksum = (-(realChecksum % 256)) & 0xFF

			if realChecksum == checksum:
				intelHex = IntelHex(byteCount, address, typeData, data, realChecksum)
				return intelHex


def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('test.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			lines = readLines(inputfile)
			intelHexes = list(map(splitOnIntelHexStructure, lines))
			print(intelHexes)
		elif opt in ("-o", "--ofile"):
			outputfile = arg

if __name__ == "__main__":
   main(sys.argv[1:])
