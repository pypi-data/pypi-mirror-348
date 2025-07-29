#!/usr/bin/env python
# real_model_example.py - Long Context Example
# ===========================================

"""
ContextWormhole Long Context Example

This script demonstrates handling long context (8000 tokens)
with ContextWormhole using different strategies.
"""

import time
import torch
import random
from contextwormhole import ContextWormholeModel, ExtendedContextConfig

# Function to generate a long essay prompt
def generate_long_essay_prompt(target_length=8000):
    """Generate a long essay prompt with approximately target_length tokens."""
    
    # Essay topics for the long context
    topics = [
        "The Evolution of Artificial Intelligence",
        "Climate Change and Global Policy",
        "The Future of Space Exploration",
        "Ethical Considerations in Biotechnology",
        "The Digital Revolution and Society",
        "Sustainable Development Goals",
        "The History of Economic Thought",
        "Philosophical Perspectives on Consciousness",
        "The Role of Art in Society",
        "Global Health Challenges"
    ]
    
    # Subtopics for each main topic
    subtopics = {
        topic: [f"Aspect {i+1} of {topic}" for i in range(20)]
        for topic in topics
    }
    
    # Generate a long essay prompt
    selected_topic = random.choice(topics)
    selected_subtopics = subtopics[selected_topic]
    
    prompt = f"# Essay on {selected_topic}\n\n"
    prompt += "## Introduction\n\n"
    prompt += f"Write a comprehensive essay on {selected_topic}. "
    prompt += "This essay should cover the historical background, current state, "
    prompt += "future prospects, and critical analysis of various perspectives. "
    prompt += "The essay should be well-structured, thoroughly researched, and academically rigorous.\n\n"
    
    # Add sections for each subtopic
    for i, subtopic in enumerate(selected_subtopics):
        prompt += f"## Section {i+1}: {subtopic}\n\n"
        prompt += f"In this section, explore {subtopic} in detail. "
        prompt += "Consider the following aspects:\n\n"
        
        # Add bullet points with specific questions
        for j in range(5):
            prompt += f"- Question {j+1} about {subtopic}\n"
        
        prompt += "\nProvide examples, cite relevant research, and analyze implications.\n\n"
    
    # Add conclusion section
    prompt += "## Conclusion\n\n"
    prompt += f"Summarize the key points discussed throughout the essay on {selected_topic}. "
    prompt += "Reflect on the significance of this topic for future research and practical applications. "
    prompt += "Offer final thoughts and recommendations.\n\n"
    
    # Add formatting instructions
    prompt += "## Formatting Guidelines\n\n"
    prompt += "- Use clear headings and subheadings\n"
    prompt += "- Include proper citations\n"
    prompt += "- Maintain academic tone and style\n"
    prompt += "- Ensure logical flow between sections\n\n"
    
    # Add a starting point for the essay
    prompt += "Begin writing the essay here:\n\n"
    
    # Repeat content to reach target length if needed
    while len(prompt.split()) < target_length:
        prompt += f"\nAdditional notes on {random.choice(selected_subtopics)}:\n"
        for _ in range(10):
            prompt += f"- Consider the relationship between {random.choice(selected_subtopics)} and {random.choice(selected_subtopics)}.\n"
    
    return prompt, selected_topic

def main():
    """Demonstrate handling long context with ContextWormhole."""
    print("🌌 ContextWormhole Long Context Example")
    print("="*50)
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Use a small model for demonstration
    model_name = "distilgpt2"  # A smaller version of GPT-2
    print(f"\nLoading model: {model_name}")
    print("This may take a moment as the model is downloaded...")
    
    # Create a custom configuration with larger context settings
    config = ExtendedContextConfig(
        max_training_length=8000,  # Set to 8000 as requested
        window_size=1024,          # Larger window size
        overlap=128,               # Significant overlap
        chunk_size=512,            # Chunk size for hierarchical processing
        summary_length=128,        # Length of summaries
        sink_tokens=16,            # More sink tokens
        temperature=0.8,           # Slightly higher temperature for creativity
        verbose=True               # Show verbose output
    )
    
    start_time = time.time()
    model = ContextWormholeModel(model_name, device=device, **config.__dict__)
    load_time = time.time() - start_time
    print(f"Model loaded in {load_time:.2f} seconds")
    
    # Generate a long essay prompt
    print("\nGenerating a long essay prompt (approximately 8000 tokens)...")
    prompt, topic = generate_long_essay_prompt(8000)
    token_count = len(prompt.split())
    print(f"Generated prompt with approximately {token_count} tokens on: {topic}")
    
    # Try different strategies
    strategies = [
        ("sliding_window", "Sliding Window Strategy"),
        ("hierarchical", "Hierarchical Context Strategy"),
        ("attention_sink", "Attention Sink Strategy"),
    ]
    
    for method, name in strategies:
        print(f"\n📝 {name}")
        print("-" * 60)
        print(f"Processing approximately {token_count} tokens...")
        
        start_time = time.time()
        
        # Call the appropriate method based on the strategy
        if method == "sliding_window":
            result = model.sliding_window_generate(prompt, max_new_tokens=200, temperature=0.8)
        elif method == "hierarchical":
            result = model.hierarchical_generate(prompt, max_new_tokens=200, temperature=0.8)
        elif method == "attention_sink":
            result = model.attention_sink_generate(prompt, max_new_tokens=200, temperature=0.8)
        
        gen_time = time.time() - start_time
        
        # Print the result
        print(f"Generation time: {gen_time:.2f} seconds")
        
        # Show the end of the prompt and the generated text
        prompt_end = "Begin writing the essay here:"
        result_start = result.find(prompt_end)
        
        if result_start > 0:
            # Show what comes after the prompt
            new_content = result[result_start + len(prompt_end):]
            print("\nPrompt ending with: ")
            print(f"...{prompt_end}")
            print("\nGenerated essay beginning:")
            print("-" * 60)
            if new_content.strip():
                print(new_content.strip())
            else:
                print("(No new content generated beyond the prompt)")
        else:
            # Fallback to showing the end of the result
            print("\nEnd of generated text:")
            print("-" * 60)
            print(result[-500:])  # Show the last 500 characters
        
        print("-" * 60)
    
    # Demonstrate how context length strategies can help with repetition
    print("\n🔄 Context Length Strategies for Reducing Repetition")
    print("="*50)
    print("Demonstrating how different context strategies can help with repetition")
    
    # Create a prompt that tends to cause repetition
    repetition_prompt = """
    List the benefits of artificial intelligence in modern society:
    1. Improved efficiency in various industries
    2. Enhanced medical diagnostics and treatment
    3. """
    
    print("\nPrompt that might cause repetition:")
    print(repetition_prompt)
    
    # First, show the default behavior (which might repeat)
    print("\n1. Default behavior (may show repetition):")
    print("-" * 50)
    
    # Use a low temperature to encourage repetition
    default_config = ExtendedContextConfig(
        temperature=0.5,          # Lower temperature
        top_p=0.9,                # Standard top_p
        top_k=50,                 # Standard top_k
        verbose=True
    )
    
    default_model = ContextWormholeModel(model_name, device=device, **default_config.__dict__)
    default_result = default_model.sliding_window_generate(
        repetition_prompt,
        max_new_tokens=100,
        temperature=0.5
    )
    
    # Show only the generated part
    default_generated = default_result[len(repetition_prompt):]
    print(default_generated)
    
    # Try with higher temperature and diversity settings
    print("\n2. Higher temperature and diversity settings:")
    print("-" * 50)
    
    # Create a model with higher temperature and diversity settings
    diverse_config = ExtendedContextConfig(
        temperature=1.0,          # Higher temperature for more randomness
        top_p=0.95,               # Higher top_p for more diversity
        top_k=100,                # Higher top_k for more diversity
        verbose=True
    )
    
    diverse_model = ContextWormholeModel(model_name, device=device, **diverse_config.__dict__)
    diverse_result = diverse_model.sliding_window_generate(
        repetition_prompt,
        max_new_tokens=100,
        temperature=1.0
    )
    
    # Show only the generated part
    diverse_generated = diverse_result[len(repetition_prompt):]
    print(diverse_generated)
    
    # Try with attention sink strategy
    print("\n3. Using Attention Sink strategy:")
    print("-" * 50)
    
    # Create a model with attention sink strategy
    sink_config = ExtendedContextConfig(
        sink_tokens=16,           # More sink tokens
        temperature=0.8,          # Standard temperature
        verbose=True
    )
    
    sink_model = ContextWormholeModel(model_name, device=device, **sink_config.__dict__)
    sink_result = sink_model.attention_sink_generate(
        repetition_prompt,
        max_new_tokens=100,
        temperature=0.8
    )
    
    # Show only the generated part
    sink_generated = sink_result[len(repetition_prompt):]
    print(sink_generated)
    
    print("\n✅ Example completed!")
    print("\nThis example demonstrates ContextWormhole's ability to handle")
    print("long contexts (8000 tokens) using different strategies,")
    print("as well as how different context length strategies can help")
    print("reduce repetition in generated text.")
    print("\nFor more examples and documentation, visit:")
    print("https://github.com/contextwormhole/contextwormhole")

if __name__ == "__main__":
    main()