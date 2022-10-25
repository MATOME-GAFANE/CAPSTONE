# Kagiso Yako
# 31/08/2022
# Class for executing high level sqlite instructions and database interaction and management.

import sqlite3
from SQL_queries import SQL_queries
import Google_data


class DB_manager:
    def __init__(self, DB_name, specializations):
        self.DB_name = DB_name
        self.AI_fields = specializations
        self.AI_fields.sort()

    def researchers_per_inst(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        cursor.execute("SELECT Institution, count(Institution) FROM Researchers group by institution " +
                       "order by count(institution) DESC;")
        count_inst = cursor.fetchall()
        institutions = []
        frequencies = []
        for i in range(len(count_inst)):
            institutions.append(count_inst[i][0])
            frequencies.append(count_inst[i][1])
        return institutions, frequencies

    def researchers_per_rating(self, table="Researchers"):
        frequencies = [0, 0, 0, 0, 0]
        ratings = ["A", "B", "C", "P", "Y"]
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = SQL_queries.get_table(table, columns=["Rating", "count(rating)"])
        query += SQL_queries.group_by("Rating")
        cursor.execute(query)
        values = cursor.fetchall()
        for i in range(len(ratings)):
            if values[i][0] is not None:
                frequencies[ratings.index(values[i][0])] = (values[i][1])
        return ratings, frequencies

    def researcher_rating_by_inst(self, institution):
        frequencies = [0, 0, 0, 0, 0]
        ratings = ["A", "B", "C", "P", "Y"]
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = "SELECT rating, count(rating) from researchers WHERE "
        query += SQL_queries.compare_to_other("Institution", "\"" + institution + "\"", "=", )
        query += SQL_queries.group_by("Rating")
        cursor.execute(query)
        values = cursor.fetchall()
        print(values)
        for i in range(len(values)):
            frequencies[ratings.index(values[i][0])] = (values[i][1])

        return ratings, frequencies

    def researchers_per_specialization(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        field_X = []
        num_researchers_Y = []

        for field in self.AI_fields:
            query = "SELECT Count(Surname) FROM Researchers "
            query += "WHERE Specializations LIKE  '%" + field + "%';"

            cursor.execute(query)
            data = cursor.fetchall()

            field_X.append(field)
            num_researchers_Y.append(data[0][0])

        return field_X, num_researchers_Y

    def researcher_dist_by_specialization(self, field):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        ratings = ["A", "B", "C", "P", "Y"]
        rating_distribution = [0] * len(ratings)
        query = "SELECT rating ,Count(Rating) FROM Researchers "
        query += "WHERE Specializations LIKE '%" + field + "%' "
        query += "GROUP BY Rating"

        cursor.execute(query)
        data = cursor.fetchall()
        for i in range(len(data)):
            rating_distribution[ratings.index(data[i][0])] = data[i][1]
        return ratings, rating_distribution

    def specialization_dist_by_inst(self, inst):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        specialization_distribution = []

        for field in self.AI_fields:
            query = "SELECT  Specializations, Count(Specializations) FROM Researchers "
            query += "WHERE Institution LIKE '%" + inst + "%'  AND specializations LIKE %" + field + "% "
            query += "GROUP BY Institution"

            cursor.execute(query)
            data = cursor.fetchall()

            specialization_distribution.append(data)

        return self.AI_fields, specialization_distribution

    def get_researchers(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        query = "SELECT Surname FROM Researchers"

        cursor.execute(query)
        data = cursor.fetchall()

        researchers = []

        for item in data:
            surname = str(item[0])
            researchers.append(surname)

        return researchers

    def get_institutions(self):

        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()

        query = "SELECT DISTINCT Institution FROM Researchers"

        cursor.execute(query)
        data = cursor.fetchall()

        institutions = []

        for item in data:
            surname = str(item[0])
            institutions.append(surname)

        return institutions

    ############

    def primary_research_dist_by_top_inst(self, primary):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        frequency = []
        for primaryResearch in primary:
            query = "SELECT Count(PrimaryResearch) as frequency FROM Researchers WHERE Institution in " \
                    "(SELECT institution from researchers group by institution order by count(*) desc limit 5) " \
                    "and primaryresearch LIKE \"%" + primaryResearch + "%\";"
            cursor.execute(query)
            frequency.append(cursor.fetchone()[0])

        return frequency

    def pie_chart_top_5_vs_rest(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        distribution = []
        cursor.execute("select count(*) from Researchers group by Institution in "
                       "(SELECT institution from researchers group by institution order by count(*) desc limit 5 ) ")
        rows = cursor.fetchall()
        labels = ["Researchers from other institutions", "Researchers from top 5 institutions"]
        distribution.append(rows[0][0])
        distribution.append(rows[1][0])
        return labels, distribution

    def pie_chart_top_5_spec_vs_no_spec(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        distribution = []
        cursor.execute("select count(*) from Researchers group by Institution in "
                       "(SELECT institution from researchers group by institution order by count(*) desc limit 5 ) ")
        rows = cursor.fetchall()
        labels = ["Researchers from other institutions", "Researchers from top 5 institutions"]
        distribution.append(rows[0][0])
        distribution.append(rows[1][0])
        return labels, distribution

    def get_new_researchers(self):
        query = "Select * from Researchers where not exists (SELECT * from PreviousResearchers where " \
                "(PreviousResearchers.Surname = Researchers.Surname" \
                " and PreviousResearchers.Initials = Researchers.Initials))"
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
