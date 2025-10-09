from polymap.geometry.surfaces import FancyRange
import pytest

self = FancyRange(10, 15)
coincident_small = FancyRange(11, 12)
coincident_touch = FancyRange(10, 12)
coincident_large = FancyRange(8, 20)
small = FancyRange(6, 7)
small_touch = FancyRange(6, 10)
large = FancyRange(22, 25)

cases: list[tuple[FancyRange, bool]] = [
    (coincident_small, True),
    (coincident_large, True),
    (small, False),
    (small_touch, False),
    (large, False),
]


@pytest.mark.parametrize("other, is_coincident", cases)
def test_coinicidence(other, is_coincident):
    assert is_coincident == self.is_coincident(other)


contains_cases: list[tuple[FancyRange, bool]] = [
    (coincident_small, True),
    (coincident_touch, True),
    (coincident_large, False),
    (small, False),
    (small_touch, False),
    (large, False),
]


@pytest.mark.parametrize("other, contains", contains_cases)
def test_contains(other, contains):
    assert contains == self.contains(other)


if __name__ == "__main__":
    print(coincident_small.contains(small))