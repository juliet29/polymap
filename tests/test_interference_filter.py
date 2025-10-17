from pipe import batched
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.layout.interfaces import Layout
from polymap.layout.neighbors import get_candidate_surface_neighbors, filter_candidate_neighbors
from rich import print

def create_stacked_domains():
    x_range = (1, 10)
    y_ranges = list(range(0, 8) | batched(2))
    return [
        FancyOrthoDomain.from_bounds(*x_range, *i, name=str(ix))
        for ix, i in enumerate(y_ranges)
    ]

def get_close_surface():
    layout = Layout(create_stacked_domains())
    surf = layout.get_domain("3").get_surface("south", 0)
    print(surf)
    potential_nbs = get_candidate_surface_neighbors(layout, surf)
    print(potential_nbs)
    true_nbs = filter_candidate_neighbors(layout, surf, potential_nbs)
    assert len(true_nbs) == 1
    assert true_nbs[0].domain_name == "2"

# range compares!
# set(range(4,5)).issubset(set(range(4,8))) True 




if __name__ == "__main__":
    get_close_surface()