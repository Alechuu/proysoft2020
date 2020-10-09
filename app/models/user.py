class User(object):
    
    @classmethod
    def all(cls, conn):
        sql = "SELECT * FROM usuario"
        datos = conn.execute(sql)
        return datos.fetchall()

    @classmethod
    def create(cls, conn, data):
        sql = """
            INSERT INTO usuario (email, username, password, activo, first_name, last_name)
            VALUES (%s, %s, %s, %s,1,%s,%s)
        """

        ##cursor = conn.cursor()
        conn.execute(sql, list(data.values()))
        ##conn.commit()

        return True

    @classmethod
    def find_by_email_and_pass(cls, conn, email, password):
        sql = """
            SELECT * FROM usuario AS u
            WHERE u.username = %s AND u.password = %s
        """

        #cursor = conn.cursor()
        
        res = conn.execute(sql, (email, password))
        return res.first()

