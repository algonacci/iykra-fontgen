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
        return  # Exit the function if the font cannot be loaded

    os.makedirs(output_dir, exist_ok=True)
    for char_code in range(char_start, char_end):
        char = chr(char_code)
        try:
            bbox = font.getbbox(char)
            size = (1024, 1024)
            image = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            draw.text((0, 0), char, font=font, fill="black")
            image = image.crop(bbox)

            image_path = os.path.join(output_dir, f"{char_code}.png")
            image.save(image_path)
            print(f"Saved {image_path}")
        except Exception as e:
            print(f"Error rendering character '{char}': {e}")


def transform_fonts(font_dir: str, output_dir: str):
    for filename in os.listdir(font_dir):
        font_path = os.path.join(font_dir, filename)
        dirname = Path(filename).stem
        font_output_dir = os.path.join(output_dir, dirname)
        try:
            transform_font(font_path, font_output_dir)
        except Exception as err:
            print(f"Error processing {filename}")
            print(repr(err))


def transform_google_fonts(
    bucket_name: str,
    raw_prefix: str,
    cleaned_prefix: str,
    font_dir: str,
    dataset_dir: str,
):
    os.makedirs(dataset_dir, exist_ok=True)
    download_dir_from_gcs(bucket_name, raw_prefix, font_dir)
    transform_fonts(font_dir, dataset_dir)
    upload_dir_to_gcs(dataset_dir, bucket_name, cleaned_prefix)
