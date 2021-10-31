from selenium.webdriver.common.by import By

from settings import segment_name_for_delete, segment_name_for_input

SEGMENT_BUTTON = (By.XPATH, "//a[@href='/segments']")
CREATE_NEW_SEGMENT = (By.XPATH, "//a[@href='/segments/segments_list/new/']")
CHECKBOX = (By.CLASS_NAME, "adding-segments-source__checkbox")
CREATE_SEGMENT_BUTTON = (By.CLASS_NAME, "adding-segments-modal__btn-wrap")
SEGMENT_NAME_CLASS = (By.CLASS_NAME, "input_create-segment-form")
SEGMENT_NAME_INPUT = (By.TAG_NAME, "input")
SUBMIT_BUTTON = (By.CLASS_NAME, "button_submit")
SEGMENT_LIST_TABLE_NAME_COLUMN = (
    By.XPATH,
    "//div[starts-with(@class, 'cells-module-nameCell')]",
)
SEGMENT_LIST_CREATED_SEGMENT = (By.XPATH, f"//a[@title='{segment_name_for_input}']")
SEGMENT_ELEMENT_TO_DELETE = (By.XPATH, f"//a[@title='{segment_name_for_delete}']")
SCROLL_HANDLER = (By.CLASS_NAME, "custom-scroll__handler")
CONFIRM_REMOVE = (By.CLASS_NAME, "button_confirm-remove")


def segment_delete_cross(segment_id):
    return By.XPATH, f"//div[starts-with(@data-test, 'remove-{segment_id}')]"
