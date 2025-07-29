#!/usr/bin/env python
# basic_usage.py - Basic Usage Example
# ====================================

"""
ContextWormhole Basic Usage Example

This script demonstrates the basic usage of ContextWormhole
with different strategies for handling long context.
"""

from contextwormhole import ContextWormholeModel, create_extended_model

def main():
    """Demonstrate basic usage of ContextWormhole."""
    print("🌌 ContextWormhole Basic Usage Example")
    print("="*50)
    
    # Note: In real usage, you'd use actual model paths like:
    # model = ContextWormholeModel("microsoft/DialoGPT-medium")
    print("To use ContextWormhole with a real model:")
    print("model = ContextWormholeModel('gpt2')")
    
    # Simulate long document
    long_document = """
    This is a very long document about artificial intelligence
    that exceeds the normal context length of most models...
    """ + "Content continues for many paragraphs... " * 50
    
    print(f"\nDocument length: ~{len(long_document)} characters")
    
    # Demo different strategies
    strategies = [
        ("sliding_window", "Best for documents and articles"),
        ("hierarchical", "Best for research papers with sections"),
        ("attention_sink", "Best for conversations"),
    ]
    
    for strategy, description in strategies:
        print(f"\n📝 {strategy.replace('_', ' ').title()} Strategy")
        print(f"   {description}")
        print(f"   result = model.{strategy}_generate(document, max_new_tokens=100)")
    
    print("\n✅ Example completed!")
    print("\nFor more examples and documentation, visit:")
    print("https://github.com/contextwormhole/contextwormhole")

if __name__ == "__main__":
    main()