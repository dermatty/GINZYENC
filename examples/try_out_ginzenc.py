import ginzyenc
import sys
import re
import time

# See if an input file (with yencoded info) was given as argument
try:
        inputfilename = sys.argv[1]
        print("Reading from", inputfilename)
        with open(inputfilename, "r") as myfile:
                data=myfile.readlines()
except:
        # No input, so use a pre-fab yencoded file / string, just like you get the BODY (or ARTICLE) from a newsserver
        # source: http://nzbindex.com/search/?q=verysmallfile+2384928394820394

        data = [b'=ybegin line=128 size=173 name=smallfile.rar\r\n', 
                b'|\x8b\x9cKD1*\xf9\xba\x9d**7*******\xcb\xfb\x9eJ\xaa[*\x8b***\x8b***-MW\xe5\xb8\x8e\x92\x95s>Z;*\xde\xab**\x9e\x8f\x9d\x9eW[ZZ\x8c\xa3\x9e\x8f\x9dX\x93\x97\x91\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x94\r\n', 
                b'4\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x944\x8b\x8c\x8d\x8e\x8f\x8e\x90\x91\x92\x93\x9444\xeeg\xa5*j1*\r\n', 
                b'=yend size=173 crc32=8828b45c\r\n']

print("\nINPUT:")
print("First Line", data[0].rstrip())
print("Last Line", data[-1].rstrip())

runs = 10000

bytes0 = bytearray()
for d in data[1:-1]:
        bytes0.extend(d)

# Find size in laste line of yencoded message:
lastline = data[-1].decode()	# For example: '=yend size=173 crc32=8828b45c\r\n' (and ... assuming it's in the last line)
m = re.search('size=(.\d+?) ', lastline)
if m:
    size = int(m.group(1))
print("size of decoded info will be", size)

# Now do the yencode-decoding using ginzyenc:
t0_ginzyenc = time.time()
for i in range(runs):
        decoded_data, output_filename, crc, crc_yenc, crc_correct = ginzyenc.decode_usenet_chunks(data, size)
dt_ginzyenc = time.time() - t0_ginzyenc

print("Result for 1000 runs:")
print("  dt:", dt_ginzyenc)
print("  output_filename:", output_filename)
print("  crc:", crc)
print("  crc_yenc:", crc_yenc)
print("  crc_correct:", crc_correct)
print("  decoded_data:", decoded_data)
