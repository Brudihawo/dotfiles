import sys
import subprocess as sp
from typing import Callable, ParamSpec, TypeVar
from PIL.ImageFilter import BoxBlur
from PIL import Image
import zipfile
import tempfile
from dataclasses import dataclass
from functools import wraps
import time

T = TypeVar("T")
P = ParamSpec("P")
def timed(fn: Callable[P, T]) -> Callable[P, T]:
    @wraps(fn)
    def f_inner(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.monotonic()
        ret = fn(*args, **kwargs)
        end = time.monotonic()
        print(f"{fn.__name__}: {(end - start)} s")
        return ret

    return f_inner

@dataclass
class Monitor:
    w: int
    h: int
    xoff: int
    yoff: int

@timed
def parse_mon_info(line: str) -> Monitor:
    cfg = line.strip().split(" ")[2]
    w = int(cfg.split("x")[0].split("/")[0])
    h = int(cfg.split("x")[1].split("/")[0])
    xoff, yoff = cfg.split("/")[-1].split("+")[1:]
    xoff = int(xoff)
    yoff = int(yoff)
    return Monitor(w, h, xoff, yoff)


@timed
def get_monitor_info():
    out = sp.getoutput("xrandr --current")
    _, w_tot, _, h_tot = out.splitlines()[0].split(",")[1].strip().split()
    w_tot = int(w_tot)
    h_tot = int(h_tot)

    mons_o = sp.getoutput("xrandr --listactivemonitors").splitlines()[1:]
    monitors = [parse_mon_info(line) for line in mons_o]
    return w_tot, h_tot, monitors


@timed
def generate_bkg(w_tot: int, h_tot: int, monitors: list[Monitor], input: Image.Image, path: str):
    out_raw = Image.new("RGB", (w_tot, h_tot), color="white")
    for m in monitors:
        out_raw.paste(input.resize((m.w, m.h), Image.Resampling.BILINEAR), (m.xoff, m.yoff))
    out_raw.save(path)


@timed
def generate_lockscreen(w_tot: int, h_tot: int, monitors: list[Monitor], input: Image.Image, path: str):
    out_blurred = Image.new("RGB", (w_tot, h_tot), color="white")
    inp_downsized = input.resize((input.width // 16, input.height // 16), Image.Resampling.BILINEAR)
    inp_filtered = inp_downsized.filter(BoxBlur(1))
    for m in monitors:
        out_blurred.paste(inp_filtered.resize((m.w, m.h), Image.Resampling.BILINEAR), (m.xoff, m.yoff))
    out_blurred.save(path)


@timed
def main():
    infile, out_raw_path, out_blurred_path = sys.argv[1:4]

    tmpdir = tempfile.mkdtemp()
    expath = zipfile.ZipFile(infile).extract("mergedimage.png", tmpdir)

    w_tot, h_tot, monitors = get_monitor_info()
    input = Image.open(expath)

    generate_bkg(w_tot, h_tot, monitors, input, out_raw_path)
    sp.call("nitrogen --restore".split())
    generate_lockscreen(w_tot, h_tot, monitors, input, out_blurred_path)


if __name__ == "__main__":
    main()
