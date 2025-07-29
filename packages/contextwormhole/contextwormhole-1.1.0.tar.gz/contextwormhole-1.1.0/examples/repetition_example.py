#!/usr/bin/env python
# repetition_example.py - Repetition Reduction Example
# ===================================================

"""
ContextWormhole Repetition Reduction Example

This script demonstrates how different context strategies and parameters
can help reduce repetition in generated text.
"""

import time
import torch
from contextwormhole import ContextWormholeModel, ExtendedContextConfig

def main():
    """Demonstrate how to reduce repetition in generated text."""
    print("🌌 ContextWormhole Repetition Reduction Example")
    print("="*50)
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Use a small model for demonstration
    model_name = "distilgpt2"  # A smaller version of GPT-2
    print(f"\nLoading model: {model_name}")
    print("This may take a moment as the model is downloaded...")
    
    start_time = time.time()
    model = ContextWormholeModel(model_name, device=device)
    load_time = time.time() - start_time
    print(f"Model loaded in {load_time:.2f} seconds")
    
    # Demonstrate how caching strategies can help with repetition
    print("\n🔄 Caching Strategies for Reducing Repetition")
    print("="*50)
    print("Demonstrating how different caching strategies can help reduce repetition")
    
    # Create a prompt that tends to cause repetition
    repetition_prompt = "Once upon a time, there was a"
    
    print("\nPrompt that might cause repetition:")
    print(repetition_prompt)
    
    # First, show the default behavior with caching disabled
    print("\n1. No caching (shows more repetition):")
    print("-" * 50)
    
    # Use a low temperature to encourage repetition and disable caching
    default_config = ExtendedContextConfig(
        temperature=0.5,          # Lower temperature
        top_p=0.9,                # Standard top_p
        top_k=50,                 # Standard top_k
        use_cache=False,          # Disable caching to show more repetition
        verbose=True
    )
    
    default_model = ContextWormholeModel(model_name, device=device, **default_config.__dict__)
    try:
        default_result = default_model.sliding_window_generate(
            repetition_prompt,
            max_new_tokens=100,
            temperature=0.5
        )
        
        # Print the entire result
        print(f"Generated text with NO caching (notice the repetition):\n{default_result}")
    except Exception as e:
        print(f"Error with default settings: {str(e)}")
    
    # Try with standard caching enabled
    print("\n2. Standard caching (reduces repetition):")
    print("-" * 50)
    
    # Create a model with caching enabled
    diverse_config = ExtendedContextConfig(
        temperature=0.8,          # Standard temperature
        top_p=0.9,                # Standard top_p
        top_k=50,                 # Standard top_k
        use_cache=True,           # Enable caching to reduce repetition
        verbose=True
    )
    
    diverse_model = ContextWormholeModel(model_name, device=device, **diverse_config.__dict__)
    try:
        diverse_result = diverse_model.sliding_window_generate(
            repetition_prompt,
            max_new_tokens=100,
            temperature=0.8
        )
        
        # Print the entire result
        print(f"Generated text with standard caching (less repetition):\n{diverse_result}")
    except Exception as e:
        print(f"Error with higher temperature and diversity: {str(e)}")
    
    # Try with attention sink strategy and optimized caching
    print("\n3. Attention Sink with optimized caching (best for reducing repetition):")
    print("-" * 50)
    
    # Create a model with attention sink strategy and caching
    sink_config = ExtendedContextConfig(
        sink_tokens=16,           # More sink tokens
        temperature=0.8,          # Standard temperature
        use_cache=True,           # Enable caching
        window_size=256,          # Smaller window size for better caching
        overlap=64,               # Larger overlap for better context
        verbose=True
    )
    
    sink_model = ContextWormholeModel(model_name, device=device, **sink_config.__dict__)
    try:
        sink_result = sink_model.attention_sink_generate(
            repetition_prompt,
            max_new_tokens=100,
            temperature=0.8
        )
        
        # Print the entire result
        print(f"Generated text with attention sink and optimized caching (minimal repetition):\n{sink_result}")
    except Exception as e:
        print(f"Error with attention sink strategy: {str(e)}")
    
    print("\n✅ Example completed!")
    print("\nThis example demonstrates how different caching strategies")
    print("can help reduce repetition in generated text without requiring")
    print("additional parameters like repetition_penalty.")
    print("\nFor more examples and documentation, visit:")
    print("https://github.com/contextwormhole/contextwormhole")

if __name__ == "__main__":
    main()