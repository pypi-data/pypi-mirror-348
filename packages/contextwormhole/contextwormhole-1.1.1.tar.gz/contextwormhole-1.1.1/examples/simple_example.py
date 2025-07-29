#!/usr/bin/env python
# simple_example.py - Simple Example
# =================================

"""
ContextWormhole Simple Example

This script demonstrates a basic usage of ContextWormhole
with a simple prompt.
"""

import torch
from contextwormhole import ContextWormholeModel

def main():
    """Demonstrate basic usage of ContextWormhole."""
    print("🌌 ContextWormhole Simple Example")
    print("="*50)
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Use a small model for demonstration
    model_name = "distilgpt2"
    print(f"\nLoading model: {model_name}")
    print("This may take a moment as the model is downloaded...")
    
    # Create the model
    model = ContextWormholeModel(model_name, device=device)
    print("Model loaded successfully!")
    
    # Create a simple prompt
    prompt = "Once upon a time, there was a"
    
    print(f"\nPrompt: \"{prompt}\"")
    
    # Generate text using the sliding window strategy
    print("\nGenerating text...")
    result = model.sliding_window_generate(prompt, max_new_tokens=20, temperature=0.8)
    
    # Print the result
    print("\nGenerated text:")
    print("-" * 40)
    print(result)
    print("-" * 40)
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main()