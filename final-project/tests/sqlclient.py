import allure
import pymysql
import pytest
import settings


class MysqlClient:

    connection = None

    def connect(self, db_created=True):
        self.connection = pymysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            db=settings.db_name if db_created else None,
            charset="utf8",
            autocommit=True,
        )

    def recreate_db(self):
        self.connect(db_created=False)
        self.connection.query(f"DROP database if exists {settings.db_name}")
        self.connection.query(f"CREATE database {settings.db_name}")
        self.connection.close()

    @pytest.fixture(autouse=True)
    def db(self):  # setup client
        self.recreate_db()
        self.connect()
        self.create_table()
        insert_query = f"""
            INSERT into `test_users`(username, password, email, access, active)
            VALUES ("{settings.login1}", "{settings.password1}", "admin@admin.com", 1, 0);
        """
        self.connection.query(insert_query)
        yield self.connection
        self.connection.close()

    def create_table(self):
        query = """CREATE TABLE `test_users` (
                    `id` int NOT NULL AUTO_INCREMENT,
                    `username` varchar(16) DEFAULT NULL,
                    `password` varchar(255) NOT NULL,
                    `email` varchar(64) NOT NULL,
                    `access` smallint DEFAULT NULL,
                    `active` smallint DEFAULT NULL,
                    `start_active_time` datetime DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `email` (`email`),
                    UNIQUE KEY `ix_test_users_username` (`username`)
                );"""
        self.connection.query(query)

    def check_database(self, name, parameter, expected_cond):
        cursor = self.connection.cursor()
        cursor.execute(
            f"select {parameter} from `{settings.db_table}` where username='{name}' ;"
        )
        res = cursor.fetchall()
        assert len(res) == 1
        with allure.step(
            f"check if user named {name} has {parameter} set to {expected_cond}"
        ):
            assert res[0] == (expected_cond,)

    def check_if_in_database(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"select * from `{settings.db_table}` where username='{name}' ;")
        res = cursor.fetchall()
        with allure.step(f"check if user named {name} is in database"):
            if len(res) == 0:
                return False
            else:
                return True
