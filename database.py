import psycopg2

class database():
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.con = psycopg2.connect(
            host=self.host,
            database= self.database,
            user= self.user, 
            password=self.password)
        self.cur = self.con.cursor()
    
    def raw_query(self, query):
        self.cur.execute(query)
        try:
            retSet = self.cur.fetchall()
            return retSet
        except Exception as e:
            return None
        
        
    
    def getCityList(self, query):
        cityList = []
        self.cur.execute(query)
        retSet = self.cur.fetchall()
        for r in retSet:cityList.append(r[0])
        return cityList


    def close(self):
        self.cur.close()
        self.con.close()


db = database("localhost", "covid","postgres","govind")
# db.raw_query("SELECT adminregion1 FROM districts")

# db.close()
