import importlib.resources

with importlib.resources.files('ae_mitiq').joinpath('autoencoder.tflite').open('r') as f:
    config = f.read()