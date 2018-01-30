# -*- coding: utf-8 -*-

from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="define the original img you want to handle")
parser.add_argument("-o","--output", help="define the output file")
parser.add_argument("--width", help="width of image", type=int, default=80)
parser.add_argument("--height", help="height of image", type=int, default=80)

args = parser.parse_args()

img = args.file
output = args.output
width = args.width
height = args.height

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!1I;:,\"^`'.")

def get_char(r, g, b, alpha = 256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126*r + 0.7152*g + 0.0722*b)

    unit = (256.0+1)/length
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    img_file = Image.open(img)
    img_file = img_file.resize((width, height), Image.NEAREST)

    txt = ""

    for h_pixel in range(height):
        for w_pixel in range(width):
            txt+=get_char(*img_file.getpixel((w_pixel, h_pixel)))
        txt+='\n'

    print (txt)

    if output:
        with open(output, 'w') as output_file:
            output_file.write(txt)
    else:
        with open("output.txt", 'w') as output_file:
            output_file.write(txt)

