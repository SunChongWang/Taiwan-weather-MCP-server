from PIL import Image
from io import BytesIO
import base64
import colorsys
import requests

bg_ansi = "\033[48;2;0;0;0m" # canvas color set to black

def brightness(r, g, b, radar):
    """
    Get the measure of whiteness for infrared and visible images 
    """
    r, g, b = r/255, g/255, b/255
   
    if not radar:
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return v * (1 - s) # whiteness

    return(0.2126 * r + 0.7152 * g + 0.0722 * b) # brightness


def image_to_base64(image_path):
    """ 
    Retrieve and base64 encode the image
    """
    try:
        response = requests.get(image_path, stream=True)
        img = Image.open(response.raw).convert('RGB')
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        buffered.close()
        return(img_base64)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {str(e)}")
        return None

    except Exception as e:
        print(f"Unexpected error processing image: {str(e)}")
        return None

def image_to_colored_ascii(image_path, new_width=120, radar=False):
    """
    Convert an image to colored ASCII art using ANSI escape codes.

    Args:
        image_path (str): Path to the image file.
        new_width (int): Desired character width of output.
        radar (bool): reverse the ascii characters

    Returns:
        str: ASCII art as a markdown-safe code block with ANSI color codes.
    """
    # ASCII characters ordered from dark to light
    ASCII_CHARS = "0123456789"

    if radar == True:
        ASCII_CHARS = "9876543210"

    try:
        # Load image
        response = requests.get(image_path, stream=True)
        img = Image.open(response.raw).convert('RGB')

        if new_width < img.size[0]:
            width, height = img.size
            aspect_ratio = height / width
            new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 is a heuristic correction factor accounting the fact that characters in terminal are taller than wide
            img = img.resize((new_width, new_height))

        # Convert image to colored ASCII
        pixels = img.getdata()
        ascii_art = ""
        for i, (r, g, b) in enumerate(pixels):
            # Brightness for ASCII character selection
            char = ASCII_CHARS[max(int(brightness(r, g, b, radar) * len(ASCII_CHARS)) - 1, 0)]
            ascii_art += f"{bg_ansi}\033[38;2;{r};{g};{b}m{char}\033[0m"
            if (i + 1) % img.size[0] == 0:
                ascii_art += "\n"

        return ascii_art

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {str(e)}")
        return ""

    except Exception as e:
        print(f"Unexpected error processing image: {str(e)}")
        return ""
