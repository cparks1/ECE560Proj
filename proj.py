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
        else:
            # Read the data in and execute the compression algorithm on it
            print("Congratulations, '"+p+"' exists.")
