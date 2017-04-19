# Engineer: Christopher Parks
# Contact: cparks13 AT live.com
# NOTE: This MUST be run with a 64 bit version of Python to get it to run on the 100 MB file

import zlib  # Used for DEFLATE compression.
import brotli  # Used for Brotli compression. Requires you run "pip install brotlipy" on Win/OS X to install the lib
import lzma  # Used for LZMA compression.
import gzip  # Used for GZIP compression.
import time  # Used for recording how long a (de)compression algorithm took to run
import winsound  # Used for notifying the user the program has finished running, since it takes awhile.

import matplotlib.pyplot as plot  # Used for displaying trial data in a bar graph format
import numpy as np  # Used with plotting trial data in bar format


file_compression_size = np.empty((4,4))  # Stores the compression ratio of each algorithm for all 4 test files
file_compression_speed = np.empty((4,4))  # Stores the speed of compression of each algorithm for all 4 test files
file_decompression_speed = np.empty((4,4))  # Stores the speed of decompression of each algorithm for all 4 test files


def report_compression(indatlen, outdatlen, timediff, i, j):
    print('{} bytes => {} bytes'.format(indatlen, outdatlen))  # Report the file size before and after compression
    print("Took {} seconds to finish compression.\n".format(timediff))
    file_compression_speed[i,j] = timediff


def report_decompression(origdatlen, decompdatlen, timediff, i, j):
    print("Took {} seconds to finish decompression.".format(timediff))
    print("Received {}/{} bytes.\n".format(decompdatlen, origdatlen))  # Bytes Received / # Original Bytes
    file_decompression_speed[i, j] = timediff


def run_deflate(indata, p, i):
    print("DEFLATE on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = zlib.compress(indata, zlib.DEFLATED)
    file_compression_size[i, 0] = len(outdata)/len(indata)
    report_compression(len(indata), len(outdata), time.clock()-start, i, 0)

    start = time.clock()
    indatlen = len(indata)
    indata = zlib.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock()-start, i, 0)


def run_brotli(indata, p, i):
    print("Brotli on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = brotli.compress(indata)
    file_compression_size[i, 1] = len(outdata)/len(indata)
    report_compression(len(indata), len(outdata), time.clock() - start, i, 1)

    start = time.clock()
    indatlen = len(indata)
    indata = brotli.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start, i, 1)


def run_lzma(indata, p, i):
    print("LZMA on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = lzma.compress(indata)
    file_compression_size[i, 2] = len(outdata)/len(indata)
    report_compression(len(indata), len(outdata), time.clock() - start, i, 2)

    start = time.clock()
    indatlen = len(indata)
    indata = lzma.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start, i, 2)


def run_gzip(indata, p, i):
    print("GZIP on File: '" + p + "'")  # Report the file name
    start = time.clock()
    outdata = gzip.compress(indata)
    file_compression_size[i, 3] = len(outdata)/len(indata)
    report_compression(len(indata), len(outdata), time.clock() - start, i, 3)

    start = time.clock()
    indatlen = len(indata)
    indata = gzip.decompress(outdata)
    report_decompression(indatlen, len(indata), time.clock() - start, i, 3)

def run_alg_test(f, p, i):
    indata = f.read()
    run_deflate(indata, p, i)
    run_brotli(indata, p, i)
    run_lzma(indata, p, i)
    run_gzip(indata, p, i)

xlab = ('DEFLATE', 'Brotli', 'LZMA', 'GZIP')
x_pos = np.arange(len(xlab))


def ax_set_x_ticksandlabels(ax):  # Sets up the x axis for our figures.
    ax.set_xlabel('Compression Algorithm')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xlab)


def comp_ratio_subplot_setup(ax, i, title):
    ax_set_x_ticksandlabels(ax)
    ax.set_ylabel('Compression Ratio (%)')
    ax.set_title(title)
    ax.bar(x_pos, file_compression_size[i, :], align='center', color=['red','green','blue','magenta'])


def comp_speed_subplot_setup(ax, i, title):
    ax_set_x_ticksandlabels(ax)
    ax.set_ylabel('Compression Speed (s)')
    ax.set_title(title)
    ax.bar(x_pos, file_compression_speed[i, :], align='center', color=['red', 'green', 'blue', 'magenta'])


def decomp_speed_subplot_setup(ax, i, title):
    ax_set_x_ticksandlabels(ax)
    ax.set_ylabel('Decompression Speed (s)')
    ax.set_title(title)
    ax.bar(x_pos, file_decompression_speed[i, :], align='center', color=['red', 'green', 'blue', 'magenta'])

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
        if p.startswith('#'):
            continue  # '#' at the beginning of a line in the paths file indicates a skip.
        if p.endswith('\r\n'):
            p = p[:-2]  # Trim '\r\n' from the end of the file paths, because Python doesn't.
        try:
            f = open(p, 'rb')
        except:
            print("Error: '" + p + "' does not exist.")
        else:  # Read the data in and execute the compression algorithm on it
            run_alg_test(f, p, i)
            f.close()
            i += 1
    plot.rcdefaults()
    fig, ((ax1, ax2), (ax3, ax4)) = plot.subplots(2, 2)
    fig2, ((ax5, ax6), (ax7, ax8)) = plot.subplots(2,2)
    fig3, ((ax9, ax10), (ax11, ax12)) = plot.subplots(2,2)
    filedesc = ['1 KB Random File', '100 KB Random File', '1 MB Random File', '100 MB Random File']
    comp_ratio_subplot_setup(ax1, 0, 'Compression Ratio - '+filedesc[0])
    comp_ratio_subplot_setup(ax2, 1, 'Compression Ratio - '+filedesc[1])
    comp_ratio_subplot_setup(ax3, 2, 'Compression Ratio - '+filedesc[2])
    comp_ratio_subplot_setup(ax4, 3, 'Compression Ratio - '+filedesc[3])
    comp_speed_subplot_setup(ax5, 0, 'Compression Speed - '+filedesc[0])
    comp_speed_subplot_setup(ax6, 1, 'Compression Speed - '+filedesc[1])
    comp_speed_subplot_setup(ax7, 2, 'Compression Speed - '+filedesc[2])
    comp_speed_subplot_setup(ax8, 3, 'Compression Speed - '+filedesc[3])
    decomp_speed_subplot_setup(ax9,  0, 'Decompression Speed - ' + filedesc[0])
    decomp_speed_subplot_setup(ax10, 1, 'Decompression Speed - ' + filedesc[1])
    decomp_speed_subplot_setup(ax11, 2, 'Decompression Speed - ' + filedesc[2])
    decomp_speed_subplot_setup(ax12, 3, 'Decompression Speed - ' + filedesc[3])
    winsound.Beep(440, 250)
    winsound.Beep(880, 250)
    plot.show()
