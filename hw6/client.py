import pymysql


class MysqlClient:
    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = "127.0.0.1"
        self.port = 3306
        self.connection = None

    def connect(self, db_created=True):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db_name if db_created else None,
            charset="utf8",
            autocommit=True,
        )

    def recreate_db(self):
        self.connect(db_created=False)
        self.connection.query(f"DROP database if exists {self.db_name}")
        self.connection.query(f"CREATE database {self.db_name}")
        self.connection.close()
