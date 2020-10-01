import os
import glob

def clean_directory(directory_path):
    files = glob.glob(f"{directory_path}*.png")
    for f in files:
        os.remove(f)

def main():
    pass

if __name__ == '__main__':
    main()