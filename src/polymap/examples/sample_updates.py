from polymap.examples.domains import create_ortho_domain


class BottomLData:
    domain = create_ortho_domain("BOTTOM_UP_L")
    paired_coords = domain.paired_coords

    # targets
    east_0 = domain.get_surface("east", 0)
    east_1 = domain.get_surface("east", 1)
    north_0 = domain.get_surface("north", 0)
    # NOTE: special case -> first edge
    west_0 = domain.get_surface("west", 0)
    # NOTE: special case -> last edge
    south_0 = domain.get_surface("south", 0)

    study_surfaces = [east_0, east_1, north_0, west_0, south_0]
