# from typing import get_args
#
# from loguru import logger
# from rich.pretty import pretty_repr
# from polymap import logconf
# from polymap.bends.b2 import assign_bends
# from polymap.bends.bends import get_domain
# from polymap.bends.problems import pi3s, kappa2s
# from polymap.examples.msd import MSD_IDs
# from polymap.visuals.visuals import plot_domain_with_surfaces
#
#
# def test_bad_domain(id_: str | int, domain_name: str, show=False):
#     id = str(id_)
#     assert id in get_args(MSD_IDs), f"{id} not in MSD_IDS"
#     msd_id: MSD_IDs = id  # pyright: ignore[reportAssignmentType]
#     domain = get_domain(msd_id, domain_name)
#     bh = assign_bends(domain)
#
#     if bh.summary["pi3s"].n_failing > 0:
#         pass
#         logger.critical(f"Failing domain:({id, domain_name})")
#         logger.info(pretty_repr(bh.summary))
#         logger.info("\n")
#         plot_domain_with_surfaces(domain, title=f"{id_} {domain_name}")
#     # logger.info(domain.summarize_surfaces())
#     # plot_domain_with_surfaces(domain, title=f"{id_} {domain_name}")
#     # logger.debug(bh.kappa2s[0].surface_names)
#     # logger.debug(bh.kappa2s[0].are_vectors_correct)
#
#
# def test_many_bad_domain(key: str):
#     groups = {"p": pi3s, "k": kappa2s}
#     for id, name in groups[key]:
#         test_bad_domain(id, name)
#
#
# if __name__ == "__main__":
#     logconf.logset()
#     # b = kappa2s[0]
#     # test_bad_domain(*b)
#     test_many_bad_domain("p")
