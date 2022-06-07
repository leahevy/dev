import sys

from pathlib import Path

import typer

from rich import print
from PIL import Image, ImageDraw, ImageFont

import importlib.resources as pkg_resources

import leahevy.fonts as fonts


def gen_project_banner(text: str, output_file: Path):
    if output_file.exists():
        print("Output file exists", file=sys.stderr)
        raise typer.Exit(code=1)

    font_path = str(pkg_resources.path(fonts, "DancingScript-VariableFont_wght.ttf"))
    font_size = 150

    min_width = font_size * 2
    calc_width = int(font_size * (len(text)*.5))
    W, H = max(min_width, calc_width), 220

    img = Image.new('RGBA', (W, H), color = (255, 0, 0, 0))
    fnt = ImageFont.truetype(font_path, font_size)
    d = ImageDraw.Draw(img)
    w, h = d.textsize(text, font=fnt)
    d.text(((W-w)/2,(H-h)/2), text, font=fnt, fill=(153, 204, 255))
 
    img.save(output_file)


def main():
    typer.run(gen_project_banner)


if __name__ == "__main__":
    main()
