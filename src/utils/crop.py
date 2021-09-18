import numpy as np


def crop(src: np.ndarray, left: int, right: int, top: int, bottom: int) -> np.ndarray:
    """
    Crop Image

    :param np.ndarray src: Source image
    :param int left: left border
    :param int right: right border
    :param int top: top border
    :param int bottom: bottom border
    :return np.ndarray: Cropped image
    """
    return src[top:-bottom-1, left:-right-1]
