import os
import subprocess


def compress(file):
    """Method that runs the actual compression"""
    level = "ebook"
    filename = os.path.split(file)[-1]
    output_file = file.replace(
        filename, filename.split(".")[0] + f"-compressed-{level}.pdf"
    )
    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{level}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_file}",
        f"{file}",
    ]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    from sys import argv

    file = argv[1]
    compress(file)
