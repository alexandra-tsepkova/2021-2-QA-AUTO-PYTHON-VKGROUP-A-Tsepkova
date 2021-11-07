from client import APIClient
import pytest


class TestCampaignAPI(APIClient):

    @pytest.mark.API
    def test_create_campaign(self):
        created_campaign = self.create_campaign()
        latest_created_campaign_id = self.latest_created_campaign()
        assert created_campaign.campaign_id == latest_created_campaign_id

        deleted = self.session.post(
            "https://target.my.com/api/v2/campaigns/mass_action.json",
            headers=self.headers,
            json=created_campaign.data_to_delete,
        )
        assert deleted.status_code == 204

    @pytest.mark.API
    def test_create_segment(self):
        created_segment = self.create_segment()
        last_segment_ids = self.get_list_of_latest_active_segments()
        assert created_segment.segment_id in last_segment_ids

    @pytest.mark.API
    def test_delete_segment(self):
        segment_to_delete = self.create_segment()
        url = "https://target.my.com/api/v1/remarketing/mass_action/delete.json"
        resp = self.session.post(url, headers=self.headers, json=segment_to_delete.data_to_delete)
        successes = resp.json()['successes'][0]
        deleted_id = successes['source_id']
        assert deleted_id == segment_to_delete.segment_id
