import argparse
import os
from winnowing import plagiarismCheck
import heapq as hp

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Plagiarism Check")
    parser.add_argument("-i",
                        "--input",
                        dest="input",
                        help="Folder containing files to compare",
                        default='tests')

    parser.add_argument("-t",
                        "--threshold",
                        dest="threshold",
                        help="Threshold to print similarity",
                        default=0.7)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    folder = os.path.join(dir_path, args.input)
    if not os.path.isdir(folder):
        raise Exception("Input is not a folder. Please check", folder)

    my_heap = []
    for file1 in os.listdir(folder):
        full_path_file1 = os.path.join(folder, file1)
        print(full_path_file1)
        for file2 in os.listdir(folder):
            full_path_file2 = os.path.join(folder, file2)
            if full_path_file1 != full_path_file2:
                similarity, _ = plagiarismCheck(full_path_file1, full_path_file2)

                hp.heappush(my_heap, (similarity, {"source": file1, "target": file2}))

    ## print output
    threshold = float(args.threshold)
    while len(my_heap) > 0:

        (similarity, item) = hp.heappop(my_heap)

        if similarity < threshold:
            continue

        source = item["source"]
        target = item["target"]
        print("{0:0.2f}".format(similarity), " source:", source, "target:", target)

    print("Thank you for using plagiarism checker")