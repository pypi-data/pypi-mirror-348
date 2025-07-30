from ballmatro.generators import exhaustive_generator, to_hf_dataset, generator_to_dict
from ballmatro.score import ScoreInfo
from ballmatro.hands import InvalidHand

def test_exhaustive_generator_size1():
    # Use a small hand size for tractable test
    results = list(exhaustive_generator(1))
    # Each result is a tuple: (hand, ScoreInfo)
    assert all(isinstance(hand, list) for hand, _ in results)
    assert all(isinstance(score_info, ScoreInfo) for _, score_info in results)
    # Check that the number of generated hands matches the expected count
    # There are 4 suits, 13 ranks, 2 modifiers, so 4*13*3 = 156 possible cards
    assert len(results) == 156
    # Check no repetitions in the generated hands
    assert len({tuple(hand) for hand, _ in results}) == len(results)
    # Check no invalid hands
    assert all(result.hand != InvalidHand for _, result in results)

def test_exhaustive_generator_size2():
    # Use a small hand size for tractable test
    results = list(exhaustive_generator(2))
    # Check that the number of generated hands matches the expected count
    # There are 4 suits, 13 ranks, 2 modifiers, so 4*13*3 = 156 possible cards
    # The number of combinations with replacement is (n + r - 1)
    # where n is the number of items to choose from and r is the number of items to choose
    # In this case, n = 156 and r = 2 so the number of combinations is (156 + 2 - 1) choose 2 = 156 * 157 / 2 = 12246
    assert len(results) == 12246
    # Check no repetitions in the generated hands
    assert len({tuple(hand) for hand, _ in results}) == len(results)
    # Check no invalid hands
    assert all(result.hand != InvalidHand for _, result in results)

def test_generator_to_dict():
    # Generate a small dataset with a small generator
    dict_generator = generator_to_dict(exhaustive_generator(1))
    # Check that the dictionary has the expected keys
    assert "input" in dict_generator
    assert "output" in dict_generator
    assert "score" in dict_generator
    assert "hand" in dict_generator
    assert "chips" in dict_generator
    assert "multiplier" in dict_generator
    assert "remaining" in dict_generator

def test_hf_dataset():
    # Generate a Hugging Face dataset with a small generator
    dataset = to_hf_dataset(exhaustive_generator(1))
    # Check that the dataset has the expected columns
    assert "input" in dataset.column_names
    assert "output" in dataset.column_names
    assert "score" in dataset.column_names
    assert "hand" in dataset.column_names
    assert "chips" in dataset.column_names
    assert "multiplier" in dataset.column_names
    assert "remaining" in dataset.column_names
