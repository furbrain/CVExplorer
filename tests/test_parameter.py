from unittest import TestCase

from functions import ParamType

FIXTURES_FILTER_HTML = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
FIXTURES_FRAGMENT_HTML = "fixtures/filter_fragment.html"


class TestParameterTemplate(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ParamType.initialise()

