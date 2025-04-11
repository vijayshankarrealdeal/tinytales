from PIL import Image
import colorsys
import requests, io

def get_brightness(color):
    # color is an iterable of [r, g, b]
    r, g, b = color
    return 0.299 * r + 0.587 * g + 0.114 * b

def get_saturation(color):
    # Normalize values to [0,1]
    r, g, b = [ch / 255 for ch in color]
    return colorsys.rgb_to_hsv(r, g, b)[1]

def get_hue(color):
    # Normalize values to [0,1]
    r, g, b = [ch / 255 for ch in color]
    return colorsys.rgb_to_hsv(r, g, b)[0]

def rgb_to_hex(color):
    # Convert [r, g, b] to hex string (without leading '#')
    return '{:02x}{:02x}{:02x}'.format(*color)

def compress_jpeg(input_path, output_path, quality=85):
    image = open_image(input_path)
    image.save(output_path, format='JPEG', optimize=True, quality=quality)

def open_image(image_path: str) -> Image.Image:
    try:
        if image_path.startswith("http://") or image_path.startswith("https://"):
            response = requests.get(image_path, timeout=10)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
        else:
            image = Image.open(image_path)
        return image.convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Failed to open image at {image_path}: {e}")
