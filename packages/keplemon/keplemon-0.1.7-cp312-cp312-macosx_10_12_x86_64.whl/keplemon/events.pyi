# flake8: noqa
from keplemon.time import Epoch

class CloseApproach:
    epoch: Epoch
    """UTC epoch of the close approach"""

    primary_id: int
    """Satellite ID of the primary body in the close approach"""

    secondary_id: int
    """Satellite ID of the secondary body in the close approach"""

    distance: float
    """Distance between the two bodies in **_kilometers_**"""

class CloseApproachReport:
    """
    Args:
        start: CA screening start time
        end: CA screening end time
        distance_threshold: Distance threshold for CA screening in **_kilometers_**
    """

    close_approaches: list[CloseApproach]
    """List of close approaches found during the screening"""

    distance_threshold: float
    def __init__(self, start: Epoch, end: Epoch, distance_threshold: float) -> None: ...
