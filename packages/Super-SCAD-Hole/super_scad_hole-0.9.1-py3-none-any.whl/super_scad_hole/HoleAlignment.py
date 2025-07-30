from enum import auto, Enum, STRICT


class HoleAlignment(Enum, boundary=STRICT):
    """
    Enumeration for how to position a hole vertically.
    """
    # ------------------------------------------------------------------------------------------------------------------
    BOTTOM = auto()
    """
    The bottom of the hole is at the xy-plane.
    """

    CENTER = auto()
    """
    The middle of the hole is a the xy-plane. 
    """

    TOP = auto()
    """
    The top of the hole is at the xy-plane.
    """

# ----------------------------------------------------------------------------------------------------------------------
