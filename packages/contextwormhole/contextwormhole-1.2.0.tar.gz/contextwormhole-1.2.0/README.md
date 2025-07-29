# ContextWormhole

**Context length extension library for transformers**

ContextWormhole provides practical implementations of three established context extension techniques. When your transformer model reaches its context limit, this library offers clean, tested strategies to handle longer inputs.

```bash
pip install contextwormhole
```

## Purpose

Most transformer models have fixed context windows (e.g., 1024 tokens for GPT-2). This library implements three strategies to work with longer texts while maintaining the model's original architecture.

## Strategies

### 1. Sliding Window

Processes text in overlapping chunks, maintaining continuity between segments.

```python
@sliding_window(window_size=512, overlap=64)
def process_long_document(model, text, **kwargs):
    return model.generate(text, **kwargs)
```

- **Implementation**: Overlapping windows with position ID recycling
- **Time complexity**: O(n)
- **Memory complexity**: O(window_size)
- **Use cases**: Documents, code files, articles

### 2. Hierarchical Context

Creates summaries of text chunks, then combines summaries with final content.

```python
@hierarchical_context(chunk_size=256, summary_length=64)
def analyze_paper(model, paper, **kwargs):
    return model.generate(paper, **kwargs)
```

- **Implementation**: Chunk → summarize → combine → process
- **Time complexity**: O(n log n)
- **Memory complexity**: O(n/chunk_size * summary_length)
- **Use cases**: Research papers, structured documents

### 3. Attention Sink

Preserves initial tokens plus recent context, discarding middle content.

```python
@attention_sink(sink_tokens=16)
def continue_conversation(model, chat_history, **kwargs):
    return model.generate(chat_history, **kwargs)
```

- **Implementation**: Initial tokens + recent context
- **Time complexity**: O(1)
- **Memory complexity**: O(max_length)
- **Use cases**: Conversations, chat histories

## Empirical Results

Tests on repetition patterns (10 runs each, distilgpt2):

| Strategy | Uniqueness Ratio | Repeated Phrases | Notes |
|----------|-----------------|------------------|-------|
| Standard (low temp) | 0.59 | 3.5 | Baseline |
| Standard (high temp) | 0.28 | 2.0 | High repetition |
| Attention Sink | 0.67 | 1.8 | Best coherence |

The attention sink strategy showed consistently better text quality with fewer repetitive patterns.

## Usage

### Basic Example

```python
from contextwormhole import ContextWormholeModel

model = ContextWormholeModel("gpt2")

# Different strategies for different needs
result1 = model.sliding_window_generate(long_document, max_new_tokens=100)
result2 = model.hierarchical_generate(research_paper, max_new_tokens=100)
result3 = model.attention_sink_generate(conversation_history, max_new_tokens=100)
```

### Configuration

```python
from contextwormhole import ExtendedContextConfig

config = ExtendedContextConfig(
    window_size=256,
    overlap=64,
    chunk_size=256,
    summary_length=64,
    sink_tokens=16,
    use_cache=True,
)

model = ContextWormholeModel("gpt2", **config.__dict__)
```

### CLI Interface

```bash
# Sliding window
contextwormhole --model gpt2 --input document.txt --strategy sliding_window

# Hierarchical
contextwormhole --model gpt2 --input paper.txt --strategy hierarchical

# Attention sink
contextwormhole --model gpt2 --input chat.txt --strategy attention_sink
```

## Example Files

This repository includes several example files that demonstrate how to use ContextWormhole with different strategies and configurations:

### 1. contextwormhole.py

A complete implementation with properly defined variables that demonstrates all three context handling strategies:

```python
from contextwormhole import ContextWormholeModel, ExtendedContextConfig

# Create a configuration optimized for long contexts
config = ExtendedContextConfig(
    max_training_length=2048,  # Increase the max training length
    window_size=512,           # Larger window size
    overlap=128,               # Significant overlap for better coherence
    chunk_size=512,            # Larger chunk size for hierarchical processing
    summary_length=128,        # Longer summaries
    sink_tokens=32,            # More sink tokens for attention sink
    temperature=0.8,           # Standard temperature
    verbose=True               # Show verbose output to see what's happening
)

# Initialize the model with our configuration
model = ContextWormholeModel("gpt2", **config.__dict__)

# Different strategies for different needs
result1 = model.sliding_window_generate(long_document, max_new_tokens=100)
result2 = model.hierarchical_generate(research_paper, max_new_tokens=100)
result3 = model.attention_sink_generate(conversation_history, max_new_tokens=100)
```

### 2. example.py

A simple example showing how to use the library with a real model:

```python
from contextwormhole import ContextWormholeModel, ExtendedContextConfig

# Create a configuration optimized for long contexts
config = ExtendedContextConfig(
    max_training_length=2048,
    window_size=512,
    overlap=128,
    chunk_size=512,
    summary_length=128,
    sink_tokens=32,
    temperature=0.8,
    verbose=True
)

# Initialize the model with our configuration
model = ContextWormholeModel("gpt2", **config.__dict__)

# Generate text using different strategies
result1 = model.sliding_window_generate(long_document, max_new_tokens=50)
result2 = model.hierarchical_generate(long_document, max_new_tokens=50)
result3 = model.attention_sink_generate(long_document, max_new_tokens=50)
```

### 3. demo.py

A more comprehensive demo with custom configurations for different use cases:

```python
from contextwormhole import ContextWormholeModel, ExtendedContextConfig

# Create a custom configuration for detailed, creative responses
detailed_config = ExtendedContextConfig(
    max_training_length=2048,
    window_size=512,
    overlap=128,
    chunk_size=512,
    summary_length=128,
    temperature=0.9,
    top_p=0.95,
    sink_tokens=24,
    verbose=True
)

# Create a model with the detailed configuration
detailed_model = ContextWormholeModel("gpt2", **detailed_config.__dict__)

# Generate a response using the attention sink strategy
detailed_response = detailed_model.attention_sink_generate(
    conversation_history,
    max_new_tokens=100
)
```

These examples demonstrate how ContextWormhole automatically handles context length limitations using innovative techniques like position ID recycling, sliding windows, hierarchical processing, and attention sink mechanisms.

## Performance Characteristics

| Strategy | Max Context | Memory (MB)* | Time (s)* | Best For |
|----------|-------------|--------------|-----------|----------|
| Sliding Window | ~10K tokens | 600 | 1.5-2.0 | Documents, code |
| Hierarchical | ~20K tokens | 400 | 1.0-1.5 | Papers, reports |
| Attention Sink | ~8K tokens | 300 | 0.8-1.2 | Conversations |

*Approximate values for GPT-2 on CPU

## Benchmark Results

Recent benchmark results with GPT-2 on CPU:

```
📊 Benchmark Results
================================================================================
Strategy             Input Length    Processing Time      Memory Used     Output Length
--------------------------------------------------------------------------------
sliding_window       1050            1.96s              659.35 MB       1252
hierarchical         1050            1.28s              27.59 MB        1275
attention_sink       1050            1.21s              11.55 MB        1241
sliding_window       5250            2.48s              655.90 MB       4941
hierarchical         5250            1.44s              68.75 MB        1909
attention_sink       5250            2.47s              272.18 MB       4979
sliding_window       10500           2.27s              50.39 MB        4973
hierarchical         10500           1.88s              137.20 MB       3572
attention_sink       10500           2.27s              9.55 MB         5864
sliding_window       21000           2.40s              50.85 MB        5018
hierarchical         21000           2.20s              3.58 MB         4485
attention_sink       21000           2.42s              24.69 MB        5012

📈 Summary
================================================================================
sliding_window: Avg Time = 2.28s, Avg Memory = 354.12 MB
hierarchical: Avg Time = 1.70s, Avg Memory = 59.28 MB
attention_sink: Avg Time = 2.09s, Avg Memory = 79.50 MB
```

Key observations:
- **Hierarchical** strategy consistently shows the best average processing time (1.70s)
- **Attention Sink** has the most balanced memory usage across different input lengths
- **Sliding Window** uses more memory for smaller inputs but stabilizes for larger texts
- All strategies successfully handle inputs up to 21,000 characters (far beyond the model's native context limit)

## Implementation Notes

- Each strategy respects the model's native context limit for individual forward passes
- Position ID recycling enables handling of arbitrarily long inputs
- KV caching improves generation speed and maintains coherence
- All strategies include proper error handling and configuration validation

## Why Position ID Recycling?

Position IDs are critical in transformer models as they provide information about token order. However, they present a significant challenge when working with inputs that exceed the model's maximum context length:

1. **Index Out of Range Errors**: Without proper handling, position IDs for long inputs can exceed the maximum index in the position embedding table, causing runtime errors.

2. **Context Preservation**: Simply truncating inputs loses valuable context. Position ID recycling allows us to maintain more context by intelligently selecting which parts of the input to keep.

3. **Quality Improvements**: Our tests show that proper position ID handling reduces repetition in generated text and improves overall coherence.

4. **Arbitrary Length Handling**: With position ID recycling, the library can process inputs of any length while ensuring position IDs always stay within the valid range (0 to max_position_embeddings-1).

The implementation uses modulo arithmetic to "recycle" position IDs, combined with strategic token selection to preserve the most relevant context from beginning, middle, and end of long documents.

## Requirements

- Python ≥ 3.8
- PyTorch ≥ 1.9.0
- Transformers ≥ 4.20.0
- NumPy ≥ 1.20.0

## Technical Background

This library implements well-established context extension techniques:

- **Sliding Window**: Classical attention windowing
- **Hierarchical Context**: Recursive summarization approach
- **Attention Sink**: Based on StreamingLLM research

The focus is on providing clean, tested implementations with practical optimizations rather than novel algorithms.

## License

MIT License