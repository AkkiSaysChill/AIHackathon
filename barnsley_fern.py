
import numpy as np
import matplotlib.pyplot as plt

def f1(x, y):
    return (0.0, 0.16 * y)

def f2(x, y):
    return (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6)

def f3(x, y):
    return (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6)

def f4(x, y):
    return (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)

def generate_fern(n_points):
    x, y = [0], [0]
    current_x, current_y = 0, 0

    for _ in range(n_points):
        p = np.random.random()
        if p < 0.01:
            current_x, current_y = f1(current_x, current_y)
        elif p < 0.86:
            current_x, current_y = f2(current_x, current_y)
        elif p < 0.93:
            current_x, current_y = f3(current_x, current_y)
        else:
            current_x, current_y = f4(current_x, current_y)
        
        x.append(current_x)
        y.append(current_y)
    
    return x, y

if __name__ == '__main__':
    n_points = 100000
    x, y = generate_fern(n_points)

    plt.figure(figsize=(6, 10))
    plt.scatter(x, y, s=0.2, c='g')
    plt.title("Barnsley Fern")
    plt.axis('off')
    plt.savefig("barnsley_fern.png")

    print("Barnsley Fern saved as barnsley_fern.png")
