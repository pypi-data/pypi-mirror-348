from ai_edge_litert.interpreter import Interpreter
import numpy as np
import os

class Autoencoder():
    def __init__(self):
        module_dir = os.path.dirname(__file__)
        model_path = os.path.join(module_dir, "autoencoder.tflite")
        self.model = Interpreter(model_path)
        self.input_detail = self.model.get_input_details()[0]
        self.output_detail = self.model.get_output_details()[0]

    def mitigation(self, input_data):
        self.model.allocate_tensors()
        input_data = np.array(np.reshape(input_data, self.input_detail["shape"]), dtype="float32")
        self.model.set_tensor(self.input_detail["index"], input_data)
        self.model.invoke()
        return self.model.get_tensor(self.output_detail["index"]).flatten()
