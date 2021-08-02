
from database import db
class controller():

    def isAdmin(uname, psw):
        # return True
        query = "SELECT * FROM adminusers WHERE username='"+uname+"' AND password='"+psw+"'"
        print("HI ", query)
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False

    def getPlaces():
        query = "SELECT adminregion2, adminregion1 FROM districts ORDER BY adminregion2, adminregion1"
        resultSet = db.raw_query(query)
        out = []
        for r in resultSet: out.append(r[0] + ' , '+ r[1])
        return out
    
    def getPlaceData():
        resultSet = db.raw_query("SELECT * FROM districts ORDER by adminregion2")
        out = {}
        for r in resultSet:
            out['district'] = r[1]
            out['state'] = r[0]
            out['lat'] = r[2]
            out['longi'] = r[3]
        return out
    
    def getUNESCOPlaces():
        query = "SELECT name,average_cases FROM unesco_sites, recent_covid_data WHERE unesco_sites.id = recent_covid_data.id ORDER BY average_cases LIMIT 5"
        resultSet = db.raw_query(query)
        out = {}
        for r in resultSet: out[r[0]] = float("{:.2f}".format(r[1])) 
        return out

    def safePath(src_district, dest_district):
        out = []
        #return ['Ajmer', 'Udaipur']
        src_string = "'" + str(src_district) + "')"
        dest_string = "'" + str(dest_district) + "')"
        query1 = ('WITH RECURSIVE paths (src_id, dst_id, distpath,casepath,hops,activecases) AS( ' 
        'SELECT graph.source_id, graph.dest_id, array[district1.adminregion2, district2.adminregion2], array[data1.average_cases,data2.average_cases],1, 0.0 '
        'FROM graph, districts AS district1, districts AS district2, recent_covid_data AS data1, recent_covid_data AS data2 '
        'WHERE district1.id = graph.source_id AND district2.id = graph.dest_id '
        'AND data1.id = district1.id AND data2.id = district2.id '
        'AND graph.source_id = (SELECT id FROM districts WHERE adminregion2 = ') + src_string
        query2 = ('AND data2.average_cases < 1000 '
        'UNION SELECT paths.src_id, graph.dest_id, paths.distpath||districts.adminregion2,paths.casepath||recent_covid_data.average_cases ,1+ hops,activecases+recent_covid_data.average_cases '
        'FROM paths, graph, districts, districts AS district1, districts AS district2, recent_covid_data '
        'WHERE districts.id = graph.dest_id AND recent_covid_data.id = districts.id '
        'AND paths.dst_id = graph.source_id AND NOT districts.adminregion2 = ANY(paths.distpath) '
        'AND district1.id = graph.source_id AND district2.id = (SELECT id FROM districts WHERE adminregion2 = ') + dest_string
        query3 = " AND paths.activecases <= 5000 AND (recent_covid_data.average_cases < 1000 OR districts.adminregion2 = " + dest_string
        query4 = (' AND districts.lat <= GREATEST(district1.lat, district2.lat)'
        'AND districts.lat >= LEAST(district1.lat, district2.lat) '
        'AND districts.long <= GREATEST(district1.long, district2.long) ' 
        'AND districts.long >= LEAST(district1.long, district2.long)) '
        'SELECT distpath, casepath FROM paths WHERE paths.src_id = (SELECT id FROM districts WHERE adminregion2 = ') + src_string
        query5 = " AND paths.dst_id = (SELECT id FROM districts WHERE adminregion2 = " + dest_string + " LIMIT 1"
        query = query1 + query2 + query3 + query4 + query5
        resultSet = db.raw_query(query)
        dict = {}
        for i in range(len(resultSet[0][1])):
            # print(resultSet[0][1][i])
            dict[resultSet[0][0][i]] = float("{:.2f}".format(resultSet[0][1][i]))
            # dict[resultSet[0][0][i]] = resultSet[0][1][i]

        # print(resultSet[0][0])
        # print(dict)
        return resultSet[0][0],dict
    #return out

    def popularDest(count = 5):
        query = "SELECT adminregion2,average_cases FROM (SELECT adminregion2,average_cases FROM user_data, districts, recent_covid_data WHERE user_data.dest_id = districts.id AND recent_covid_data.id = districts.id) AS R1 GROUP BY adminregion2,average_cases ORDER BY COUNT(adminregion2) DESC LIMIT " + str(count)
        resultSet = db.raw_query(query)
        out = {}
        for r in resultSet: out[r[0]] = float("{:.2f}".format(r[1])) 
        return out

    def safestStates(count = 5):
        query = "SELECT adminregion1 as state, AVG(average_cases) AS average_cases FROM (SELECT adminregion1, adminregion2, average_cases FROM districts, recent_covid_data WHERE districts.id = recent_covid_data.id) AS R1 GROUP BY adminregion1 ORDER BY AVG(R1.average_cases) LIMIT " + str(count)
        resultSet = db.raw_query(query)
        out = {}
        for r in resultSet: out[r[0]] = float("{:.2f}".format(r[1])) 
        return out
    
    def getNewsHeading(count = 5):
        query = "SELECT tag, heading FROM news LIMIT " + str(count)
        resultSet = db.raw_query(query)
        out = {}
        for r in resultSet: out[r[0]] = r[1] 
        return out
        # news = {}
        # news['Coronavirus LIVE'] = "Maharashtra sees nearly 48,000 new cases; 9,086 in Pune"
        # news['Coronavirus Lockdown Highlights'] = "Maharashtra sees nearly 48,000 new cases; 9,086 in Pune"
        # news['Coronavirus'] = "Second surge puts children, younger adults at high risk, say experts"
        # return news
    
    def createUser(uname, psw):
        query = "INSERT INTO adminusers (username, password) VALUES ('" + str(uname) +"','" + str(psw) + "');"
        db.raw_query(query)
        return True

    def createPlace(district, state, lat, longi):
        query1 = "INSERT INTO districts (id, adminregion2, adminregion1, lat, long) VALUES ("
        query2 = "1 +" + " (SELECT MAX(id) FROM districts)" + "," + "'" + str(district) + "'" + "," + "'" + str(state) + "'" + "," + str(lat) + "," + str(longi)
        query3 = ")"
        query = query1 + query2 + query3
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False

    def createNews(newsTag, newsHeading,newsDetails):
        query = "INSERT INTO news (tag, heading) VALUES ('" + str(newsTag) +"','" + str(newsHeading) + "');"
        print(query)
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False
    
    def createUnesco(unesco_site_name, district, state):
        query1 = "INSERT INTO unesco_sites (name, id) VALUES ('" + str(unesco_site_name) + "', (SELECT id FROM districts WHERE adminregion2 = '"
        query2 = str(district) + "'))"
        query = query1 + query2
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False
    
    def insertActiveCases(district, active_cases, active_cases_date):
        query1 = "INSERT INTO covid_data (id,active,updated) VALUES ((SELECT id FROM districts WHERE adminregion2='" + str(district) + "'),"
        query2 = str(active_cases) + "," + "'" + str(active_cases_date) + "')"
        query = query1 + query2
        print(query)
        r = db.raw_query(query)
        return True
    
    def getPlaceDataList():
        resultSet = db.raw_query("SELECT adminregion2,adminregion1,lat,long FROM districts ORDER BY adminregion2")
        out = []
        for r in resultSet: out.append(r[0])
        return out
    
    def getUserDataList():
        resultSet = db.raw_query("SELECT username FROM adminusers")
        out = []
        for r in resultSet:out.append(r[0])
        return out

    def getUnescoDataList():
        resultSet = db.raw_query("SELECT name FROM unesco_sites")
        out = []
        for r in resultSet:out.append(r[0])
        return out

    def getNewsDataList():
        resultSet = db.raw_query("SELECT tag FROM news")
        out = []
        for r in resultSet:out.append(r[0])
        return out

    def deleteUser(key):
        query = "DELETE FROM adminusers WHERE username='"+key+"'"
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False

    def deleteNews(key):
        query = "DELETE FROM news WHERE tag='"+key+"'"
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False

    def deletePlace(key):
        query = "DELETE FROM districts WHERE adminregion2='"+key+"'"
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False

    def deleteUnesco(key):
        query = "DELETE FROM unesco_sites WHERE name='"+key+"'"
        db.raw_query(query)
        if db.cur.rowcount >= 1:
            return True
        return False



# out = controller.getNewsHeading()
# print(out)
# out = '|'.join(controller.safePath('Panipat', 'Ajmer'))
# print(out)
