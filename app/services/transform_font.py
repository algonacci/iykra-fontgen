import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.helpers.gcs import upload_dir_to_gcs, download_dir_from_gcs


def transform_font(
    font_path: str,
    output_dir: str,
    font_size: int = 128,
    char_start: int = 33,
    char_end: int = 127,
):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Error: Could not open font file: {font_path}")
    os.makedirs(output_dir, exist_ok=True)
    for char_code in range(char_start, char_end):
        char = chr(char_code)
        left, top, right, bottom = font.getbbox(char)
        width = right - left
        heigth = bottom - top

        padding = 10
        size = (width + 2 * padding, heigth + 2 * padding)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.text((padding, padding), char, font=font, fill="black")

        image_path = os.path.join(output_dir, f"{char_code}_{char}.png")
        image.save(image_path)


def transform_fonts(font_dir: str, output_dir: str):
    for filename in os.listdir(font_dir):
        font_path = os.path.join(font_dir, filename)
        dirname = Path(filename).stem
        font_output_dir = os.path(output_dir, dirname)
        transform_font(font_path, font_output_dir)


def transform_google_fonts(
    bucket_name: str,
    raw_prefix: str,
    cleaned_prefix: str,
    font_dir: str,
    dataset_dir: str,
):
    download_dir_from_gcs(bucket_name, raw_prefix, font_dir)
    transform_fonts(font_dir, dataset_dir)
    upload_dir_to_gcs(dataset_dir, bucket_name, cleaned_prefix)
