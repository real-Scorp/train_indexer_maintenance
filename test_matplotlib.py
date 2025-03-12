import matplotlib
# Set the backend explicitly before importing pyplot
matplotlib.use('TkAgg')  # This should be more compatible with macOS
import matplotlib.pyplot as plt

print(f"Current backend: {matplotlib.get_backend()}")

# Create a very simple plot
plt.figure()
plt.plot([1, 2, 3, 4])
plt.title("Test Plot")
plt.savefig("test_plot.png")
print("Plot saved successfully to test_plot.png")