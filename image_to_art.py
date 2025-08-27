
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import argparse

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    mandelbrot_set = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            cx = np.linspace(x_min, x_max, width)[x]
            cy = np.linspace(y_min, y_max, height)[y]
            c = complex(cx, cy)
            mandelbrot_set[y, x] = mandelbrot(c, max_iter)
    return mandelbrot_set

def color_fractal_with_image(fractal_set, image_pixels):
    height, width = fractal_set.shape
    num_pixels = image_pixels.shape[0]
    colored_fractal = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            iteration = int(fractal_set[y, x])
            pixel_index = iteration % num_pixels
            colored_fractal[y, x] = image_pixels[pixel_index]

    return colored_fractal

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create abstract art from an image using a fractal.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    parser.add_argument('--output', type=str, default='abstract_art.png', help='Output file name.')
    parser.add_argument('--width', type=int, default=800, help='Width of the output image.')
    parser.add_argument('--height', type=int, default=800, help='Height of the output image.')
    parser.add_argument('--x_min', type=float, default=-2.0, help='x_min for the complex plane.')
    parser.add_argument('--x_max', type=float, default=1.0, help='x_max for the complex plane.')
    parser.add_argument('--y_min', type=float, default=-1.5, help='y_min for the complex plane.')
    parser.add_argument('--y_max', type=float, default=1.5, help='y_max for the complex plane.')
    parser.add_argument('--max_iter', type=int, default=256, help='Maximum number of iterations.')
    args = parser.parse_args()

    try:
        with Image.open(args.image_path) as img:
            img_pixels = np.array(img.convert('RGB'))
            img_pixels = img_pixels.reshape(-1, 3)
    except FileNotFoundError:
        print(f"Error: Image file not found at {args.image_path}")
        exit()

    print("Generating Mandelbrot set...")
    mandelbrot_set = generate_mandelbrot(args.width, args.height, args.x_min, args.x_max, args.y_min, args.y_max, args.max_iter)

    print("Coloring fractal with image...")
    art_image = color_fractal_with_image(mandelbrot_set, img_pixels)

    plt.imsave(args.output, art_image)

    print(f"Abstract art saved as {args.output}")
