from utils4plans.lists import chain_flatten
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.update import InvalidPolygonError, update_domain
from polymap.layout.interfaces import create_layout_from_json
from polymap.paths import DynamicPaths
from polymap.nonortho.dot import make_ortho_coords
from random import choice, seed, uniform

seed(1234567)


def profile_msd_domains():
    source_path = DynamicPaths.MSD_PATHS
    paths = sorted([i for i in source_path.iterdir()])
    layouts = [create_layout_from_json(path.stem, source_path) for path in paths]
    print(f"{len(layouts)=}")
    domains = chain_flatten([i.domains for i in layouts])
    print(f"{len(domains)=}")
    return domains


def attempt_moving_domain(domain: FancyOrthoDomain):
    area = domain.polygon.area
    amount_to_move_potential = 0.15 * area
    move = round(uniform(-amount_to_move_potential, amount_to_move_potential), 3)
    if not domain.is_orthogonal:
        print(f"{domain.name} is not orthogonal, trying to fix...")
        new_coords = make_ortho_coords(domain.coords, domain.vectors)
        domain = FancyOrthoDomain(new_coords)

    surface_to_move = choice(domain.surfaces)
    updated_domain = update_domain(domain, surface_to_move, move, debug=False)
    return updated_domain


def study_moving_domains():
    domains = profile_msd_domains()
    new_doms = []
    num_failing = 0
    for ix, domain in enumerate(domains):
        try:
            dom = attempt_moving_domain(domain)
            new_doms.append(dom)
        except InvalidPolygonError as err:
            print(f"domain at ix: {ix} failed: {err}")
            num_failing += 1

    print(f"{num_failing=}")
    print(f"ratio of fail to total: {num_failing/len(domains)}")

    # for d in new_doms:
    #     if len(d.surfaces) > 4:
    #         d.plot()


if __name__ == "__main__":
    study_moving_domains()
