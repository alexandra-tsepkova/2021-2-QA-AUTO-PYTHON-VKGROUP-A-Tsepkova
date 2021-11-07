import faker
fake = faker.Faker()


class Campaign:
    def __init__(self, url_id, id_photo, id_photo_small):
        self.campaign_id = None
        self.data_to_delete = [
            {"id": None,
             "status": "deleted"}
        ]
        self.data_json = {
            "name": fake.lexify(text="???? ??? ?????????"),
            "read_only": False,
            "conversion_funnel_id": None,
            "objective": "reengagement",
            "targetings": {
                "split_audience": list(range(1, 11)),
                "sex": [
                    "male",
                    "female"
                ],
                "age": {
                    "age_list": [0] + list(range(12, 76)),
                    "expand": True
                },
                "geo": {
                    "regions": [
                        188
                    ]
                },
                "interests_soc_dem": [],
                "segments": [],
                "interests": [],
                "fulltime": {
                    "flags": [
                        "use_holidays_moving",
                        "cross_timezone"
                    ],
                    "mon": list(range(0, 24)),
                    "tue": list(range(0, 24)),
                    "wed": list(range(0, 24)),
                    "thu": list(range(0, 24)),
                    "fri": list(range(0, 24)),
                    "sat": list(range(0, 24)),
                    "sun": list(range(0, 24)),
                },
                "pads": [
                    102659
                ],
                "mobile_types": [
                    "tablets",
                    "smartphones"
                ],
                "mobile_vendors": [],
                "mobile_operation_systems": [
                    5
                ],
                "mobile_operators": [],
                "mobile_apps": "now"
            },
            "age_restrictions": "12+",
            "date_start": None,
            "date_end": None,
            "autobidding_mode": "second_price_mean",
            "budget_limit_day": None,
            "budget_limit": None,
            "mixing": "fastest",
            "utm": None,
            "enable_utm": False,
            "price": "1.06",
            "max_price": "0",
            "package_id": 861,
            "banners": [
                {
                    "urls": {
                        "primary": {
                            "id": url_id
                        }
                    },
                    "textblocks": {
                        "title_25": {
                            "text": fake.lexify(text="???????")
                        },
                        "text_90": {
                            "text": fake.sentence()
                        },
                        "cta_apps_full": {
                            "text": "install"
                        }
                    },
                    "content": {
                        "image_1080x607": {
                            "id": id_photo
                        },
                        "icon_300x300_app": {
                            "id": id_photo_small
                        }
                    },
                    "name": ""
                }
            ]
        }

    @property
    def id(self):
        return self.campaign_id

    @id.setter
    def id(self, campaign_id):
        self.campaign_id = campaign_id
        self.data_to_delete[0]["id"] = campaign_id
