from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.nonortho.dot import make_ortho_coords

from polymap.process.process import simplify_layout
from polymap.visuals.visuals import plot_layout_comparison, plot_polygon_comparison
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
import shapely as sp


def test_shapely_fixes(msd_id: MSD_IDs, domain_name: str, tolerance=0.13):
    id, layout = get_one_msd_layout(msd_id)
    dom = layout.get_domain(domain_name)
    p1 = dom.polygon
    p2 = sp.simplify(p1, tolerance=tolerance)

    p2dom = FancyOrthoDomain(get_coords_from_shapely_polygon(p2))

    ortho_coords = make_ortho_coords(p2dom.coords, p2dom.vectors)

    dom_ortho = FancyOrthoDomain(ortho_coords)
    p3 = dom_ortho.polygon

    polys = [p1, p2, p3]
    titles = ["orig", f"shapely.simplify: tol={tolerance}", "ortho"]

    plot_polygon_comparison(polys, titles, f"{id}-{domain_name}")


def see_shapely_fixes():
    test_shapely_fixes("106493", "corridor_2")
    test_shapely_fixes("71308", "corridor_2")
    test_shapely_fixes("106493", "kitchen_7")


def test_simplify_layout():
    id, layout = get_one_msd_layout("60529")
    new_layout = simplify_layout(layout)
    plot_layout_comparison([layout, new_layout], [str(id), "simplified"])


if __name__ == "__main__":
    test_simplify_layout()
