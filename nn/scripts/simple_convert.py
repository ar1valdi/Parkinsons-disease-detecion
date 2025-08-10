import torch
import torch.nn as nn

def create_model():
    """Hardcoded architecture for convertion"""
    model = nn.Sequential(
        nn.Linear(32, 10),
        nn.LeakyReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(10, 1),
        nn.Sigmoid()
    )
    return model

def main():
    import os
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.dirname(script_dir)
    
    state_dict = torch.load(os.path.join(model_dir, "model.pt"), map_location='cpu')
    model = create_model()
    model.load_state_dict(state_dict)
    model.eval()
    dummy_input = torch.zeros(1, 32)
    
    torch.onnx.export(
        model,
        dummy_input,
        os.path.join(model_dir, "model.onnx"),
        export_params=True,
        opset_version=11,  # Use opset 11 for better web compatibility
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )

if __name__ == "__main__":
    main()
