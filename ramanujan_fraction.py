
import numpy as np
import matplotlib.pyplot as plt

def rogers_ramanujan_fraction(q, n):
    """Calculates the Rogers-Ramanujan continued fraction to a depth n."""
    if n == 0:
        return 1
    else:
        return 1 + (q**n) / rogers_ramanujan_fraction(q, n - 1)

def ramanujan_expression(q, n):
    """Calculates the full Ramanujan expression."""
    return q**(1/5) / rogers_ramanujan_fraction(q, n)

# Generate q values
q_values = np.linspace(0.01, 1, 100)

# Calculate the expression for each q
y_values = [ramanujan_expression(q, 10) for q in q_values]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(q_values, y_values)
plt.title("Ramanujan's Continued Fraction")
plt.xlabel("q")
plt.ylabel("R(q)")
plt.grid(True)
plt.savefig("ramanujan_fraction.png")

print("Plot saved as ramanujan_fraction.png")
