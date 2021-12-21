import faker

fake = faker.Faker()

login1 = "administrator"
password1 = "administrator"
normal_login = lambda: fake.lexify(text="?????????????")
normal_password = lambda: fake.lexify(text="??????")
normal_email = fake.email
wrong_format_login = lambda: fake.lexify(text="???")
wrong_format_email = lambda: fake.lexify(text="??????")


db_user = "test_qa"
db_password = "qa_test"
db_name = "myapp"
db_host = "0.0.0.0"
db_port = 3306
db_table = "test_users"
