from polymap.geometry.surfaces import FancyRange
import pytest

self = FancyRange(10, 15)
co_small = FancyRange(11, 12)
co_large = FancyRange(8, 20)
small = FancyRange(6, 7)
small_touch = FancyRange(6, 10)
large = FancyRange(22, 25)

cases: list[tuple[FancyRange, bool]] = [
    (co_small, True),
    (co_large, True),
    (small, False),
    (small_touch, False),
    (large, False),
]


@pytest.mark.parametrize("other, is_coincident", cases)
def test_coinicidence(other, is_coincident):
    assert is_coincident == self.is_coincident(other)
