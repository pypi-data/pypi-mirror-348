"""Functions to generate datasets for LLM training with ballmatro hands"""
from datasets import Dataset
from itertools import combinations_with_replacement
from typing import List, Tuple, Generator, Dict, Any

from ballmatro.card import Card, SUITS, RANKS, MODIFIERS
from ballmatro.optimizer import brute_force_optimize
from ballmatro.score import ScoreInfo

def exhaustive_generator(hand_size: int) -> Generator[Tuple[List[Card], ScoreInfo], None, None]:
    """Generator functions for a dataset with all possible hands of a given size
    and their optimal plays using brute force optimization.
    Args:
        hand_size (int): The size of the hands to generate.
    Returns:
        List[Tuple[List[Card], ScoreInfo]]: A list of tuples, each containing a hand and its optimal play in the form of a ScoreInfo object.
    """
    # Generate all possible cards
    cards = [Card(f"{rank}{suit}{modifier}") for suit in SUITS for rank in RANKS for modifier in [""] + MODIFIERS]
    
    # Generate all combinations of the given size
    for input in combinations_with_replacement(cards, hand_size):
        # Find optimal play for this input
        optimal_play = brute_force_optimize(list(input))
        yield list(input), optimal_play

def generator_to_dict(generator: Generator[Tuple[List[Card], ScoreInfo], None, None]) -> Dict[str, List[Any]]:
    """Convert a generator of tuples to a generator of dictionaries.

    Args:
        generator (Generator[Tuple[List[Card], ScoreInfo]]): A generator that yields tuples of input cards and their corresponding ScoreInfo.

    Returns:
        Dict[str, List[Any]]: A dictionary where each key corresponds to a field in the ScoreInfo object.
    """
    # Get all the data into memory
    data = list(generator)
    # Create a dictionary with the data
    dict_data = {
        "input": [str(cards) for cards, _ in data],
        "output": [str(score.played) for _, score in data],
        "score": [score.score for _, score in data],
        "hand": [score.hand.__name__ for _, score in data],
        "chips": [score.chips for _, score in data],
        "multiplier": [score.multiplier for _, score in data],
        "remaining": [str(score.remaining) for _, score in data],
    }
    return dict_data

def to_hf_dataset(generator: Generator[Tuple[List[Card], ScoreInfo], None, None]) -> Dataset:
    """Convert a dataset generator to a Hugging Face dataset format.
    
    Args:
        generator (Generator[Tuple[List[Card], ScoreInfo]]): A generator that yields tuples of input cards and their corresponding ScoreInfo.
    
    Returns:
        Dataset: A Hugging Face dataset containing the generated data.
    """
    # Create a Hugging Face dataset from the generator
    return Dataset.from_dict(generator_to_dict(generator))
