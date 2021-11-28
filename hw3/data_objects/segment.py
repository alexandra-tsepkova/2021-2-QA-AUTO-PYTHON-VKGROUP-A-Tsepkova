import faker

fake = faker.Faker()


class Segment:
    def __init__(self):
        self.segment_id = None
        self.data_json = {
            "name": fake.lexify(text="??????????? ???????????"),
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": "remarketing_player",
                    "params": {"type": "positive", "left": 365, "right": 0},
                }
            ],
            "logicType": "or",
        }

    @property
    def id(self):
        return self.segment_id

    @id.setter
    def id(self, segment_id):
        self.segment_id = segment_id
