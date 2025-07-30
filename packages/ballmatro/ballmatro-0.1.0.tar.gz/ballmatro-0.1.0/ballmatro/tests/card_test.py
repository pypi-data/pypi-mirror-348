"""Tests for the card module."""
from ballmatro.card import Card

def test_card_suit():
    card = Card("10♠")
    assert card.suit == "♠"
    card = Card("A♥")
    assert card.suit == "♥"
    card = Card("🂿")
    assert card.suit is None

def test_card_rank():
    card = Card("10♠")
    assert card.rank == "10"
    card = Card("A♥")
    assert card.rank == "A"
    card = Card("🂿Cards with rank 2 provide double chips")
    assert card.rank is None

def test_card_modifier():
    card = Card("10♠+")
    assert card.modifier == "+"
    card = Card("A♥x")
    assert card.modifier == "x"
    # card = Card("K♣*")
    # assert card.modifier == "*"
    card = Card("Q♦")
    assert card.modifier is None

def test_card_is_joker():
    card = Card("🂿Cards from the ♦ suit cannot be used in the hand")
    assert card.is_joker is True
    card = Card("10♠")
    assert card.is_joker is False

def test_card_joker_rule():
    card = Card("🂿Straights cannot be played")
    assert card.joker_rule == "Straights cannot be played"
    card = Card("10♠")
    assert card.joker_rule is None
