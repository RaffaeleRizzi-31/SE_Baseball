from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeams():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    SELECT 
                         id,
                         year,
                         team_code,
                         name 
                    FROM 
                        team
                    WHERE 
                        year  >= 1980; 
                """

        cursor.execute(query)

        for row in cursor:
            if row["year"] not in result:
                result[row["year"]] = []
                result[row["year"]].append(Team(row["id"], row["year"],row["team_code"], row["name"]))
            else:
                result[row["year"]].append(Team(row["id"], row["year"],row["team_code"], row["name"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_peso_archi(anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    SELECT  
                        team_id, 
                        SUM(salary) as salarioTeam 
                    FROM 
                        salary
                    WHERE 
                        year = %s
                    GROUP BY 
                        team_id
                    ORDER BY 
                        team_code ASC
                """

        cursor.execute(query, (anno,))

        for row in cursor:
            result[row["team_id"]] = row["salarioTeam"]

        cursor.close()
        conn.close()
        return result