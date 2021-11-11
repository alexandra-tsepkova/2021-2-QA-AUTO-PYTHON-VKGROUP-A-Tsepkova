from selenium.common.exceptions import NoSuchElementException

from locators import segment_locators
from pages.page import Page


class SegmentPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login()
        self.click(segment_locators.SEGMENT_BUTTON)

    def create_segment(self, segment_name):
        # click on create segment button
        # depends on whether we created segments before
        try:
            self.click(segment_locators.CREATE_NEW_SEGMENT)
        except NoSuchElementException:
            try:
                self.click(segment_locators.SUBMIT_BUTTON)
            except NoSuchElementException:
                raise

        # set conditions for segment and submit them
        self.click(segment_locators.CHECKBOX)
        self.click(segment_locators.CREATE_SEGMENT_BUTTON)

        # input segment name
        segment_name_input = self.find_complex_elem(
            segment_locators.SEGMENT_NAME_CLASS,
            segment_locators.SEGMENT_NAME_INPUT,
            is_input=True,
        )
        segment_name_input.send_keys(segment_name)

        # click on create segment button
        self.click(segment_locators.SUBMIT_BUTTON)

    def delete_segment(self, locator):
        # get id of deleted segment using name
        segment_to_delete = self.find(locator)
        segment_id = segment_to_delete.get_attribute("href").split("/")[-1]

        # scroll right to load delete buttons
        self.scroll_right(segment_locators.SCROLL_HANDLER)

        # click delete button and confirm
        self.click(segment_locators.segment_delete_cross(segment_id))
        self.click(segment_locators.CONFIRM_REMOVE)

        self.wait_for_load()
