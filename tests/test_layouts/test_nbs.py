from loguru import logger
from utils4plans.lists import chain_flatten
from utils4plans.sets import set_equality
from typing import TypeVar

from utils4plans import logconfig

T = TypeVar("T")


def generate_comparisons(arr: list[int]):
    def gen(item: int):
        ix = slist.index(item)
        remain_list = slist[ix + 1 :]
        pairs = [(item, i) for i in remain_list]
        return pairs

    slist = sorted(
        arr, reverse=True
    )  # this is generic, for ints, now need something more specific for neigbours
    logger.info(slist)
    assert slist[0] > slist[1]
    res = [gen(i) for i in slist]
    return chain_flatten(res)


def test_generate_nb_comparisons():
    lst = [1, 2, 3, 4]
    expected = [(4, 3), (4, 2), (4, 1), (3, 2), (3, 1), (2, 1)]
    out = generate_comparisons(lst)
    logger.info(out)
    assert set_equality(expected, out)


if __name__ == "__main__":
    logconf.logset()
    test_generate_nb_comparisons()
