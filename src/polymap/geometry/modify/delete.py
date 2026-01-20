from typing import NamedTuple

from polymap.geometry.paired_coords import PairedCoord


class Delete(NamedTuple):
    paired_coords: list[PairedCoord]
    target_coords: PairedCoord


def delete_paired_coords(delete: Delete):
    paired_coords, target = delete
    coords_to_delete_ix = paired_coords.index(target)
    new_coords = [i for ix, i in enumerate(paired_coords) if ix != coords_to_delete_ix]
    return new_coords
