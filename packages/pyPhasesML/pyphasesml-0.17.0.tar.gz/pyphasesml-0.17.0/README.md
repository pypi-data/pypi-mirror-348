# Machine Learning Extension for pyPhases

This Extension adds:
- an Exporter for `PyTorch` and `TensorFlow` Models.
- an Modelmanager that can handle `PyTorch` and `TensorFlow` Models


## Setup

- add pyPhasesML to your dependencies or run `pip install -U pyPhasesML`
- add `pyPhasesML` to your plugins in the main project config f.e: in your `project.yaml`
```yaml
name: bumpDetector
namespace: ibmt.tud

# load machine learning plugin
plugins:
  - pyPhasesML
```
- you do not need to add the ModelExporter manually


## Getting startet


### Minimal Example

For a complete minimal example see, with loading data, training and evaluation see:
https://gitlab.com/tud.ibmt.public/pyphases/pyphasesml-example-bumpdetector


## Adding required config values

These values can be changed in your config. The default values are shown here:

```yaml

modelPath: models/mymodels

# the name of the model (also defines the path: models/MyCnn/MyCnn.py)
modelName: CNNPytorch

# the model config for a specific model
model:
    kernelSize: 3

alwaysIgnoreClassIndex: null
inputShape: [16, 50]
oneHotDecoded: False

trainingParameter:
  useEventScorer: false
  stopAfterNotImproving: false
  maxEpochs: false
  batchSize: 32
  validationEvery: false
  optimizer: false
  batchSizeValidation: 32
  learningRate: 0.001
  learningRateDecay: 0.001
  validationMetrics: ["acc", "kappa"]

classification:
  type: classification
  classNames: [A, B]
  classWeights: [0.6, 0.4]
```

## Adding a PyTorch Model `CNNPytorch`

Create a class that is compatible with your `modelPath` and `modelname`. So in this example, we need a class `CNNPytorch` in the path `models/mymodels/CNNPytorch.py` relative to your root. 

This class is required to:
- inherit from `ModelTorchAdapter`:
- populate the `self.model` with a valid PyTorch-Model, in the `define` method
- return a valid loss function in the method `getLossFunction`

```python
import torch.nn as nn

from pyPhasesML.adapter.ModelTorchAdapter import ModelTorchAdapter

class CNNPytorch(ModelTorchAdapter):
    def define(self):
        length, channelCount = self.inputShape
        numClasses = self.config.numClasses

        self.model = nn.Conv1d(
            in_channels=channelCount, 
            out_channels=self.config.numClasses,
            kernel_size=self.getOption("kernelSize"),
        )

    def getLossFunction(self):
        return torch.nn.MultiLabelSoftMarginLoss(reduction="mean", weight=self.weightTensors)

```

### Load the model

In a phase you can simply use the `ModelManager` to get the Model and `registerData` to save the state. There is no dependency on `pyTorch` or `TensorFlow` in this example, so you swap your models dynamicly depending on your environment:

```php
import numpy as np
from pathlib import Path

from pyPhases import Phase
from pyPhasesML import DatasetWrapXY, ModelManager, TrainingSet


class TestModel(Phase):
    def main(self):
        # loads the model depending on modelPath and modelName
        model = ModelManager.getModel()
        
        input = np.randn(20, 16, 50)        
        output = model(input)
        # save the model state
        self.project.registerData("modelState", model)
```
