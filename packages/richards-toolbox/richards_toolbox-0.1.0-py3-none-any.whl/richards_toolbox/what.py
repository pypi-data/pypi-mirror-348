class IterableProcessor:

    @staticmethod
    def can(obj, **kwarg):
        from collections.abc import Iterable
        return isinstance(obj, Iterable)
    
    @staticmethod
    def describe(obj, **kwarg):
        import pandas as pd
        x = pd.Series(obj)
        return x

class DoubleIterableProcessor:

    @staticmethod
    def can(obj, **kwarg):
        return IterableProcessor.can(obj) and IterableProcessor.can(next(iter(obj)))
    
    @staticmethod
    def describe(obj, **kwarg):
        import pandas as pd
        x = pd.DataFrame(obj)
        return x


class PytorchModuleProcessor:

    @staticmethod
    def can(obj, **kwargs):
        import torch.nn as nn
        return issubclass(type(obj), nn.Module)
    
    @staticmethod
    def describe(obj, **kwargs):
        import torch
        print("Warn: Using simple Pytorch processor, please use kwarg 'input_size' or 'input_data' for rich information")
        print(obj)


class PyTorchRichModuleProcessor:
    
    @staticmethod
    def can(obj, **kwargs):
        import torch.nn as nn
        return issubclass(type(obj), nn.Module) and "input_size" in kwargs
    
    @staticmethod
    def describe(obj, **kwargs):
        from torchinfo import summary
        return summary(obj, **kwargs)


class ONNXRuntimeInferenceSession:

    @staticmethod
    def can(obj, **kwargs):
        return type(obj).__qualname__ == "InferenceSession"
    
    @staticmethod
    def describe(obj, **kwargs):
        
        print("InferenceSession details")
        print("Inputs:")
        for node in obj.get_inputs():
            print(f"{node.name}: {node.shape} of {node.type}")
        
        print("Outputs:")
        for node in obj.get_outputs():
            print(f"{node.name}: {node.shape} of {node.type}")


class DictProcessor:

    @staticmethod
    def can(obj, **kwargs):
        return type(obj) == dict
    
    @staticmethod
    def describe(obj, **kwargs):
        from pprint import pprint
        import io
        stream = io.StringIO()
        pprint(obj, stream=stream)
        s = stream.getvalue()
        stream.close()
        return s


PROCESSORS = [
    ONNXRuntimeInferenceSession,
    PyTorchRichModuleProcessor,
    PytorchModuleProcessor,
    DictProcessor,
    DoubleIterableProcessor,
    IterableProcessor
]


def what(obj, *args, **kwargs):

    results = []
    
    for obj in [obj, *args]:
        print(f"Processing type {type(obj)}")
        for processor in PROCESSORS:
            if processor.can(obj, **kwargs):
                print(f"Using processor: {processor}")
                results += [processor.describe(obj, **kwargs)]
                break
        else:
            print(f"Couldn't figure out what {obj} is")
            results += [obj]
    
    if len(results) == 1:
        return results[0]
    else:
        return tuple(results)


if __name__ == "__main__":
    print(what([1, 2, 3]))
    print(what([[1, 2, 3], [4, 7, 8]]))

    from torchvision.models import resnet50, ResNet50_Weights
    print(what(resnet50(weights=ResNet50_Weights.IMAGENET1K_V1), input_size=(1, 3, 224, 224)))

    print(*what([1, 2, 3], [1, 2, 3]))

    print(what([1, 2, 3]))