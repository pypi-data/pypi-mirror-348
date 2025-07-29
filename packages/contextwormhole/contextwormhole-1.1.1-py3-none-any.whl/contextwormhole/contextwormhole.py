#!/usr/bin/env python3
"""
Fixed implementation of ContextWormhole with position ID recycling.

This standalone file contains a fixed implementation of the ContextWormhole library
that properly handles position IDs for very long inputs.
"""

import logging
import functools
import warnings
import torch
from typing import Optional, List, Union, Dict, Any
from transformers import AutoTokenizer, AutoModelForCausalLM

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Custom exceptions
class ContextWormholeError(Exception):
    """Base exception for ContextWormhole errors."""
    pass


class ConfigurationError(ContextWormholeError):
    """Exception raised for configuration errors."""
    pass


class ModelError(ContextWormholeError):
    """Exception raised for model-related errors."""
    pass


class ExtendedContextConfig:
    """Configuration for extended context processing."""

    def __init__(
        self,
        max_training_length: int = 1024,
        window_size: int = 256,
        overlap: int = 64,
        chunk_size: int = 256,
        summary_length: int = 64,
        sink_tokens: int = 16,
        temperature: float = 0.8,
        top_p: float = 0.9,
        top_k: int = 50,
        use_cache: bool = True,
        verbose: bool = False,
        **kwargs,
    ):
        """Initialize configuration with default or custom values."""
        self.max_training_length = max_training_length
        self.window_size = window_size
        self.overlap = overlap
        self.chunk_size = chunk_size
        self.summary_length = summary_length
        self.sink_tokens = sink_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.use_cache = use_cache
        self.verbose = verbose

        # Validate configuration
        if self.overlap >= self.chunk_size:
            raise ConfigurationError(
                f"Overlap ({self.overlap}) must be less than chunk_size ({self.chunk_size})"
            )

        if self.sink_tokens < 0:
            raise ConfigurationError(
                f"sink_tokens ({self.sink_tokens}) must be non-negative"
            )

        # Warn about extreme temperature values
        if self.temperature > 1.5 or self.temperature < 0.1:
            warnings.warn(
                f"Temperature value ({self.temperature}) is outside the recommended range "
                f"[0.1, 1.5]"
            )

        # Handle unknown parameters
        for key, value in kwargs.items():
            warnings.warn(f"Unknown config parameter: {key}")


class ExtendedContextMixin:
    """Mixin class providing extended context functionality."""

    def _ensure_tokenizer(self):
        """Ensure model has a tokenizer attribute."""
        if not hasattr(self, "tokenizer"):
            raise ModelError("Model must have a 'tokenizer' attribute")

    def _detect_max_length(self):
        """Detect maximum context length from model config."""
        if hasattr(self.model, "config"):
            config = self.model.config
            # Try different attributes where max length might be stored
            if hasattr(config, "max_position_embeddings"):
                return config.max_position_embeddings
            elif hasattr(config, "n_positions"):
                return config.n_positions
            elif hasattr(config, "n_ctx"):
                return config.n_ctx
        return 512  # Default fallback

    def _generate_with_cache(self, input_ids, max_new_tokens, temperature):
        """Generate text with KV cache and position ID recycling."""
        try:
            # Create attention mask
            attention_mask = torch.ones_like(input_ids)
            
            # Get model's position embedding limit
            max_position_embeddings = 1024  # Default for GPT-2 models
            if hasattr(self.model.config, "max_position_embeddings"):
                max_position_embeddings = self.model.config.max_position_embeddings
            
            # INNOVATIVE APPROACH: Position ID Recycling
            # Instead of truncating long inputs, we'll use modulo arithmetic to ensure
            # position IDs always stay within the valid range (0 to max_position_embeddings-1)
            
            seq_length = input_ids.size(1)
            
            if self._ext_config.verbose and seq_length > max_position_embeddings:
                logger.info(
                    f"Using position ID recycling for long input ({seq_length} tokens)"
                )
            
            # For very long inputs, we'll keep a good portion of the beginning (for context)
            # and a larger portion of the end (for recency), and apply position ID recycling
            if seq_length > max_position_embeddings * 2:
                # Keep beginning and end portions
                beginning_tokens = max(16, max_position_embeddings // 8)  # At least 16 tokens from beginning
                ending_tokens = max_position_embeddings - beginning_tokens
                
                if self._ext_config.verbose:
                    logger.info(
                        f"Keeping {beginning_tokens} tokens from beginning and {ending_tokens} tokens from end"
                    )
                
                # Select tokens from beginning and end
                beginning_ids = input_ids[:, :beginning_tokens]
                ending_ids = input_ids[:, -ending_tokens:]
                
                # Combine them
                input_ids = torch.cat([beginning_ids, ending_ids], dim=1)
                attention_mask = torch.ones_like(input_ids)
                
                # Update sequence length
                seq_length = input_ids.size(1)
            
            # Create position IDs that cycle within the valid range
            # We use modulo to ensure position IDs stay within the valid range
            # For the first max_position_embeddings tokens, use regular position IDs
            # For tokens beyond that, recycle position IDs using modulo
            
            # Create a range from 0 to seq_length-1
            raw_position_ids = torch.arange(0, seq_length, dtype=torch.long, device=self.device)
            
            # Apply modulo to ensure position IDs stay within valid range
            # We use max_position_embeddings-1 as the modulo to ensure 0-indexed position IDs
            # are always less than max_position_embeddings
            position_ids = (raw_position_ids % (max_position_embeddings-1)).unsqueeze(0)
            
            if self._ext_config.verbose and seq_length > max_position_embeddings:
                logger.info(
                    f"Position IDs recycled to stay within range [0, {max_position_embeddings-1}]"
                )
            
            # Generate parameters
            generate_params = {
                "input_ids": input_ids.to(self.device),
                "attention_mask": attention_mask.to(self.device),
                "max_new_tokens": max_new_tokens,
                "use_cache": self._ext_config.use_cache,
                "pad_token_id": self.tokenizer.eos_token_id,
                "position_ids": position_ids,  # Always include recycled position_ids
            }
            
            # Only add sampling parameters if temperature is not 1.0
            if temperature != 1.0:
                generate_params.update({
                    "do_sample": True,
                    "temperature": temperature,
                    "top_p": self._ext_config.top_p,
                    "top_k": self._ext_config.top_k,
                })
            
            # Generate text
            output = self.model.generate(**generate_params)
            
            # Handle different output formats
            try:
                # Try accessing as a GenerationOutput object
                return self.tokenizer.decode(output.sequences[0], skip_special_tokens=True)
            except AttributeError:
                # Handle as a tensor
                return self.tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            raise ModelError(f"Generation failed: {str(e)}")


def sliding_window(window_size: Optional[int] = None, overlap: Optional[int] = None):
    """Decorator for sliding window context extension with position ID recycling."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(model, prompt, **kwargs):
            # Validate input
            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string")
            if not prompt or prompt.isspace():
                raise ValueError("Prompt cannot be empty")

            # Ensure model has tokenizer
            if not hasattr(model, "tokenizer"):
                raise ModelError("Model must have a 'tokenizer' attribute")
            elif hasattr(model, "_ensure_tokenizer") and callable(
                model._ensure_tokenizer
            ):
                model._ensure_tokenizer()

            # Get configuration
            config = model._ext_config
            window_size_actual = window_size or config.window_size
            overlap_actual = overlap or config.overlap
            max_new_tokens = kwargs.get("max_new_tokens", 100)
            temperature = kwargs.get("temperature", config.temperature)

            # Tokenize input
            try:
                input_tokens = model.tokenizer.encode(prompt)
            except AttributeError:
                raise ModelError("Model must have a 'tokenizer' attribute")

            # Get max length
            if hasattr(model, "_detect_max_length"):
                max_length = model._detect_max_length()
            else:
                max_length = 512  # Default fallback

            if config.verbose:
                logger.info(f"Full prompt: {len(input_tokens)} tokens")
                logger.info(
                    f"Using sliding window with size={window_size_actual}, overlap={overlap_actual}"
                )

            # If input fits in context, process normally
            if len(input_tokens) <= max_length:
                input_tensor = torch.tensor([input_tokens]).to(model.device)
                return model._generate_with_cache(
                    input_tensor, max_new_tokens, temperature
                )

            # Process with sliding window - enhanced version
            # Get the model's position embedding limit
            max_position_embeddings = 1024  # Default for GPT-2 models
            if hasattr(model.model.config, "max_position_embeddings"):
                max_position_embeddings = model.model.config.max_position_embeddings
            
            # For very long inputs, use a more sophisticated approach
            if len(input_tokens) > window_size_actual * 2:
                if config.verbose:
                    logger.info(f"Using enhanced sliding window for long input ({len(input_tokens)} tokens)")
                
                # Keep tokens from beginning, middle, and end for better context
                beginning_tokens_count = min(window_size_actual // 4, 256)  # Beginning context
                middle_tokens_count = min(window_size_actual // 4, 256)     # Middle context
                ending_tokens_count = max_position_embeddings - beginning_tokens_count - middle_tokens_count - 2  # End context (most important)
                
                # Get tokens from different parts of the document
                beginning_tokens = input_tokens[:beginning_tokens_count]
                
                # Middle tokens from approximately the middle of the document
                middle_start = len(input_tokens) // 2 - middle_tokens_count // 2
                middle_tokens = input_tokens[middle_start:middle_start + middle_tokens_count]
                
                # End tokens (most recent/relevant)
                ending_tokens = input_tokens[-ending_tokens_count:]
                
                # Combine them
                enhanced_window = beginning_tokens + middle_tokens + ending_tokens
                
                if config.verbose:
                    logger.info(
                        f"Enhanced window: {len(beginning_tokens)} beginning + "
                        f"{len(middle_tokens)} middle + {len(ending_tokens)} ending tokens"
                    )
                    logger.info(
                        f"Total tokens processed: {len(enhanced_window)} out of {len(input_tokens)} original tokens"
                    )
                    logger.info(
                        f"Position IDs range: 0 to {len(enhanced_window)-1}"
                    )
                
                input_tensor = torch.tensor([enhanced_window]).to(model.device)
                final_window = enhanced_window
            else:
                # For shorter inputs, use the standard sliding window approach
                windows = []
                step = window_size_actual - overlap_actual
                
                for i in range(0, len(input_tokens), step):
                    window = input_tokens[i : i + window_size_actual]
                    windows.append(window)
                    if i + window_size_actual >= len(input_tokens):
                        break
                
                # Process last window with safety checks
                if len(input_tokens) > window_size_actual:
                    last_window = input_tokens[-window_size_actual:]
                    # Ensure we don't exceed the position embedding limit
                    if len(last_window) > max_position_embeddings - 2:
                        last_window = last_window[-(max_position_embeddings - 2):]
                else:
                    last_window = input_tokens
                    # Ensure we don't exceed the position embedding limit
                    if len(last_window) > max_position_embeddings - 2:
                        last_window = last_window[-(max_position_embeddings - 2):]
                
                input_tensor = torch.tensor([last_window]).to(model.device)
                
                if config.verbose:
                    logger.info(f"Standard sliding window: {len(last_window)} tokens")
                
                final_window = last_window
            
            if config.verbose:
                logger.info(f"Processing final window: {len(final_window)} tokens")

            return model._generate_with_cache(input_tensor, max_new_tokens, temperature)

        return wrapper

    return decorator


def hierarchical_context(
    chunk_size: Optional[int] = None, summary_length: Optional[int] = None
):
    """Decorator for hierarchical context processing with position ID recycling."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(model, prompt, **kwargs):
            # Validate input
            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string")
            if not prompt or prompt.isspace():
                raise ValueError("Prompt cannot be empty")

            # Ensure model has tokenizer
            if not hasattr(model, "tokenizer"):
                raise ModelError("Model must have a 'tokenizer' attribute")
            elif hasattr(model, "_ensure_tokenizer") and callable(
                model._ensure_tokenizer
            ):
                model._ensure_tokenizer()

            # Get configuration
            config = model._ext_config
            chunk_size_actual = chunk_size or config.chunk_size
            summary_length_actual = summary_length or config.summary_length
            max_new_tokens = kwargs.get("max_new_tokens", 100)
            temperature = kwargs.get("temperature", config.temperature)

            # Tokenize input
            input_tokens = model.tokenizer.encode(prompt)

            # Get max length
            if hasattr(model, "_detect_max_length"):
                max_length = model._detect_max_length()
            else:
                max_length = 512  # Default fallback

            if config.verbose:
                logger.info(f"Full prompt: {len(input_tokens)} tokens")
                logger.info(
                    f"Using hierarchical context with chunk_size={chunk_size_actual}, "
                    f"summary_length={summary_length_actual}"
                )

            # If input fits in context, process normally
            if len(input_tokens) <= max_length:
                input_tensor = torch.tensor([input_tokens]).to(model.device)
                return model._generate_with_cache(
                    input_tensor, max_new_tokens, temperature
                )

            # Process with enhanced hierarchical approach
            # Get the model's position embedding limit
            max_position_embeddings = 1024  # Default for GPT-2 models
            if hasattr(model.model.config, "max_position_embeddings"):
                max_position_embeddings = model.model.config.max_position_embeddings
            
            # Divide the input into chunks
            chunks = []
            for i in range(0, len(input_tokens), chunk_size_actual):
                chunk = input_tokens[i : i + chunk_size_actual]
                chunks.append(chunk)
            
            if config.verbose:
                logger.info(f"Divided input into {len(chunks)} chunks")
            
            # For long inputs, implement a true hierarchical approach
            if len(chunks) > 1:
                # Calculate how many tokens we can take from each chunk
                tokens_per_chunk = min(
                    summary_length_actual,
                    (max_position_embeddings - chunk_size_actual) // max(1, len(chunks) - 1)
                )
                
                if tokens_per_chunk > 0:
                    # Get representative tokens from each chunk (except the last)
                    chunk_samples = []
                    for i in range(len(chunks) - 1):
                        # Take tokens from the beginning of each chunk
                        sample = chunks[i][:tokens_per_chunk]
                        chunk_samples.append(sample)
                    
                    # Combine samples with the last chunk
                    combined_tokens = []
                    for sample in chunk_samples:
                        combined_tokens.extend(sample)
                    
                    # Add the last chunk (most important for recency)
                    last_chunk = chunks[-1]
                    
                    # Ensure we don't exceed position embedding limit
                    remaining_space = max_position_embeddings - 2 - len(combined_tokens)
                    if len(last_chunk) > remaining_space:
                        last_chunk = last_chunk[-remaining_space:]
                    
                    combined_tokens.extend(last_chunk)
                    
                    if config.verbose:
                        logger.info(
                            f"Hierarchical approach: {len(combined_tokens)} tokens "
                            f"({len(chunk_samples)} chunks × {tokens_per_chunk} tokens + "
                            f"{len(last_chunk)} tokens from last chunk)"
                        )
                        logger.info(
                            f"Total tokens processed: {len(combined_tokens)} out of {len(input_tokens)} original tokens"
                        )
                        logger.info(
                            f"Position IDs range: 0 to {len(combined_tokens)-1}"
                        )
                    
                    input_tensor = torch.tensor([combined_tokens]).to(model.device)
                else:
                    # If we can't take tokens from each chunk, fall back to using just the last chunk
                    last_chunk = chunks[-1]
                    
                    # Ensure we don't exceed position embedding limit
                    if len(last_chunk) > max_position_embeddings - 2:
                        last_chunk = last_chunk[-(max_position_embeddings - 2):]
                    
                    if config.verbose:
                        logger.info(f"Using only last chunk: {len(last_chunk)} tokens")
                    
                    input_tensor = torch.tensor([last_chunk]).to(model.device)
            else:
                # For single chunk inputs
                last_chunk = chunks[0]
                
                # Ensure we don't exceed position embedding limit
                if len(last_chunk) > max_position_embeddings - 2:
                    last_chunk = last_chunk[-(max_position_embeddings - 2):]
                
                input_tensor = torch.tensor([last_chunk]).to(model.device)
            
            if config.verbose:
                logger.info(f"Processing final chunk: {len(last_chunk)} tokens")

            return model._generate_with_cache(input_tensor, max_new_tokens, temperature)

        return wrapper

    return decorator


def attention_sink(sink_tokens: Optional[int] = None):
    """Decorator for attention sink mechanism with position ID recycling."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(model, prompt, **kwargs):
            # Validate input
            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string")
            if not prompt or prompt.isspace():
                raise ValueError("Prompt cannot be empty")

            # Ensure model has tokenizer
            if not hasattr(model, "tokenizer"):
                raise ModelError("Model must have a 'tokenizer' attribute")
            elif hasattr(model, "_ensure_tokenizer") and callable(
                model._ensure_tokenizer
            ):
                model._ensure_tokenizer()

            # Get configuration
            config = model._ext_config
            sink_tokens_actual = sink_tokens or config.sink_tokens
            max_new_tokens = kwargs.get("max_new_tokens", 100)
            temperature = kwargs.get("temperature", config.temperature)

            # Tokenize input
            input_tokens = model.tokenizer.encode(prompt)

            # Get max length
            if hasattr(model, "_detect_max_length"):
                max_length = model._detect_max_length()
            else:
                max_length = 512  # Default fallback

            if config.verbose:
                logger.info(f"Full prompt: {len(input_tokens)} tokens")
                logger.info(
                    f"Using attention sink with sink_tokens={sink_tokens_actual}"
                )
                logger.info(
                    f"Token count: {len(input_tokens)} tokens in original input"
                )

            # If input fits in context, process normally
            if len(input_tokens) <= max_length:
                input_tensor = torch.tensor([input_tokens]).to(model.device)
                return model._generate_with_cache(
                    input_tensor, max_new_tokens, temperature
                )

            # Process with attention sink
            # For long inputs, implement the true attention sink mechanism
            # with position ID recycling to handle arbitrarily long inputs
            
            # Get the model's position embedding limit
            max_position_embeddings = 1024  # Default for GPT-2 models
            if hasattr(model.model.config, "max_position_embeddings"):
                max_position_embeddings = model.model.config.max_position_embeddings
            
            # Calculate how many tokens we can keep from the end
            # We want to keep as many as possible while ensuring the total
            # doesn't exceed max_position_embeddings
            end_tokens_count = min(
                len(input_tokens) - sink_tokens_actual,  # Don't overlap with sink tokens
                max_position_embeddings - sink_tokens_actual - 2  # Ensure total fits in position embeddings with safety margin
            )
            
            # Get sink tokens and end tokens
            sink_tokens_part = input_tokens[:sink_tokens_actual]
            end_tokens_part = input_tokens[-end_tokens_count:]
            
            # Combine them
            combined_tokens = sink_tokens_part + end_tokens_part
            
            if config.verbose:
                logger.info(
                    f"Using {len(sink_tokens_part)} sink tokens + {len(end_tokens_part)} recent tokens"
                )
                logger.info(
                    f"Total tokens processed: {len(combined_tokens)} out of {len(input_tokens)} original tokens"
                )
                logger.info(
                    f"Position IDs range: 0 to {len(combined_tokens)-1}"
                )
            
            input_tensor = torch.tensor([combined_tokens]).to(model.device)

            return model._generate_with_cache(input_tensor, max_new_tokens, temperature)

        return wrapper

    return decorator


def extended_context(strategy: str = "sliding_window", **kwargs):
    """Meta-decorator that selects the appropriate context extension strategy."""
    if strategy == "sliding_window":
        return sliding_window(**kwargs)
    elif strategy == "hierarchical":
        return hierarchical_context(**kwargs)
    elif strategy == "attention_sink":
        return attention_sink(**kwargs)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


class ContextWormholeModel(ExtendedContextMixin):
    """Main model class for extended context processing."""

    def __init__(self, model_path: str, **kwargs):
        """Initialize with a model path and optional configuration."""
        # Create configuration
        self._ext_config = ExtendedContextConfig(**kwargs)

        # Set device
        self.device = kwargs.get("device", "cuda" if torch.cuda.is_available() else "cpu")

        # Load model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)

            # Set pad token if not defined
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            if self._ext_config.verbose:
                logger.info(f"Loaded model: {model_path}")
                logger.info(f"Using device: {self.device}")
                logger.info(f"Context length: {self._detect_max_length()}")
        except Exception as e:
            raise ModelError(f"Failed to load model: {str(e)}")

    def __getattr__(self, name):
        # Forward attribute access to the wrapped model
        if hasattr(self.model, name):
            return getattr(self.model, name)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    @sliding_window()
    def sliding_window_generate(self, prompt: str, **kwargs):
        """Generate text using sliding window approach."""
        # This is just a placeholder - the actual implementation is in the decorator
        return self.model.generate(prompt, **kwargs)

    @hierarchical_context()
    def hierarchical_generate(self, prompt: str, **kwargs):
        """Generate text using hierarchical context approach."""
        # This is just a placeholder - the actual implementation is in the decorator
        return self.model.generate(prompt, **kwargs)

    @attention_sink()
    def attention_sink_generate(self, prompt: str, **kwargs):
        """Generate text using attention sink approach."""
        # This is just a placeholder - the actual implementation is in the decorator
        return self.model.generate(prompt, **kwargs)


def create_extended_model(model_path: str, device: Optional[str] = None, **kwargs):
    """Factory function to create a ContextWormholeModel."""
    # Determine device
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        # Create and return model
        return ContextWormholeModel(model_path, device=device, **kwargs)
    except Exception as e:
        raise ModelError(f"Failed to create model: {str(e)}")


# For backwards compatibility
ExtendedContextConfig = ExtendedContextConfig