from enum import StrEnum

from definit_db_py.definition.definition import Definition


class Track(StrEnum):
    DATA_STRUCTURES = "data_structures"


_track_to_definitions: dict[Track, list[Definition]] = {
    Track.DATA_STRUCTURES: [],
}


def get_track_list(track: Track) -> list[Definition]:
    return _track_to_definitions[track]
