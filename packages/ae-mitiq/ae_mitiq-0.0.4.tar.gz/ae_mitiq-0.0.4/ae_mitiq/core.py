import importlib.resources

with importlib.resources.files('ae_mitiq').joinpath('autoencoder.tflite').open('rb') as f:
    config = f.read()