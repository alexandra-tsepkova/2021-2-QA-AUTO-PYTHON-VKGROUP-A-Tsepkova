from locators import dashboard_locators
from pages.page import Page


class DashboardPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login()

    def create_campaign(self, path_to_pic, url_for_campaign, campaign_name):
        # click on create new campaign button
        self.click(dashboard_locators.CREATE_NEW_CAMPAIGN)

        # set campaign aim
        self.click(dashboard_locators.CAMPAIGN_AIM)

        # input url of the advertised item
        input_url_window = self.find(dashboard_locators.INPUT_URL)
        input_url_window.send_keys(url_for_campaign)

        # input campaign name
        self.click(dashboard_locators.CLOSE_POPUP)
        input_name_window = self.find_complex_elem(
            dashboard_locators.CAMPAIGN_NAME,
            dashboard_locators.INPUT_CAMPAIGN_NAME,
            is_input=True,
        )
        input_name_window.click()
        input_name_window.send_keys(campaign_name)

        # upload banner pic
        elements = self.driver.find_elements(*dashboard_locators.LOAD_PIC_FIELD)
        elements[1].send_keys(path_to_pic)

        # save banner
        self.click(dashboard_locators.SUBMIT_BANNER_BUTTON)

        # save campaign
        self.click(dashboard_locators.SAVE_CAMPAIGN)
