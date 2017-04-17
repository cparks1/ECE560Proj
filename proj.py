# Engineer: Christopher Parks
# Contact: cparks13 AT live.com

import zlib  # Used for DEFLATE compression.
import brotli  # Used for Brotli compression. Requires you run "pip install brotlipy" on Win/OS X to install the lib
import lzma  # Used for LZMA compression.
import lzw as lzw  # Used for LZW compression.
import time  # Used for recording how long a compression algorithm took to run


def run_deflate(indata, p):
    print("DEFLATE on File: '" + p + "'")  # Report the file name
    outdata = zlib.compress(indata, zlib.DEFLATED)
    print('{} bytes => {} bytes'.format(len(indata), len(outdata)))  # Report the file size before and after compression


def run_brotli(indata, p):
    print("Brotli on File: '" + p + "'")  # Report the file name
    outdata = brotli.compress(indata)
    print('{} bytes => {} bytes'.format(len(indata), len(outdata)))  # Report the file size before and after compression

def run_lzma(indata, p):
    print("LZMA on File: '" + p + "'")  # Report the file name
    outdata = lzma.compress(indata)
    print('{} bytes => {} bytes'.format(len(indata), len(outdata)))  # Report the file size before and after compression

def run_lzw(indata, p):
    print("LZW on File: '" + p + "'")  # Report the file name
    instrdata = "".join(map(chr, indata))
    outdata = lzw.compress(instrdata)
    print('{} bytes => {} bytes'.format(len(instrdata), len(outdata)))  # Report the file size before and after compression


def run_alg_test(f, p):
    indata = f.read()
    start = time.clock()
    run_deflate(indata, p)
    print("Took {} seconds to finish.\n".format(time.clock() - start))

    start = time.clock()
    run_brotli(indata, p)
    print("Took {} seconds to finish.\n".format(time.clock() - start))

    start = time.clock()
    run_lzma(indata, p)
    print("Took {} seconds to finish.\n".format(time.clock() - start))

    start = time.clock()
    run_lzw(indata, p)
    print("Took {} seconds to finish.\n".format(time.clock() - start))

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
