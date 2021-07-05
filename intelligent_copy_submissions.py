import argparse
import os
import zipfile
from fnmatch import fnmatch
from shutil import copyfile
from shutil import rmtree


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Intelligent Copy")
    parser.add_argument("-i",
                        "--input",
                        dest="input",
                        help="Folder containing files to extract and copy to output",
                        default='tests/output_src')

    parser.add_argument("-e",
                        "--extension",
                        dest="extension",
                        help="Interested file extensions. Comma separated list.",
                        default='c,txt')
    return parser


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

    output_folder = os.path.join(folder, 'output_target')
    if os.path.exists(output_folder) and os.path.isdir(output_folder):
        rmtree(output_folder)

    if not os.path.isdir(folder):
        raise Exception("Input is not a folder. Please check", folder)

    for my_file in os.listdir(folder):
        full_path_file1 = os.path.join(folder, my_file)
        if os.path.isfile(full_path_file1):
            copyfile(full_path_file1, output_folder)
        else:
            # my_file is a folder
            source_code_paths = []
            source_root = None
            source_file_paths = []
            for root, dirs, files in os.walk(full_path_file1):
                lowercase_root = root.lower()
                if lowercase_root.endswith('macosx') or lowercase_root.endswith('build-debug'):
                    continue

                if source_root is None:
                    source_root = root
                for file in files:
                    full_path = os.path.join(root, file)
                    is_file = os.path.isfile(full_path)
                    if is_file:
                        source_file_paths = source_file_paths + [full_path]
                    if is_file and is_c_programming(full_path):
                        source_code_paths = source_code_paths + [full_path]

            ## only one file in the folder or only one c, cpp in the folder
            if len(source_code_paths) == 1 or len(source_file_paths) == 1:
                if not os.path.isdir(output_folder):
                    os.makedirs(output_folder, exist_ok=True)

                if len(source_code_paths):
                    copyfile(source_code_paths[0], os.path.join(output_folder, my_file + ".cpp"))
                elif len(source_file_paths):
                    copyfile(source_file_paths[0], os.path.join(output_folder, my_file + ".cpp"))

                if source_root is not None:
                    rmtree(source_root)
            else:
                print(full_path_file1, ':Need to manually check')

    print("Thank you for using intelligent copy")