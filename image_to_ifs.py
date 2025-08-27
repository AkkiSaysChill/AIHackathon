#!/usr/bin/env python3

"""
image_to_ifs.py

Fractalize an image using a Chaos-Game-like process on detected edges.
Features:
 - color sampling from the image edges (--colorize)
 - overlay points onto the original image (--overlay)
 - optional dilation of edge mask (--dilate)
 - step parameter: use step ~0.98..1.0 to place points near edges
"""

import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import feature
from skimage.color import rgb2gray
from skimage.morphology import binary_dilation, disk


def fractalize_image(
    image_path: str,
    output_path: str = "fractal.png",
    sigma: float = 2.0,
    dilate: int = 0,
    iterations: int | None = None,
    multiplier: int = 40,
    step: float = 0.98,
    point_size: float = 0.4,
    alpha: float = 0.6,
    colorize: bool = True,
    overlay: bool = True,
    seed: int | None = None,
):
    """
    Parameters:
      image_path: input image
      output_path: saved result
      sigma: Canny smoothing
      dilate: morphological dilation radius (0 = none)
      iterations: exact number of iterations; if None use (n_edge_points * multiplier)
      multiplier: multiplier for edge-point-based default iterations
      step: how much to move toward chosen attractor (0..1). Near 1 places points on edges.
      point_size: matplotlib scatter 's' (point area); increase for thicker points
      alpha: point alpha
      colorize: sample color from original at attractor location
      overlay: draw points on top of original (if False -> black background)
      seed: RNG seed for reproducibility
    """
    # load
    img = Image.open(image_path).convert("RGB")
    img_arr = np.array(img)
    h, w, _ = img_arr.shape

    # edges
    gray = rgb2gray(img_arr)
    edges = feature.canny(gray, sigma=sigma)

    if dilate and dilate > 0:
        edges = binary_dilation(edges, disk(dilate))

    edge_pts = np.argwhere(edges)  # (row, col)
    n_edges = edge_pts.shape[0]
    print(f"Detected {n_edges} edge points (sigma={sigma}, dilate={dilate})")

    if n_edges == 0:
        raise RuntimeError(
            "No edges found. Try lowering sigma or using a different image."
        )

    if iterations is None:
        iterations = max(1000, n_edges * multiplier)
    print(
        f"Running {iterations} iterations, step={
            step}, colorize={colorize}, overlay={overlay}"
    )

    rng = np.random.default_rng(seed)

    # start from a random position (within image space)
    current = rng.random(2) * np.array([h, w], dtype=float)

    pts = np.empty((iterations, 2), dtype=float)
    cols = None
    if colorize:
        cols = np.empty((iterations, 3), dtype=float)

    # Main loop
    for i in range(iterations):
        idx = rng.integers(0, n_edges)
        attractor = edge_pts[idx].astype(float)  # row, col
        if step >= 0.999:
            # snap directly to attractor (fastest way to match edges)
            current = attractor
        else:
            current = current + (attractor - current) * step
        pts[i] = current
        if colorize:
            r = int(round(attractor[0]))
            c = int(round(attractor[1]))
            r = max(0, min(h - 1, r))
            c = max(0, min(w - 1, c))
            cols[i] = img_arr[r, c] / 255.0

    x = pts[:, 1]
    y = pts[:, 0]

    # Plotting
    # set figure size to match input pixels approximately (so saved image resolution looks similar)
    dpi = 100
    fig_w = max(6, w / dpi)
    fig_h = max(4, h / dpi)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")

    if overlay:
        ax.imshow(img_arr, origin="upper")

    # color array or white
    if colorize:
        ax.scatter(x, y, s=point_size, c=cols,
                   alpha=alpha, linewidths=0, marker=".")
    else:
        ax.scatter(x, y, s=point_size, c="white",
                   alpha=alpha, linewidths=0, marker=".")

    # background color if not overlay
    if not overlay:
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")

    # Save with the figure's facecolor (so black backgrounds are preserved)
    fig.savefig(
        output_path,
        bbox_inches="tight",
        pad_inches=0,
        facecolor=fig.get_facecolor(),
        dpi=dpi,
    )
    plt.close(fig)
    print(f"Saved -> {output_path}")


def cli():
    p = argparse.ArgumentParser(
        description="Fractalize image using edges + chaos-game style sampling"
    )
    p.add_argument("input", help="Input image file")
    p.add_argument("-o", "--output", default="fractal_out.png",
                   help="Output PNG")
    p.add_argument(
        "--sigma", type=float, default=2.0, help="Canny sigma (edge detector)"
    )
    p.add_argument(
        "--dilate", type=int, default=0, help="Dilate radius for edges (0 = none)"
    )
    p.add_argument(
        "--iters",
        type=int,
        default=None,
        help="Exact iterations (default = n_edges * multiplier)",
    )
    p.add_argument(
        "--multiplier", type=int, default=40, help="Multiplier for default iterations"
    )
    p.add_argument(
        "--step",
        type=float,
        default=0.98,
        help="Step toward attractor (0..1). Use ~0.98..1 for edge matching",
    )
    p.add_argument(
        "--point-size",
        type=float,
        default=0.4,
        help="Scatter point size (matplotlib 's')",
    )
    p.add_argument("--alpha", type=float, default=0.6, help="Point alpha")
    p.add_argument(
        "--no-color",
        dest="colorize",
        action="store_false",
        help="Don't colorize — use white points",
    )
    p.add_argument(
        "--no-overlay",
        dest="overlay",
        action="store_false",
        help="Don't overlay on the original (use black bg)",
    )
    p.add_argument("--seed", type=int, default=None, help="RNG seed")
    args = p.parse_args()

    fractalize_image(
        args.input,
        args.output,
        sigma=args.sigma,
        dilate=args.dilate,
        iterations=args.iters,
        multiplier=args.multiplier,
        step=args.step,
        point_size=args.point_size,
        alpha=args.alpha,
        colorize=args.colorize,
        overlay=args.overlay,
        seed=args.seed,
    )


if __name__ == "__main__":
    cli()
