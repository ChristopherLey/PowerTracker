import os


def read_last_n_lines(file_path: str, n: int) -> str:
    """
    Read the last n lines of a file.

    :param file_path: The path to the file.
    :param n: The number of lines to read.
    :return: The last n lines of the file.
    """
    with open(file_path, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while n < 0:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    n += 1
        except OSError:
            f.seek(0)
        remainder = f.readlines()
        data = ""
        for line in remainder:
            data += line.decode()
        return data
