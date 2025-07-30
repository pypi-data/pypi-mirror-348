"""Functions to score ballmatro hands"""
from dataclasses import dataclass
from typing import List, Tuple


from ballmatro.card import Card
from ballmatro.hands import find_hand, PokerHand, InvalidHand


CHIPS_PER_RANK = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}


@dataclass
class ScoreInfo:
    """Class that represents the score of a hand"""
    played: List[Card]  # Cards played in the hand
    remaining: List[Card]  # Unplayed cards
    hand: PokerHand  # Type of hand played
    chips: int = 0  # Value in chips of the hand
    multiplier: int = 0  # Multiplier for the chips value

    @property
    def score(self) -> int:
        """Return the score of the hand"""
        return self.chips * self.multiplier

    def __repr__(self):
        """Return a string representation of the score info"""
        if self.hand is None:
            return "ScoreInfo(INVALID HAND, chips=0, multiplier=0, score=0)"
        return f"ScoreInfo(played={self.played}, remaining={self.remaining}, hand={self.hand}, chips={self.chips}, multiplier={self.multiplier}, score={self.score})"

def remaining_cards(available: List[Card], played: List[Card]) -> List[Card]:
    """Returns the remaining (not played) cards after playing a hand"""
    remaining = available.copy()
    for card in played:
        # Check if the card is available
        if card not in remaining:
            raise ValueError(f"Impossible play: card {card} not in available cards")
        # Remove the card from the remaining cards
        remaining.remove(card)
    return remaining

def score_played(available: List[Card], played: List[Card]) -> ScoreInfo:
    """Given a list of played cards, find their ballmatro score
    
    A score of 0 is attained when the hand is not recognized or the list of played cards contains cards that are not available.
    """
    # Check if the played cards are available
    try:
        remaining = remaining_cards(available, played)
    except ValueError:
        # If the play is impossible, return a score of 0
        return ScoreInfo(played, available, InvalidHand)
    # Find the hand type
    hand = find_hand(played)
    if hand == InvalidHand:
        return ScoreInfo(played, remaining, InvalidHand)
    
    # Start scoring using the chips and multiplier of the hand type
    chips, multiplier = hand.chips, hand.multiplier
    # Now iterate over the cards in the order played, and score each card individually
    for card in played:
        chips, multiplier = score_card(card, chips, multiplier)

    return ScoreInfo(played, remaining, hand, chips, multiplier)

def score_card(card: Card, chips: int, multiplier: int) -> Tuple[int, int]:
    """Applies the scoring of a single card to the current chips and multiplier"""
    # Add the chips of the card rank to the current chips
    chips += CHIPS_PER_RANK.get(card.rank, 0)
    # Apply modifiers
    if card.modifier == "+":
        chips += 30
    elif card.modifier == "x":
        multiplier += 4
    return chips, multiplier
