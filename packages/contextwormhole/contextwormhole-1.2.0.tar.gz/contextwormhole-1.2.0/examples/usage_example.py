#!/usr/bin/env python
# usage_example.py - Complete Usage Example
# =========================================

"""
ContextWormhole Complete Usage Example

This script demonstrates how to use all three context extension strategies
in ContextWormhole with properly defined input variables.
"""

import torch
from contextwormhole import ContextWormholeModel

def main():
    """Demonstrate complete usage of ContextWormhole."""
    print("🌌 ContextWormhole Complete Usage Example")
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
    
    # 1. Sliding Window Example (best for documents and articles)
    print("\n\n1. SLIDING WINDOW STRATEGY")
    print("="*30)
    
    # Define a long document
    long_document = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    as opposed to intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, 
    which refers to any system that perceives its environment and takes actions 
    that maximize its chance of achieving its goals.
    """ + "The field of AI research continues to expand rapidly. " * 20
    
    print(f"Document length: ~{len(long_document)} characters")
    print("\nGenerating with sliding window strategy...")
    
    # Generate using sliding window
    result1 = model.sliding_window_generate(
        long_document, 
        max_new_tokens=50,
        temperature=0.8
    )
    
    print("\nGenerated text (sliding window):")
    print("-" * 40)
    print(result1)
    print("-" * 40)
    
    # 2. Hierarchical Example (best for research papers with sections)
    print("\n\n2. HIERARCHICAL STRATEGY")
    print("="*30)
    
    # Define a research paper with sections
    research_paper = """
    # Abstract
    
    This paper explores the applications of transformer models in natural language processing.
    
    # Introduction
    
    Transformer models have revolutionized the field of NLP since their introduction.
    
    # Methodology
    
    We compare several transformer architectures on benchmark tasks.
    
    # Results
    
    Our experiments show significant improvements over baseline models.
    
    # Conclusion
    
    Transformer models continue to push the state of the art in NLP tasks.
    """ + "Further research is needed to fully understand their capabilities. " * 15
    
    print(f"Research paper length: ~{len(research_paper)} characters")
    print("\nGenerating with hierarchical strategy...")
    
    # Generate using hierarchical approach
    result2 = model.hierarchical_generate(
        research_paper, 
        max_new_tokens=50,
        temperature=0.8
    )
    
    print("\nGenerated text (hierarchical):")
    print("-" * 40)
    print(result2)
    print("-" * 40)
    
    # 3. Attention Sink Example (best for conversations)
    print("\n\n3. ATTENTION SINK STRATEGY")
    print("="*30)
    
    # Define a conversation history
    conversation_history = """
    User: Hello, how are you today?
    Assistant: I'm doing well, thank you for asking! How can I help you?
    User: I'm interested in learning about artificial intelligence.
    Assistant: That's a great topic! AI is a broad field that includes machine learning, neural networks, and more.
    User: Can you tell me more about neural networks?
    Assistant: Neural networks are computing systems inspired by the biological neural networks in animal brains.
    User: How do they work?
    """ + "Assistant: Neural networks consist of layers of interconnected nodes. " * 10
    
    print(f"Conversation length: ~{len(conversation_history)} characters")
    print("\nGenerating with attention sink strategy...")
    
    # Generate using attention sink
    result3 = model.attention_sink_generate(
        conversation_history, 
        max_new_tokens=50,
        temperature=0.8
    )
    
    print("\nGenerated text (attention sink):")
    print("-" * 40)
    print(result3)
    print("-" * 40)
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main()