# Engineer: Christopher Parks
# Contact: cparks13 AT live.com

import zlib  # Used for DEFLATE compression.
import brotli  # Used for Brotli compression. Requires you run "pip install brotlipy" on Win/OS X to install the lib
import lzma  # Used for LZMA compression.
import lzw as lzw  # Used for LZW compression.
import time  # Used for recording how long a compression algorithm took to run


def report_compression(indatlen, outdatlen, timediff):
    print('{} bytes => {} bytes'.format(indatlen, outdatlen))  # Report the file size before and after compression
    print("Took {} seconds to finish compression.\n".format(timediff))


def report_decompression(origdatlen, decompdatlen, timediff):
    print("Took {} seconds to finish decompression.".format(timediff))
    print("Received {}/{} bytes.\n".format(decompdatlen, origdatlen))  # Bytes Received / # Original Bytes

def run_deflate(indata, p):
    print("DEFLATE on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = zlib.compress(indata, zlib.DEFLATED)
    report_compression(len(indata), len(outdata), time.clock()-start)

    start = time.clock()
    indatlen = len(indata)
    indata = zlib.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock()-start)


def run_brotli(indata, p):
    print("Brotli on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = brotli.compress(indata)
    report_compression(len(indata), len(outdata), time.clock() - start)

    start = time.clock()
    indatlen = len(indata)
    indata = brotli.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start)

def run_lzma(indata, p):
    print("LZMA on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = lzma.compress(indata)
    report_compression(len(indata), len(outdata), time.clock() - start)

    start = time.clock()
    indatlen = len(indata)
    indata = lzma.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start)

def run_lzw(indata, p):
    print("LZW on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = lzw.compress(indata)
    report_compression(len(indata), len(outdata), time.clock() - start)

    start = time.clock()
    indatlen = len(indata)
    indata = lzw.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start)


def run_alg_test(f, p):
    indata = f.read()
    run_deflate(indata, p)
    run_brotli(indata, p)
    run_lzma(indata, p)
    #indata = "".join(map(chr, indata))  # Convert bytes to string format for LZW function
    #run_lzw(indata, p)

#  --------MAIN PROGRAM EXECUTION--------

path = input("Please enter text file with file paths. File paths must be newline separated.")
try:
    file = open(path, 'rb')
except:
    print('Error: File with file paths does not exist, or cannot be read.')
else:
    paths = file.readlines()
    for p in paths:
        p = p.decode('utf-8')
        if p.endswith('\r\n'):
            p = p[:-2]  # Trim '\r\n' from the end of the file paths, because Python doesn't.
        try:
            f = open(p, 'rb')
        except:
            print("Error: '" + p + "' does not exist.")
        else:  # Read the data in and execute the compression algorithm on it
            run_alg_test(f, p)
