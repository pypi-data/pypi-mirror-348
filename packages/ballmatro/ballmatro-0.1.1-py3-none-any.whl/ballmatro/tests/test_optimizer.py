import pytest

from ballmatro.card import Card
from ballmatro.optimizer import brute_force_optimize
from ballmatro.score import ScoreInfo
from ballmatro.hands import HighCard, Pair, TwoPair, ThreeOfAKind, FullHouse, Flush, Straight, FourOfAKind, StraightFlush

test_data = [
    (
        [Card('3♦')],
        ScoreInfo(played=[Card('3♦')], remaining=[], hand=HighCard, chips=8, multiplier=1)
    ),
    (
        [Card(txt='K♥x'), Card(txt='A♥x')],
        ScoreInfo(played=[Card(txt='A♥x')], remaining=[Card(txt='K♥x')], hand=HighCard, chips=16, multiplier=5)
    ),
    (
        [Card('2♥'), Card('3♦')],
        ScoreInfo(played=[Card('3♦')], remaining=[Card('2♥')], hand=HighCard, chips=8, multiplier=1)
    ),
    (
        [Card('2♥'), Card('2♥'), Card('3♦')],
        ScoreInfo(played=[Card('2♥'), Card('2♥')], remaining=[Card('3♦')], hand=Pair, chips=14, multiplier=2)
    ),
    (
        [Card('2♥'), Card('2♥'), Card('3♦'), Card('3♦'), Card('A♣')],
        ScoreInfo(played=[Card('2♥'), Card('2♥'), Card('3♦'), Card('3♦')], remaining=[Card('A♣')], hand=TwoPair, chips=30, multiplier=2)
    ),
    (
        [Card('3♥'), Card('3♦'), Card('3♠'), Card('A♣')],
        ScoreInfo(played=[Card('3♥'), Card('3♦'), Card('3♠')], remaining=[Card('A♣')], hand=ThreeOfAKind, chips=39, multiplier=3)
    ),
    (
        [Card('3♥'), Card('3♦'), Card('3♠'), Card('A♦'), Card('A♠'), Card('2♥'), Card('2♥')],
        ScoreInfo(played=[Card('3♥'), Card('3♦'), Card('3♠'), Card('A♦'), Card('A♠')], remaining=[Card('2♥'), Card('2♥')], hand=FullHouse, chips=71, multiplier=4)
    ),
    (
        [Card('2♥'), Card('2♥'), Card('3♥'), Card('5♥'), Card('8♥'), Card('J♥')],
        ScoreInfo(played=[Card('2♥'), Card('3♥'), Card('5♥'), Card('8♥'), Card('J♥')], remaining=[Card('2♥')], hand=Flush, chips=63, multiplier=4)
    ),
    (
        [Card('2♥'), Card('3♦'), Card('4♠'), Card('5♦'), Card('6♠'), Card('3♦'), Card('3♦')],
        ScoreInfo(played=[Card('2♥'), Card('3♦'), Card('4♠'), Card('5♦'), Card('6♠')], remaining=[Card('3♦'), Card('3♦')], hand=Straight, chips=50, multiplier=4)
    ),
    (
        [Card('2♥'), Card('4♥'), Card('3♥'), Card('3♦'), Card('3♠'), Card('3♣'), Card('A♥')],
        ScoreInfo(played=[Card('3♥'), Card('3♦'), Card('3♠'), Card('3♣')], remaining=[Card('2♥'), Card('4♥'), Card('A♥')], hand=FourOfAKind, chips=72, multiplier=7)
    ),
    (
        [Card('2♥'), Card('3♥'), Card('4♥'), Card('5♠'), Card('5♥'), Card('6♥'), Card('7♠')],
        ScoreInfo(played=[Card('2♥'), Card('3♥'), Card('4♥'), Card('5♥'), Card('6♥')], remaining=[Card('5♠'), Card('7♠')], hand=StraightFlush, chips=120, multiplier=8)
    ),
]

@pytest.mark.parametrize("cards, expected_score_info", test_data)
def test_brute_force_optimize(cards, expected_score_info):
    """The brute force optimizer can find the best hand for a number of cards"""
    assert brute_force_optimize(cards) == expected_score_info
