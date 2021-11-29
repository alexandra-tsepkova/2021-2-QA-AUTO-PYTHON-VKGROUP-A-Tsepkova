import pytest

from client import APIClient


class TestCampaignAPI(APIClient):
    @pytest.mark.API
    def test_create_campaign(self):
        created_campaign = self.create_campaign()
        latest_created_campaign_id = self.latest_created_campaign()
        assert created_campaign.campaign_id == latest_created_campaign_id
        status_code_after_delete = self.delete_campaign(created_campaign)
        assert status_code_after_delete == 204

    @pytest.mark.API
    def test_create_segment(self):
        created_segment = self.create_segment()
        last_segment_ids = self.get_list_of_latest_active_segments()
        assert created_segment.segment_id in last_segment_ids

    @pytest.mark.API
    def test_delete_segment(self):
        segment_to_delete = self.create_segment()
        status_code_after_delete = self.delete_segment(segment_to_delete)
        assert status_code_after_delete == 204
