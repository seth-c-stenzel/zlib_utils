import os, zlib, json, errno, sys
from sys import platform


def main():
    if len(sys.argv) > 1:
        folder_to_extract = sys.argv[1].replace(".\\", "").replace('"', "")
    else:
        print("\nMissing required arguments.")
        print(
            "\nUsage:\n> python.exe zlib_extractor.py compressed_folder.z compressed_folder_index.json."
        )
        sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] != "-d":
        compressed_file_path_index = sys.argv[2].replace(".\\", "").replace('"', "")
    else:
        compressed_file_path_index = None

    for i, arg in enumerate(sys.argv):
        if arg == "-d":
            try:
                extract_directory = sys.argv[i + 1]
            except IndexError:
                extract_directory = os.getcwd()

    zlib_extract_files(
        folder_to_extract,
        compressed_file_path_index=compressed_file_path_index,
        extract_directory=extract_directory,
    )


def zlib_extract_files(
    compressed_file_path, compressed_file_path_index="", extract_directory=os.getcwd()
):
    if compressed_file_path_index:
        with open(compressed_file_path_index, "r") as f:
            index_data = f.read()
            files = json.loads(index_data)

        with open(compressed_file_path, "rb") as f:
            decompressed_data = zlib.decompress(f.read())
            initial_dir = os.getcwd()
            if not path_exists(extract_directory):
                mkdirs(extract_directory)
            os.chdir(f"{extract_directory}")
            if platform == "win32":
                slash = "\\"
            else:
                slash = "/"
            for key in files.keys():
                file_name = key.replace(".\\", "").replace("./", "")
                if platform != "win32":
                    file_name = file_name.replace("\\", "/")
                file_start, data_length = files[key]
                file_data = decompressed_data[file_start : data_length + file_start]
                file_directory_path = f"{slash}".join(file_name.split(f"{slash}")[:-1])
                cwd = os.getcwd()
                mkdirs(file_directory_path)
                with open(cwd + slash + file_name, "wb") as f:
                    f.write(file_data)
            os.chdir(initial_dir)
    else:
        with open(compressed_file_path, "rb") as f:
            decompressed_data = zlib.decompress(f.read())

        with open(compressed_file_path.replace(".z", ""), "wb") as f:
            f.write(decompressed_data)


def mkdirs(directories):
    if platform == "win32":
        directory_chain = directories.split("\\")
    else:
        directories = directories.replace("\\", "/")
        directory_chain = directories.split("/")
    cwd = os.getcwd()
    for directory in directory_chain:
        try:
            if directory:
                os.mkdir(directory)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise
        if directory:
            os.chdir(directory)
    os.chdir(cwd)


def path_exists(path):
    try:
        cwd = os.getcwd()
        os.chdir(path)
        os.chdir(cwd)
        return True
    except OSError as e:
        return False


if __name__ == "__main__":
    main()
