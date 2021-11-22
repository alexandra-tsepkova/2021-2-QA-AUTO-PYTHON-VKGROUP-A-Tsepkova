import pytest

from client import MysqlClient


@pytest.fixture(scope="session", autouse=True)
def c():  # setup client
    c = MysqlClient("root", "pass", "TEST_SQL")
    c.recreate_db()
    c.connect()
    return c


@pytest.fixture(scope="session", autouse=True)
def lines():  # setup file data
    f = open("access.log", "r")
    return f.readlines()


class TestSQL:
    def test_num_all_queries(self, c, lines):
        num_queries = """
            CREATE TABLE `num_queries` (
              `id` smallint(6) NOT NULL AUTO_INCREMENT,
              `num` int,
              PRIMARY KEY (`id`)
            )
        """

        c.connection.query(num_queries)

        insert_query = f"""
                INSERT into `num_queries`(num)
                VALUES ("{str(len(lines))}");
        """
        c.connection.query(insert_query)
        assert c.connection.query("select * from `num_queries`;") == 1

    #####################################
    def test_num_queries_by_type(self, c, lines):
        num_queries_2 = """
            CREATE TABLE `queries by type` (
              `id` smallint(6) NOT NULL AUTO_INCREMENT,
              `method` char(10),
              `num` int,
              PRIMARY KEY (`id`)
            )
        """

        c.connection.query(num_queries_2)

        methods = {
            "GET": 0,
            "HEAD": 0,
            "POST": 0,
            "PUT": 0,
            "PATCH": 0,
            "DELETE": 0,
            "CONNECT": 0,
            "OPTIONS": 0,
            "TRACE": 0,
        }
        for m, v in methods.items():
            for string in lines:
                if '"' + m in string:
                    methods[m] += 1
        for m, v in methods.items():
            insert_query = f"""
                INSERT into `queries by type`(method, num)
                VALUES ("{m}", "{v}");
            """
            c.connection.query(insert_query)

        assert c.connection.query("select * from `queries by type`;") == len(methods)

    #########################################

    def test_times_most_visited_urls(self, c, lines):
        num_queries_3 = """
            CREATE TABLE `most visited urls` (
              `id` smallint(6) NOT NULL AUTO_INCREMENT,
              `url` char(255),
              `times` int,
              PRIMARY KEY (`id`)
            )
        """

        c.connection.query(num_queries_3)

        times_visited_urls = {}
        for line in lines:
            url = line.split()[6]
            if url in times_visited_urls.keys():
                times_visited_urls[url] += 1
            else:
                times_visited_urls[url] = 1
        for res in sorted(times_visited_urls.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]:
            insert_query = f"""
            INSERT into `most visited urls` (url, times)
            VALUES ("{res[0]}", "{res[1]}");
        """
            c.connection.query(insert_query)

        assert c.connection.query("select * from `most visited urls`;") == 10

    ###################################################

    def test_num_biggest_sizes_4xx_queries(self, c, lines):
        num_queries_4 = """
            CREATE TABLE `biggest 4xx queries` (
              `id` smallint(6) NOT NULL AUTO_INCREMENT,
              `ip` char(20),
              `url` char(255),
              `status_code` smallint(3),
              `size` int,
              PRIMARY KEY (`id`)
            )
        """

        c.connection.query(num_queries_4)

        queries = []
        for line in lines:
            status_code = line.split()[8]
            ip = line.split()[0]
            url = line.split()[6]
            size = line.split()[9]
            if int(status_code) // 100 == 4:
                queries.append(ip + " " + url + " " + status_code + " " + size)

        for string in sorted(queries, key=lambda x: int(x.split()[-1]), reverse=True)[
            :5
        ]:
            res = string.split()
            insert_query = f"""
                INSERT into `biggest 4xx queries` (ip, url, status_code, size)
                VALUES ("{res[0]}", "{res[1]}", "{res[2]}", "{res[3]}");
            """
            c.connection.query(insert_query)

        assert c.connection.query("select * from `biggest 4xx queries`;") == 5

    ####################################################

    def test_ips_most_frequent_5xx_queries(self, c, lines):
        num_queries_5 = """
            CREATE TABLE `top 5xx queries` (
              `id` smallint(6) NOT NULL AUTO_INCREMENT,
              `ip` char(20),
              `times` int,
              PRIMARY KEY (`id`)
            )
        """

        c.connection.query(num_queries_5)

        queries_5xx = {}
        for line in lines:
            status_code = line.split()[8]
            ip = line.split()[0]
            if int(status_code) // 100 == 5:
                if ip in queries_5xx.keys():
                    queries_5xx[ip] += 1
                else:
                    queries_5xx[ip] = 1

        for res in sorted(queries_5xx.items(), key=lambda x: x[1], reverse=True)[:5]:
            insert_query = f"""
            INSERT into `top 5xx queries` (ip, times)
            VALUES ("{res[0]}", "{res[1]}");
        """
            c.connection.query(insert_query)

        assert c.connection.query("select * from `top 5xx queries`;") == 5
