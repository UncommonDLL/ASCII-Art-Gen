from PIL import Image, ImageEnhance
import pyfiglet
import os

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

def unique_file(base_name, ext, directory="."):
    counter = 1
    while True:
        unique_name = f"{base_name}_{counter}{ext}" if counter > 1 else f"{base_name}{ext}"
        if not os.path.exists(os.path.join(directory, unique_name)):
            return unique_name
        counter += 1

def resize_image(image, new_width):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ''
    scale_factor = 255 / (len(ASCII_CHARS) - 1)
    for pixel in pixels:
        ascii_str += ASCII_CHARS[min(int(pixel / scale_factor), len(ASCII_CHARS) - 1)]
    return ascii_str

def enhance_image(image, contrast, sharpness):
    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = ImageEnhance.Sharpness(image).enhance(sharpness)
    return image

def text_to_ascii_art(text, directory="."):
    ascii_art = pyfiglet.figlet_format(text)
    ascii_art_file = unique_file("ascii_text", ".txt", directory)
    with open(os.path.join(directory, ascii_art_file), "w") as f:
        f.write(ascii_art)
    return ascii_art, ascii_art_file

def image_to_ascii_art(path, config, directory="."):
    try:
        image = Image.open(path)
    except Exception as e:
        print(e)
        return None, None

    image = resize_image(enhance_image(grayify(image), config['contrast'], config['sharpness']), config['width'])
    ascii_str = pixels_to_ascii(image)
    ascii_img = "\n".join([ascii_str[i:i+config['width']] for i in range(0, len(ascii_str), config['width'])])
    ascii_art_file = unique_file("ascii_image", ".txt", directory)
    with open(os.path.join(directory, ascii_art_file), "w") as f:
        f.write(ascii_img)
    return ascii_img, ascii_art_file

def main():
    mode = input("Choose mode - Image to ASCII (I) or Text to ASCII (T) [I/T]: ").upper()

    if mode == 'I':
        path = input("Enter a valid pathname to an image:\n")
        config = {'width': 100, 'contrast': 2, 'sharpness': 2}
        ascii_art, ascii_art_file = image_to_ascii_art(path, config)
        if ascii_art:
            print(f"ASCII art written to {ascii_art_file}")
    elif mode == 'T':
        text = input("Enter the text for ASCII art:\n")
        ascii_art, ascii_art_file = text_to_ascii_art(text)
        if ascii_art:
            print(f"ASCII art written to {ascii_art_file}")
    else:
        print("Invalid mode selected.")

main()
