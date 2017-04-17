# Engineer: Christopher Parks
# Contact: cparks13 AT live.com

import zlib  # Used for DEFLATE compression.
import brotli  # Used for Brotli compression. Requires you run "pip install brotlipy" on Win/OS X to install the lib
import lzma  # Used for LZMA compression.
import lzw as lzw  # Used for LZW compression.
import time  # Used for recording how long a compression algorithm took to run

import matplotlib.pyplot as plot  # Used for displaying trial data in a bar graph format
import numpy as np  # Used with plotting trial data in bar format

file_compression_size = np.empty((4,4))


def report_compression(indatlen, outdatlen, timediff):
    print('{} bytes => {} bytes'.format(indatlen, outdatlen))  # Report the file size before and after compression
    print("Took {} seconds to finish compression.\n".format(timediff))


def report_decompression(origdatlen, decompdatlen, timediff):
    print("Took {} seconds to finish decompression.".format(timediff))
    print("Received {}/{} bytes.\n".format(decompdatlen, origdatlen))  # Bytes Received / # Original Bytes


def run_deflate(indata, p, i):
    print("DEFLATE on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = zlib.compress(indata, zlib.DEFLATED)
    file_compression_size[i, 0] = len(outdata)
    report_compression(len(indata), len(outdata), time.clock()-start)

    start = time.clock()
    indatlen = len(indata)
    indata = zlib.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock()-start)


def run_brotli(indata, p, i):
    print("Brotli on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = brotli.compress(indata)
    file_compression_size[i, 1] = len(outdata)
    report_compression(len(indata), len(outdata), time.clock() - start)

    start = time.clock()
    indatlen = len(indata)
    indata = brotli.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start)


def run_lzma(indata, p, i):
    print("LZMA on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = lzma.compress(indata)
    file_compression_size[i, 2] = len(outdata)
    report_compression(len(indata), len(outdata), time.clock() - start)

    start = time.clock()
    indatlen = len(indata)
    indata = lzma.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start)


def run_lzw(indata, p, i):
    print("LZW on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = lzw.compress(indata)
    file_compression_size[i, 3] = len(outdata)
    report_compression(len(indata), len(outdata), time.clock() - start)

    #start = time.clock()
    #indatlen = len(indata)
    #indata = lzw.decompress(outdata)
    #report_decompression(indatlen, len(indata), time.clock() - start)


def run_alg_test(f, p, i):
    indata = f.read()
    run_deflate(indata, p, i)
    run_brotli(indata, p, i)
    run_lzma(indata, p, i)
    if len(indata) < 100000000:  # Force skip 100 MB file until we can fix memory error issues
        indata = "".join(map(chr, indata))  # Convert bytes to string format for LZW function
        run_lzw(indata, p, i)
    else:
        file_compression_size[i, 3] = len(indata)


def subplot_setup(ax, i):
    xlab = ('DEFLATE', 'Brotli', 'LZMA', 'LZW')
    x_pos = np.arange(len(xlab))
    ax.set_xlabel('Compression Algorithm')
    ax.set_ylabel('Compressed File Size (Bytes)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xlab)
    ax.bar(x_pos, file_compression_size[i, :], align='center', color='green')

#  --------MAIN PROGRAM EXECUTION--------

path = input("Please enter text file with file paths. File paths must be newline separated.")
try:
    file = open(path, 'rb')
except:
    print('Error: File with file paths does not exist, or cannot be read.')
else:
    paths = file.readlines()
    i = 0
    for p in paths:
        p = p.decode('utf-8')
        if p.endswith('\r\n'):
            p = p[:-2]  # Trim '\r\n' from the end of the file paths, because Python doesn't.
        try:
            f = open(p, 'rb')
        except:
            print("Error: '" + p + "' does not exist.")
        else:  # Read the data in and execute the compression algorithm on it
            run_alg_test(f, p, i)
            i += 1

    fig, ax = plot.subplots()
    ax1 = fig.add_subplot(2,2,1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2,2,3)
    ax4 = fig.add_subplot(2,2,4)
    ax1.set_title('Compressed File Size - 1 KB File')
    ax2.set_title('Compressed File Size - 100 KB File')
    ax3.set_title('Compressed File Size - 1 MB File')
    ax4.set_title('Compressed File Size - 100 MB File')
    subplot_setup(ax1, 0)
    subplot_setup(ax2, 1)
    subplot_setup(ax3, 2)
    subplot_setup(ax4, 3)
    plot.show()
