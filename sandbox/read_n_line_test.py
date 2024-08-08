import os


file = '../data/07-08_17-57-53_accel.csv'
lines_to_buffer = 10
n = 0
with open(file, 'rb') as f:
    try:
        f.seek(-2, os.SEEK_END)
        while n < lines_to_buffer:
            f.seek(-2, os.SEEK_CUR)
            if f.read(1) == b'\n':
                n += 1
    except OSError:
        f.seek(0)
    remainder = f.readlines()
    data = ""
    for line in remainder:
        data += line.decode()
    print(data)
