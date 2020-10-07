class User(object):
    @classmethod
    def all(cls, conn):
        sql = "SELECT * FROM users"
        #cursor = conn.cursor()
        #conn.execute(sql)
        #cursor.fetchall()
        return conn.execute(sql)

    @classmethod
    def create(cls, conn, data):
        sql = """
            INSERT INTO users (email, password, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """

        ##cursor = conn.cursor()
        conn.execute(sql, list(data.values()))
        ##conn.commit()

        return True

    @classmethod
    def find_by_email_and_pass(cls, conn, email, password):
        sql = """
            SELECT * FROM users AS u
            WHERE u.email = %s AND u.password = %s
        """

        #cursor = conn.cursor()
        
        res = conn.execute(sql, (email, password))
        return res.first()

