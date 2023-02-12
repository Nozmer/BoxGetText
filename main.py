import argparse
import configparser
import pytesseract
from termcolor import colored
import os
import time


def print_scan(name_file):
    # store active_window
    active_window = os.popen("xdotool getactivewindow").read().strip()

    # minimize window
    os.system("xdotool windowminimize $(xdotool getactivewindow)")
    time.sleep(0.5)

    # check folder
    if not os.path.exists("data"):
        os.mkdir("data")

    # select area and save in data
    os.system("cd data \n"
              "import base.jpg")

    imageOCR = pytesseract.image_to_string("data/base.jpg")
    sentence = imageOCR.replace("\n", " ").capitalize()

    with open(name_file, 'a') as file:
        file.write("# {}\n#\n\n".format(sentence))

    print("Save in file: {}".format(colored(sentence, "green")))

    # reopen window
    os.system("xdotool windowactivate {}".format(active_window))


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="file name")
    args = parser.parse_args()

    if args.file:
        config['DEFAULT']['file'] = args.file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("File name:", args.file)
        print_scan(args.file)
    else:
        file_name = config.get('DEFAULT', 'file', fallback=None)
        if file_name:
            print("File name:", file_name)
            print_scan(file_name)
        else:
            print("No file name specified, use --file nameFile.txt")


main()
print("\nThe file name is saved automatically, just run 'python3 main.py',"
      " if necessary change the file name using '--file'")
