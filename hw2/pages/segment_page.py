from locators import segment_locators
from pages.page import Page


class SegmentPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login()
        self.click(segment_locators.SEGMENT_BUTTON)
