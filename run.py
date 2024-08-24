from argparse import ArgumentParser
from mimetypes import guess_type
from os import listdir
from os.path import basename, dirname, exists, join, realpath

from img2pdf import convert  # type: ignore


def get_images(img_dir: str, real_path: bool = True, test_pic: bool = False, skip_hidden: bool = True):
    for file in sorted(listdir(img_dir)):
        if skip_hidden and file.startswith("."):
            continue
        file_type = get_file_mime_type(file)
        if file_type and file_type in ["image/jpeg", "image/png"]:
            out_filepath = realpath(join(img_dir, file)) if real_path else file
            if test_pic:
                try:
                    convert(out_filepath)
                    yield out_filepath
                except:
                    print(f"Unable to convert: {out_filepath}")
            else:
                yield out_filepath


def get_file_mime_type(file_path: str) -> str | None:
    return guess_type(file_path)[0]


def run():
    # Argument parser for command line that takes in a directory and convert all the image files in the directory to a pdf file
    parser = ArgumentParser(
        description="Convert all the image files in a directory to a pdf file"
    )
    parser.add_argument("-d", "--dir", help="The directory containing the image files")
    args = parser.parse_args()
    directory = args.dir

    # Check id directory exists
    if not exists(directory):
        print(f"Directory {directory} does not exist")
        return

    try:
        real_path = realpath(directory)
        dir_name = basename(real_path)
        base_path = dirname(real_path)

        with open(join(base_path, f"{dir_name}.pdf"), "wb") as pdf_file:
            pdf_file.write(convert(list(get_images(real_path, test_pic=False, skip_hidden=True))))
    except Exception as e:
        print(f"Unable to parse {directory}, \nError: {e}")


if __name__ == "__main__":
    run()
