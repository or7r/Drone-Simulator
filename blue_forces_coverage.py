from typing import List, Union

from Objects.notifiers.Radar import Radar
from Objects.notifiers.GroundCompany import GroundCompany


def create_blue_forces_coverage_gaza() -> List[Union[Radar, GroundCompany]]:
    # south - gaza
    radars_south = [Radar((31.423646, 34.484981), 10_000, 280, 60),  # beeri
                    Radar((31.309221, 34.393258), 5_000, 290, 60),  # nir oz
                    Radar((31.341020, 34.691933), 20_000, 330, 20),  # mishmar hanegev to ashkelon
                    Radar((31.302155, 34.605973), 20_000, 270, 20),  # ofakim to gaza
                    Radar((31.608674, 34.746969), 20_000, 260, 20),  # kiryat gat to gaza
                    ]

    troops_south = [GroundCompany((31.245129, 34.335290), seeing_distance=2_000),  # sofa motzav
                    GroundCompany((31.380265, 34.388255), seeing_distance=2_000),  # kisufim motzav
                    GroundCompany((31.477534, 34.490303), seeing_distance=2_000),  # nahal oz motzav
                    GroundCompany((31.513214, 34.552468), seeing_distance=2_000),  # mefalsim motzav
                    GroundCompany((31.579000, 34.520717), seeing_distance=2_000),  # mefalsim motzav
                    ]
    blue_forces_gaza = radars_south + troops_south

    return blue_forces_gaza
