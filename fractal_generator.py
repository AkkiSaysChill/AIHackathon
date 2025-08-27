
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    img = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            cx = np.linspace(x_min, x_max, width)[x]
            cy = np.linspace(y_min, y_max, height)[y]
            c = complex(cx, cy)
            img[y, x] = mandelbrot(c, max_iter)
    return img

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a Mandelbrot set image.')
    parser.add_argument('--width', type=int, default=800, help='Width of the image.')
    parser.add_argument('--height', type=int, default=800, help='Height of the image.')
    parser.add_argument('--x_min', type=float, default=-2.0, help='x_min for the complex plane.')
    parser.add_argument('--x_max', type=float, default=1.0, help='x_max for the complex plane.')
    parser.add_argument('--y_min', type=float, default=-1.5, help='y_min for the complex plane.')
    parser.add_argument('--y_max', type=float, default=1.5, help='y_max for the complex plane.')
    parser.add_argument('--max_iter', type=int, default=256, help='Maximum number of iterations.')
    parser.add_argument('--colormap', type=str, default='hot', help='Matplotlib colormap.')
    parser.add_argument('--output', type=str, default='mandelbrot.png', help='Output file name.')
    args = parser.parse_args()

    mandelbrot_set = generate_mandelbrot(args.width, args.height, args.x_min, args.x_max, args.y_min, args.y_max, args.max_iter)

    plt.figure(figsize=(10, 10))
    plt.imshow(mandelbrot_set, cmap=args.colormap, extent=[args.x_min, args.x_max, args.y_min, args.y_max])
    plt.title("Mandelbrot Set")
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.savefig(args.output)

    print(f"Mandelbrot set saved as {args.output}")
