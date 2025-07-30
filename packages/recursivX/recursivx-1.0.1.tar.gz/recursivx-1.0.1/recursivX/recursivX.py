import os
import zipfile
import lzma
import bz2
import gzip
import shutil
import tarfile



USAGE="""


     ▄▄▄ ▗▞▀▚▖▗▞▀▘█  ▐▌ ▄▄▄ ▄▄▄ ▄ ▄   ▄ ▗▖  ▗▖
    █    ▐▛▀▀▘▝▚▄▖▀▄▄▞▘█   ▀▄▄  ▄ █   █  ▝▚▞▘ 
    █    ▝▚▄▄▖         █   ▄▄▄▀ █  ▀▄▀    ▐▌  
                                █       ▗▞▘▝▚▖

===============================================================
Recursive Archive Extractor with Password Detection and Logging
===============================================================

Author: www.github.com/Paul00

Supported formats:
  - .zip (detects password-protected archives)
  - .xz
  - .bz2
  - .gz
  - .tar

This script recursively extracts nested archives and logs any password-protected ZIP files
that it encounters, halting at that point unless a password is provided manually.

Usage:
------
Run the script from the command line:

    python recursivX.py input_archive.ext -o output_directory

Arguments:
  input_archive.ext   The starting archive file (e.g., file.zip or file.bz2)
  -o / --output       Optional: Directory to extract files into (default: ./extracted)

Example:
    python recursivX.py sample.zip -o unpacked_layers

Output:
-------
- Extracted files will be placed in nested directories: ./extracted/layer_1/, layer_2/, etc.
- A log file will be written to: ./extracted/extraction_log.txt
- If a password-protected ZIP file is encountered, its details will be logged and copied to:
  ./extracted/final_locked_layer.zip

"""


def detect_format(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(512)  # Read enough for tar magic
    if header.startswith(b'\x50\x4B\x03\x04'):
        return 'zip'
    elif header.startswith(b'\xFD\x37\x7A\x58\x5A\x00'):
        return 'xz'
    elif header.startswith(b'\x42\x5A\x68'):
        return 'bz2'
    elif header.startswith(b'\x1F\x8B'):
        return 'gz'
    elif b'ustar' in header:
        return 'tar'
    return 'unknown'


def rename_by_type(filepath, log_path=None, layer=None):
    ftype = detect_format(filepath)
    if ftype == 'unknown':
        return filepath, None
    new_path = filepath + f'.' + ftype
    os.rename(filepath, new_path)
    
    if log_path and layer is not None:
        with open(log_path, "a") as log:
            log.write(f"[Layer {layer}] Detected format: {ftype} — renamed to: {os.path.basename(new_path)}\n")
    
    return new_path, ftype


def extract_zip(zip_path, output_dir, layer, log_path, output_root):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            try:
                zip_ref.extractall(output_dir)
                return True
            except RuntimeError as e:
                if 'password required' in str(e).lower():
                    contents = zip_ref.namelist()
                    print(f"[!] Password-protected ZIP at layer {layer}: {os.path.basename(zip_path)}")
                    print(f"    > Encapsulated files: {contents}")
                    with open(log_path, "a") as log:
                        log.write(f"[Layer {layer}] {os.path.basename(zip_path)} requires password\n")
                        log.write(f"  → Encapsulated files: {', '.join(contents)}\n\n")
                    dest_path = os.path.join(output_root, f'final_locked_layer.zip')
                    shutil.copy(zip_path, dest_path)
                    print(f"[→] Copied locked ZIP to: {dest_path}")
                    return False
                else:
                    raise e
    except Exception as e:
        print(f"[!] Unexpected error at layer {layer} on file {zip_path}: {e}")
        return False


def extract_xz(xz_path, output_dir):
    out_file = os.path.join(output_dir, os.path.basename(xz_path).replace('.xz', ''))
    with lzma.open(xz_path) as f_in, open(out_file, 'wb') as f_out:
        f_out.write(f_in.read())
    return out_file


def extract_bz2(bz2_path, output_dir):
    out_file = os.path.join(output_dir, os.path.basename(bz2_path).replace('.bz2', ''))
    with bz2.open(bz2_path, 'rb') as f_in, open(out_file, 'wb') as f_out:
        f_out.write(f_in.read())
    return out_file


def extract_gz(gz_path, output_dir):
    out_file = os.path.join(output_dir, os.path.basename(gz_path).replace('.gz', ''))
    with gzip.open(gz_path, 'rb') as f_in, open(out_file, 'wb') as f_out:
        f_out.write(f_in.read())
    return out_file


def extract_tar(tar_path, output_dir):
    try:
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path=output_dir)
            return True
    except Exception as e:
        print(f"[!] Failed to extract TAR file: {tar_path} — {e}")
        return False


def extract_layers(start_file, output_root):
    print("""


     ▄▄▄ ▗▞▀▚▖▗▞▀▘█  ▐▌ ▄▄▄ ▄▄▄ ▄ ▄   ▄ ▗▖  ▗▖
    █    ▐▛▀▀▘▝▚▄▖▀▄▄▞▘█   ▀▄▄  ▄ █   █  ▝▚▞▘ 
    █    ▝▚▄▄▖         █   ▄▄▄▀ █  ▀▄▀    ▐▌  
                                █       ▗▞▘▝▚▖
                                          
    """)
    os.makedirs(output_root, exist_ok=True)
    log_path = os.path.join(output_root, "extraction_log.txt")
    current_file = start_file
    current_dir = output_root
    layer = 0
    last_successful_layer = -1

    while True:
        print(f"\n[Layer {layer}] Processing: {os.path.basename(current_file)}")
        renamed_path, file_type = rename_by_type(current_file, log_path=log_path, layer=layer)
        if not file_type:
            print("[!] Unknown file type. Stopping.")
            break

        next_dir = os.path.join(output_root, f'layer_{layer + 1}')
        os.makedirs(next_dir, exist_ok=True)

        success = False

        if file_type == 'zip':
            success = extract_zip(renamed_path, next_dir, layer, log_path, output_root)
            if not success:
                print("[!] Stopped due to password protection.")
                break
        elif file_type == 'xz':
            current_file = extract_xz(renamed_path, next_dir)
            success = True
        elif file_type == 'bz2':
            current_file = extract_bz2(renamed_path, next_dir)
            success = True
        elif file_type == 'gz':
            current_file = extract_gz(renamed_path, next_dir)
            success = True
        elif file_type == 'tar':
            success = extract_tar(renamed_path, next_dir)
            if not success:
                break
        else:
            print("[!] Unsupported file type. Halting.")
            break

        if success:
            last_successful_layer = layer

        files = os.listdir(next_dir)
        files = [f for f in files if os.path.isfile(os.path.join(next_dir, f))]
        if not files:
            print("[✓] Extraction complete — no further nested files.")
            break

        current_file = os.path.join(next_dir, files[0])
        current_dir = next_dir
        layer += 1

    print(f"\n[✓] Finished at layer {last_successful_layer+1}")
    print(f"[→] Log written to: {log_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Recursive archive extractor with password detection and logging",
        epilog=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input_file", help="Starting archive")
    parser.add_argument("-o", "--output", default="extracted", help="Output directory")
    args = parser.parse_args()

    extract_layers(args.input_file, args.output)
  

if __name__ == "__main__":
    main()

