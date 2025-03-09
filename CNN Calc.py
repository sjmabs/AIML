# Originally created by another student but updated to include extra caluclations

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


class CNNCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("CNN Multi-Layer Calculator")

        # Labels
        tk.Label(root, text="Input Size (Width/Height):").grid(row=0, column=0)
        self.input_size_entry = tk.Entry(root)
        self.input_size_entry.grid(row=0, column=1)
        self.input_size_entry.insert(0, "9")  # Default input size

        tk.Label(root, text="Input Channels:").grid(row=1, column=0)
        self.input_channels_entry = tk.Entry(root)
        self.input_channels_entry.grid(row=1, column=1)
        self.input_channels_entry.insert(0, "3")  # Default 3 channels (RGB)

        # label for output layer
        tk.Label(root, text="Neurons in fully connected output layer:").grid(row=2, column=0)
        self.output_layer_entry = tk.Entry(root)
        self.output_layer_entry.grid(row=2, column=1)
        self.output_layer_entry.insert(0, "10")  # Default 10 output nodes

        # Frame for dynamically adding/removing layers
        self.layer_frame = tk.Frame(root)
        self.layer_frame.grid(row=3, columnspan=2)

        self.layers = []
        self.add_layer()

        # Buttons
        tk.Button(root, text="Add Layer", command=self.add_layer).grid(row=4, column=1)
        tk.Button(root, text="Remove Layer", command=self.remove_layer).grid(row=4, column=2)
        tk.Button(root, text="Calculate", command=self.calculate).grid(row=4, column=0)

    def add_layer(self):
        """Add a new convolutional layer input row."""
        layer_index = len(self.layers)

        tk.Label(self.layer_frame, text=f"Layer {layer_index + 1}: Kernel Size").grid(row=layer_index, column=0)
        kernel_entry = tk.Entry(self.layer_frame)
        kernel_entry.grid(row=layer_index, column=1)
        kernel_entry.insert(0, "4")  # Default kernel size

        tk.Label(self.layer_frame, text="Num Filters").grid(row=layer_index, column=2)
        filters_entry = tk.Entry(self.layer_frame)
        filters_entry.grid(row=layer_index, column=3)
        filters_entry.insert(0, "10")  # Default filters

        tk.Label(self.layer_frame, text="Stride").grid(row=layer_index, column=4)
        stride_entry = tk.Entry(self.layer_frame)
        stride_entry.grid(row=layer_index, column=5)
        stride_entry.insert(0, "1")  # Default stride

        tk.Label(self.layer_frame, text="Padding").grid(row=layer_index, column=6)
        padding_entry = tk.Entry(self.layer_frame)
        padding_entry.grid(row=layer_index, column=7)
        padding_entry.insert(0, "0")  # Default padding 0

        self.layers.append((kernel_entry, filters_entry, stride_entry, padding_entry))

    def remove_layer(self):
        """Remove the last convolutional layer from the input fields."""
        if self.layers:
            layer_index = len(self.layers) - 1
            for widget in self.layer_frame.grid_slaves():
                if int(widget.grid_info()["row"]) == layer_index:
                    widget.destroy()
            self.layers.pop()
        else:
            messagebox.showwarning("Warning", "No layers to remove!")

    def calculate(self):
        """Calculate neurons and weights for each layer and plot results."""
        try:
            input_size = int(self.input_size_entry.get())
            input_channels = int(self.input_channels_entry.get())
            output_layer_size = int(self.output_layer_entry.get())

            neurons_per_layer = []
            weights_per_layer = []
            layer_names = []

            for i, (kernel_entry, filters_entry, stride_entry, padding_entry) in enumerate(self.layers):
                kernel_size = int(kernel_entry.get())
                num_filters = int(filters_entry.get())
                stride = int(stride_entry.get())
                padding = int(padding_entry.get())

                # Calculate output size
                output_size = ((input_size - kernel_size + 2 * padding) // stride) + 1
                if output_size <= 0:
                    messagebox.showerror("Error", f"Invalid dimensions at Layer {i + 1}")
                    return

                # Calculate neurons and weights (including bias)
                num_neurons = output_size * output_size * num_filters
                total_weights = ((kernel_size ** 2) * input_channels * num_filters) + num_filters  # Bias added

                # Store results
                neurons_per_layer.append(num_neurons)
                weights_per_layer.append(total_weights)
                layer_names.append(f"Layer {i + 1}")

                # Update input size and channels for the next layer
                input_size = output_size
                input_channels = num_filters

            # final output layer weights
            fully_connected_output_layer_weights = neurons_per_layer[-1] * output_layer_size + output_layer_size

            # calculate all weights in whole network
            combined_weights = fully_connected_output_layer_weights
            for weight in weights_per_layer:
                combined_weights += weight


            # Display results
            messagebox.showinfo("Results",
                                f"Neurons per convolutional layer: {neurons_per_layer}\nWeights per convolutional layer (including biases): {weights_per_layer}"
                                f"\nWeights in fully connected output layer: {fully_connected_output_layer_weights}"
                                f"\nTotal combined weights in whole network: {combined_weights}")

            # Plot results
            self.plot_results(layer_names, neurons_per_layer, weights_per_layer)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def plot_results(self, layers, neurons, weights):
        """Plot neurons and weights per layer."""
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Layer')
        ax1.set_ylabel('Neurons', color='tab:blue')
        ax1.bar(layers, neurons, color='tab:blue', alpha=0.6, label="Neurons")
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Weights (incl. Bias)', color='tab:red')
        ax2.plot(layers, weights, color='tab:red', marker='o', label="Weights (incl. Bias)")
        ax2.tick_params(axis='y', labelcolor='tab:red')

        plt.title("CNN Neurons and Weights (with Bias) per Layer")
        fig.tight_layout()
        plt.show()


# Run GUI
root = tk.Tk()
app = CNNCalculator(root)
root.mainloop()
