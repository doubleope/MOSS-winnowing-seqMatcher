import argparse
import os
import zipfile
from fnmatch import fnmatch
from shutil import copyfile


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Plagiarism Check")
    parser.add_argument("-i",
                        "--input",
                        dest="input",
                        help="Folder containing files to extract and copy to output",
                        default='tests')

    parser.add_argument("-e",
                        "--extension",
                        dest="extension",
                        help="Interested file extensions. Comma separated list.",
                        default='c,txt')
    return parser


def handle_read_zip_file(filepath, output_folder):

    try:
        zfile = zipfile.ZipFile(filepath)

        head, tail_ext = os.path.split(filepath)
        tail = os.path.splitext(tail_ext)[0]
        my_tmp_folder = os.path.join(output_folder, tail)
        zfile.extractall(my_tmp_folder)

        return True
    except:
        print("something went wrong")

    return False


def is_c_programming(full_file_path):

    return fnmatch(full_file_path, "*.c") or fnmatch(full_file_path, "*.cpp")


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if args.input.startswith('/'):
        folder = args.input
    else:
        folder = os.path.join(dir_path, args.input)

    output_folder = os.path.join(folder, 'output_src')

    if not os.path.isdir(folder):
        raise Exception("Input is not a folder. Please check", folder)

    for file1 in os.listdir(folder):
        full_path_file1 = os.path.join(folder, file1)

        is_file = os.path.isfile(full_path_file1)
        if is_file and is_c_programming(full_path_file1):
            copyfile(file1, output_folder)
            os.remove(file1)
        elif is_file and file1.endswith(".zip"):
            if not handle_read_zip_file(full_path_file1, output_folder=output_folder):
                print('Cannot process the file; double check:', file1)
        else:
            print('No processing folder or other file format; double check:', file1)

    print("Thank you for using plagiarism checker")