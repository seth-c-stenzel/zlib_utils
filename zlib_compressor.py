import os, sys, zlib
import json
from collections import OrderedDict


def main():
    while True:
        file_or_folder = input("[F]older\n[Fi]le\n[Q]uit\n> ")
        if file_or_folder.lower() in "fifoq":
            break
        else:
            print("Not F, Fi, or Q. Please try again")

    if file_or_folder.lower() == "q":
        sys.exit()

    if file_or_folder.lower() == "f":
        while True:
            single_binary = input(
                "[S]ingle binary blob file with index file\n[I]ndividual files in source dir\n[Q]uit\n> "
            )
            if single_binary.lower() in "siq":
                break
            else:
                print("Not S, I, or Q. Please try again")

    if "q" in single_binary.lower() or "q" in file_or_folder.lower():
        sys.exit()

    if file_or_folder.lower() == "f":
        folder_to_compress = input("Enter folder path: ").replace('"', "")
        if "s" in single_binary.lower():
            single_binary = True
        elif "i" in single_binary.lower():
            single_binary = False
        zlib_compress_folder(folder_to_compress, single_binary=True)

    elif file_or_folder.lower() == "fi":
        file_to_compress = input("Enter file path: ").replace('"', "")
        zlib_compress_file(file_to_compress)


def zlib_compress_folder(
    folder_to_compress, single_binary=False, conserve_memory=False
):
    if single_binary:
        all_file_data = bytearray()
        all_file_data_index = OrderedDict()
        current_index = 0

        for path, subdirs, files in os.walk(folder_to_compress):
            for name in files:
                relative_path = os.path.join(path, name)
                with open(relative_path, "rb") as f:
                    data = f.read()
                    all_file_data.extend(data)

                    all_file_data_index[
                        relative_path.replace(folder_to_compress, ".")
                    ] = (
                        current_index,
                        len(data),
                    )
                    current_index += len(data)

        compressed_all_file_data = zlib.compress(all_file_data, level=9)
        with open(f"compressed_folder.z", "wb") as f:
            f.write(compressed_all_file_data)

        all_file_data_index = json.dumps(all_file_data_index)
        with open(f"compressed_folder_index.json", "w") as f:
            f.write(all_file_data_index)

    else:
        for path, subdirs, files in os.walk(folder_to_compress):
            for name in files:
                relative_path = os.path.join(path, name)
                zlib_compress_file(relative_path, conserve_memory=conserve_memory)

        compressed_index = json.dumps(compressed_index)
        with open(f"compressed_folder_index.json", "w") as f:
            f.write(compressed_index)
    return True


def zlib_compress_file(file_to_compress, conserve_memory=False):
    with open(file_to_compress, "rb") as f:
        bf_data = f.read()

    compressed_bf_data = zlib.compress(bf_data, level=9)
    with open(f"{file_to_compress}.z", "wb") as f:
        f.write(compressed_bf_data)
    return True


if __name__ == "__main__":
    main()
