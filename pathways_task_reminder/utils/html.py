from pathlib import Path
import subprocess


def to_image_path(inpath: Path, outpath: Path):
    cmd = [
        "wkhtmltoimage",
        "--width",
        str(400),
        "--format",
        outpath.suffix[1:],
        str(inpath),
        str(outpath),
    ]
    subprocess.run(cmd)
    assert outpath.exists()
    return outpath
