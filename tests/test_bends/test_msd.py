import pytest
from typing import get_args

from polymap.bends.main import (
    remove_bends_from_layout,
)
from polymap.examples.msd import (
    MSD_IDs,
    get_one_msd_layout,
)


@pytest.mark.parametrize("id", get_args(MSD_IDs)[0:5])
def test_msd_layouts_can_have_bends_removed(id):
    _, layout = get_one_msd_layout(id)
    _, bad_domains = remove_bends_from_layout(layout)
    if id == "22940":
        assert len(bad_domains) == 1
    else:
        assert not bad_domains
