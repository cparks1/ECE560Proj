# Title: randfilegen.py
# Description: To fulfill our project requirements, this python script will require the user to specify a directory
# and then randomly generate text files of the following sizes: 1 KB, 100 KB, 1 MB, 100 MB, and 500 MB. These files
# will be stored in the given directory, along with a text file that specifies the file path of each file.

# Engineer: Christopher Parks
# Email: cparks13 AT live DOT com


import random  # Used for random generation
import string  # Used to grab character sets containing 0-9, A-Z, a-z, and conversion of integers to strings.

sizes = [1000, 100000, 1000000, 100000000, 500000000] # Definition of the file sizes.
r = random.seed(1234)  # Set a seed so files generated in the future are identical.

cwd = input("Define save directory: ")  # Ask the user to define where we'll save the randomly generated text files.
cwd = cwd.replace('\\', '/')  # If the user gave response in format "C:\Users\..." reformat it to "C:/Users/..."
if cwd.endswith('/'):  # If the user added '/' at the end, remove it so we know what to expect.
    cwd = cwd[:-1]

pathsfilepath = cwd+'/'+'560paths.txt'  # Define the path of the file which will hold the locations of the generated files.
pathsfile_opened = False  # Whether or not the paths file has been opened previously.

for filesize in sizes:
    filepath = cwd + '/' + str(filesize) + '.txt'  # Define the path of the file being worked on.
    try:  # Attempt to open file path.
        file = open(filepath, 'w')
    except:  # If there is a failure in opening the file path, notify the user.
        print('Unexpected error. Could not randomly generate a text file at "'+filepath+'".')
    else:  # If opening the file was successful, begin generation.
        for i in range(0, filesize):  # Generate random characters (0-9,A-Z,a-z) and write to file.
            file.write(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits))
        file.close()  # Close the file, as we are finished.
        try:
            file = open(pathsfilepath, 'a' if pathsfile_opened else 'w')  # Wipe the paths file if this is a new run. Append if not.
        except:
            print('Unexpected error. Could not write to the paths file.')
        else:
            pathsfile_opened = True
            file.write(filepath + '\n')
            file.close()
