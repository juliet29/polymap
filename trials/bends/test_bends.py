from typing import NamedTuple, get_args
from rich import print
from polymap.bends.bends import (
    get_domain,
)
from polymap.bends.iterate import clean_layout, iterate_clean_domain
from polymap.examples.msd import MSD_IDs, get_one_msd_layout


def test_bends():
    id: MSD_IDs = "67372"
    _, layout = get_one_msd_layout(id)
    domains = layout.domains
    for dom in domains:
        print(f"\n{dom.name.upper()=}")
        try:
            iterate_clean_domain(dom, id)
        except NotImplementedError as e:
            print(e)
            continue


def test_layout():
    id: MSD_IDs = "57231"
    _, layout = get_one_msd_layout(id)
    new_layout = clean_layout(layout, layout_id=id, debug=False)


def test_all_layouts():
    bad_ids = []
    good_ids = []
    bad_domains_all = []
    for id in get_args(MSD_IDs):
        print(f"\n{id=}")
        _, layout = get_one_msd_layout(id)

        _, bad_domains = clean_layout(layout, layout_id=id, debug=False)
        print(f"{bad_domains=}")
        bad_domains_all.extend(bad_domains)

        if not bad_domains:
            good_ids.append(id)
        else:
            bad_ids.append(id)

    print(f"{sorted(bad_ids)=}")
    print(f"{sorted(good_ids)=}")
    print(f"{sorted(bad_domains_all)=}")


def test_bends_one():
    domain_name = "kitchen_9"
    id: MSD_IDs = "27540"
    dom = get_domain(id, domain_name)
    iterate_clean_domain(dom, id)


class DomainName(NamedTuple):
    id: str
    room_type: str
    ix: str

    @property
    def msd_id(self) -> MSD_IDs:
        assert self.id in get_args(MSD_IDs)
        id: MSD_IDs = self.id  # pyright: ignore[reportAssignmentType]
        return id

    @property
    def domain_name(self):
        return f"{self.room_type}_{self.ix}"


def test_failing_domain(name: str):
    dname = DomainName(*name.split("_"))
    dom = get_domain(dname.msd_id, dname.domain_name)
    iterate_clean_domain(dom, dname.msd_id)


if __name__ == "__main__":
    # test_failing_domain("58613_kitchen_3")
    test_all_layouts()
