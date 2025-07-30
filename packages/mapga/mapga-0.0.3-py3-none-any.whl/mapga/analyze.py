import tensorflow as tf
from typing import Tuple
import math
import numpy as np
import keras
import matplotlib.pyplot as plt
import random
from keras.models import load_model

class ModelAnalyzer:
    def __init__(self, model):
        self._model = model
        # print(self._model.input_shape)
        # model.summary()
        self._model.build(input_shape=self._model.input_shape)
        self._model_layers = [layer for layer in self._model.layers]

    def get_maccs_per_layer(self, layer):
        if isinstance(layer, keras.layers.Dense):
            return layer.count_params()
        
        if isinstance(layer, keras.layers.Conv2D):
            _, h_out, w_out, c_out = layer.output_shape
            c_in = layer.input_shape[-1]
            # MACCS = h_out x w_out x c_out x kernel_size x kernel_size x c_in
            return h_out*w_out*c_out*math.prod(layer.kernel_size)*c_in
        
        if isinstance(layer, keras.layers.SeparableConv2D):
            _, h_in, w_in, c_in = layer.input_shape
            x = np.random.rand(1, h_in, w_in, c_in)
            depth = keras.Sequential(keras.layers.DepthwiseConv2D(kernel_size=layer.kernel_size, padding=layer.padding))
            z = depth(x)
            pointwise = keras.Sequential(keras.layers.Conv2D(filters = layer.filters, kernel_size=1, padding=layer.padding))
            pointwise(z)
            return self.get_maccs_per_layer(depth) + self.get_maccs_per_layer(pointwise)
        
        if isinstance(layer, keras.Sequential):
            _, h_out, w_out, c_out = layer.output_shape
            c_in = layer.input_shape[-1]
            # MACCs=output_height×output_width×num_filters×kernel_height×kernel_width×input_channels
            layer = layer.layers[0]
            if isinstance(layer, keras.layers.DepthwiseConv2D):
                # print("Depthwise: ", h_out*w_out*math.prod(layer.kernel_size)*c_in)
                return h_out*w_out*math.prod(layer.kernel_size)*c_in
            else:
                # print("Pointwise: ", h_out*w_out*c_out*math.prod(layer.kernel_size)*c_in)
                return h_out*w_out*c_out*math.prod(layer.kernel_size)*c_in
        else:
            return 0

    def inspect(self) -> dict:
        params = {}
        for i, layer in enumerate(self._model_layers):
            params[i] = {
                'name': layer.name,
                'n_params': layer.count_params(),
                'input_shape': layer.input_shape,
                'output_shape': layer.output_shape,
                'activations': math.prod(layer.output_shape[1:]),
                'maccs': self.get_maccs_per_layer(layer)
            }
        return params
    
    def summary(self):
        params = self.inspect()
        print(f"{'Index':<10}{'Name':<20}{'MACCs':<20}{'# of Parameters':<20}{'Output_shape':<25}{'Activations':<20}")
        print("=" * 110)
        for name in params:
            output_shape = params[name]['output_shape']
            print(f"{name:<10}{params[name]['name']:<20}{params[name]['maccs']:<20}{params[name]['n_params']:<20}{str(output_shape):<25}{params[name]['activations']:<20}")
    
    def plot_summary(self, scale_factor: float = 1.0):
        inspection = self.inspect()
        maccs = []
        activations = []
        params = []
        for name in inspection:
            maccs.append(inspection[name]['maccs'])
            activations.append(inspection[name]['activations'])
            params.append(inspection[name]['n_params'])
        # Sample data
        layers = np.arange(1, len(self._model_layers) + 1)  # Layer indexes from 1 to 5
        bar_width = 0.2  # Width of each bar
        x = np.arange(len(layers))

        # Data for the 3 bars per layer
        maccs = np.array(maccs) / scale_factor
        activations = np.array(activations) / scale_factor
        params = np.array(params) / scale_factor

        for metrics, label in zip([maccs, activations, params], ['Maccs', 'Activations', 'Parameters']):
            plt.bar(x, metrics, width=bar_width, label=label)

            # Set the x-ticks and labels
            plt.xticks(x, layers)

            # Adding labels and title
            plt.xlabel('Layer Index')
            if scale_factor == 1.0:
                plt.ylabel(f'Number')
            else:
                plt.ylabel(f'Number * {scale_factor:.1e}')
            plt.title('Bar plot visualization of inspection summary')
            plt.legend()

            # Show the plot
            plt.tight_layout()
            plt.show()