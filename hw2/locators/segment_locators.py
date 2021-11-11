from selenium.webdriver.common.by import By

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
SCROLL_HANDLER = (By.CLASS_NAME, "custom-scroll__handler")
CONFIRM_REMOVE = (By.CLASS_NAME, "button_confirm-remove")


def segment_element(segment_name):
    return By.XPATH, f"//a[@title='{segment_name}']"


def segment_delete_cross(segment_id):
    return By.XPATH, f"//div[starts-with(@data-test, 'remove-{segment_id}')]"
