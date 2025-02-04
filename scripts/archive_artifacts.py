import argparse
import os
import zipfile
import time

def make_rel_archive(a_args):
    archive = zipfile.ZipFile("{}.zip".format(a_args.name), "w", zipfile.ZIP_DEFLATED)
    os.utime(a_args.dll, (time.time(), time.time()))
    os.utime(a_args.pdb, (time.time(), time.time()))
    os.utime(a_args.ini, (time.time(), time.time()))
    archive.write(a_args.dll, "SKSE/Plugins/{}".format(os.path.basename(a_args.dll)))
    archive.write(a_args.pdb, "SKSE/Plugins/{}".format(os.path.basename(a_args.pdb)))
    archive.write(a_args.ini, "SKSE/Plugins/{}".format(os.path.basename(a_args.ini)))

def parse_arguments():
    parser = argparse.ArgumentParser(description="archive build artifacts for distribution")
    parser.add_argument("--dll", type=str, help="the full dll path", required=True)
    parser.add_argument("--name", type=str, help="the project name", required=True)
    parser.add_argument("--pdb", type=str, help="the full pdb path", required=True)
    parser.add_argument("--ini", type=str, help="the full ini path", required=False) 
    return parser.parse_args()

def main():
    out = "artifacts"
    try:
        os.mkdir(out)
    except FileExistsError:
        pass
    os.chdir(out)

    args = parse_arguments()
    make_rel_archive(args)

if __name__ == "__main__":
    main()
