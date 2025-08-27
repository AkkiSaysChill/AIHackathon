🎨 Image Fractalizer using Chaos Game

Turn any image into artistic fractals by sampling its edges and re-drawing them using a Chaos Game process.
This project combines image processing, fractals, and creative coding to transform photos into sketches, outlines, and abstract pointillist art.

✨ Features

🖼 Edge Detection: Uses Canny edge detection to find outlines in an image.

🔀 Chaos Game Iterations: Randomly jumps towards detected edge points to generate fractal-like patterns.

🎨 Color Modes:

White outlines (sketch mode)

Colored edges (sampled from original image)

Psychedelic gradients (optional extension)

🔧 Customizable Parameters:

--step controls fractal diffusion (0.5 = cloudy, 1.0 = edge-locked).

--iters defines how many points are drawn.

--point-size controls dot size.

--overlay places fractals over the original image.

--dilate thickens edges.


⚡ How It Works

Input Image → Load your chosen image.

Edge Detection → Find outlines using the Canny algorithm.

Chaos Game → Start at a random point, repeatedly jump towards random edge pixels (factor = --step).

Scatter Plot → Each jump leaves a dot, forming fractalized edges.

Output → Save a new image with fractal art.


📊 Parameters

| Flag           | Default | Description                                                 |
| -------------- | ------- | ----------------------------------------------------------- |
| `--sigma`      | `2.0`   | Edge detection smoothing                                    |
| `--dilate`     | `0`     | Expand edges for thicker outlines                           |
| `--iters`      | `None`  | Number of Chaos Game steps (default = `edges * multiplier`) |
| `--multiplier` | `40`    | Iterations per edge pixel                                   |
| `--step`       | `0.98`  | Jump factor (1.0 = edges, <1.0 = fractal diffusion)         |
| `--point-size` | `0.4`   | Scatter point size                                          |
| `--alpha`      | `0.6`   | Dot transparency                                            |
| `--no-overlay` | off     | Hide original photo (black background)                      |
| `--no-color`   | off     | White dots only                                             |



## 🧮 Mathematics Behind the Project

This project is not just art — it’s math in action!  

### 1. Edge Detection (Canny Algorithm)
- Uses **gradient magnitude** from calculus:  
  \[
  G = \sqrt{\left(\frac{\partial I}{\partial x}\right)^2 + \left(\frac{\partial I}{\partial y}\right)^2}
  \]  
- Finds sharp intensity changes → outlines of the image.

### 2. Chaos Game (Fractal Generation)
- Start at a point \( P_0 \).  
- Pick a random edge pixel \( A \).  
- Move towards it by factor \( s \) (`--step`):  
  \[
  P_{n+1} = P_n + s \cdot (A - P_n)
  \]  
- Repeat → points cluster along fractal-like structures.  
- When \( s = 1.0 \), points fall exactly on edges (sketch mode).  
- When \( s < 1.0 \), points diffuse inward → cloud-like fractals.  

### 3. Probability & Randomness
- Each edge pixel has equal chance to be chosen.  
- Over many iterations, patterns emerge due to the **law of large numbers**.  

### 4. Geometry & Scaling
- The fractal patterns show **self-similarity**: zoomed-in parts resemble the whole.  
- Point sizes, densities, and iteration counts act like scaling factors.

👉 This project demonstrates how **calculus (gradients), geometry (iterations), probability (random jumps), and fractals (self-similarity)** combine to turn an ordinary picture into mathematical art.

