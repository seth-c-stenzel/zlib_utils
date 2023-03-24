# zlib_utils
Compressor and Extractor for multi-file zlib archives. This utility was created for storing archives for use with Micro Python as an alternative to .zip archives.

# How to use
### compress files
The compressor can be run from the cli with `python .\zlib_compressor.py`. From there you can choose to either compress a single file, or a folder of files. If the single blob file is chosen, this will have all compressed files be stored in one file, and offset index will be generated with that with a .json extention. These two files can then be used to decompressed the compressed files.

### decompress files
The decompressor can be use from the cli like so: `python .\zlib_extractor.py .\compressed_folder.z .\compressed_folder_index.json -d unpacked_files`
