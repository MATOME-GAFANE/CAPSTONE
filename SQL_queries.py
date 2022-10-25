# class responsible for the creation of string  sqlite queries to be used by other classes. Not responsible for
# THIS CLASS IS NOT RESPONSIBLE FOR DATABASE INTERACTION only the creation of string sqlite queries.

class SQL_queries:
    @staticmethod
    def delete_table(table_name):
        return "DROP TABLE IF EXISTS " + str(table_name)

    @staticmethod
    def create_table_compound_key(table_name, columns: list, primary_key=None):
        # Adding columns to query
        query = "CREATE TABLE " + table_name + " ("
        for column in columns:
            query += column + " ,"
        query = query[0: len(query) - 1]

        # Adding primary key: Allows for composite key too
        if primary_key is not None:
            # Composite key support
            if all(x in columns for x in primary_key):
                query += ", PRIMARY KEY ("
                for key in primary_key:
                    query += key + " ,"
                query = query[0: len(query) - 1] + ")"
            # simple key/one column support
            else:
                if primary_key in columns:
                    query += ", PRIMARY KEY (" + primary_key + ")"
        return query + ")"

    @staticmethod
    def create_table(table_name, columns: list):
        # Adding columns to query
        query = "CREATE TABLE " + table_name + " ("
        for column in columns:
            query += column + " ,"
        query = query[0: len(query) - 1]
        return query + ")"

    # Method returning insert query. To be used with a list(s) of field values.
    # i.e. cursor.executemany(insert(column_list), recordList) or cursor.executemany(sqlite_insert_query, recordList)
    @staticmethod
    def insert_record(table_name, columns):
        query = "INSERT into " + table_name + " ("
        str_columns = str(columns)
        query += str_columns[1: len(str_columns) - 1] + ") "
        wildcards = len(columns) * "?"
        query += "values (" + wildcards + ");"
        return query

    @staticmethod
    def update_record(table_name, columns, ID, ID_column):
        query = "UPDATE " + table_name + " SET "
        for column in columns:
            query += str(column) + " = ?, "

        query = query[0: len(query) - 2] + " WHERE " + ID_column + " = " + ID + ";"  # removing the last comma
        return query

    @staticmethod
    def delete_record(table_name, ID_column, ID):
        query = "DELETE FROM " + table_name + " WHERE " + ID_column + " = " + ID + ";"
        return query

    @staticmethod
    def get_subset(table_name, columns, operators, column_values=None, conjunction="", negate=False, prefix="",
                   to_one=None, wrap=False):
        query = SQL_queries.get_table(table_name) + " WHERE"
        if column_values is not None:
            skip = 1
            for i in range(len(columns)):
                if wrap:
                    column_values[i] = "\"" + column_values[i] + "\""
                if skip == 1:
                    skip = 0
                    query += SQL_queries.compare_to_other(columns[i], column_values[i], operators[i])
                else:
                    query += SQL_queries.compare_to_other(columns[i], column_values[i], operators[i],
                                                          conjunction=conjunction)
        elif to_one is not None:
            skip = 1
            if wrap:
                to_one = "\"" + to_one + "\""
            for i in range(len(columns)):
                if skip == 1:
                    skip = 0
                    query += SQL_queries.compare_to_other(columns[i], to_one, operators[i], negate=negate,
                                                          prefix=prefix)
                else:
                    query += SQL_queries.compare_to_other(columns[i], to_one,
                                                          operators[i], conjunction="OR", negate=negate, prefix=prefix)
        return query

    @staticmethod
    def delete_subset(table_name, condition, negate=False):
        if negate:
            query = "DELETE FROM " + table_name + " WHERE NOT (" + condition + ");"
        else:
            query = "DELETE FROM " + table_name + " WHERE (" + condition + ");"
        return query

    # PLEASE PASS LIST INSTEAD OF STRING
    @staticmethod
    def get_table(table_name, columns=None, single_column="", DISTINCT=False):
        query = "select "
        if DISTINCT:
            query += "DISTINCT "

        if columns is not None:
            for column in columns:
                query += column + ","
            query = query[0: len(query) - 1]
        elif single_column != "":
            query += single_column
        else:
            query += " *"

        query += " from " + table_name
        return query

    @staticmethod
    def compare_to_other(column, column_value, operator, conjunction="", negate=False, prefix=""):
        if not negate:
            condition = " " + prefix + " " + conjunction + " " + column + " " + operator + " " + str(column_value)
        else:
            condition = " " + prefix + " " + conjunction + " " + column + " NOT " + operator + " " + str(column_value)
        return condition

    @staticmethod
    def between_range(column, lower_bound, upper_bound, conjunction="", negation=False):
        if not negation:
            condition = conjunction + " " + column + " BETWEEN " + lower_bound + " AND " + upper_bound
        else:
            condition = conjunction + " NOT " + column + " BETWEEN " + lower_bound + " AND " + upper_bound

        return condition

    @staticmethod
    def count_records(table_name, Distinct=False, columns=None, single_column="", other_column=""):
        query = "SELECT COUNT("
        if Distinct:
            query += "DISTINCT "

        if columns is not None and not Distinct:
            for column in columns:
                query += column + ", "
            query = query[0: len(query) - 2] + ") "
        elif single_column != "":
            query += single_column + ") "
        else:
            if not Distinct:
                query += "*) "
        if other_column != "":
            query += ", " + other_column + " "

        query += "FROM " + table_name
        return query

    @staticmethod
    def group_by(column):
        group_by = " GROUP BY " + column
        return group_by

    @staticmethod
    def count(column):
        return "COUNT (" + column + ")"

    @staticmethod
    def order_by(column, order=""):
        add_on = " ORDER BY " + column + " " + order
        return add_on

    # Useful for whenever we are dealing with the institutions table
    @staticmethod
    def institutions_table():
        query = "SELECT Institutions.institution , Institutions.location, count(*) as \"NumberofResearchers\" " \
                "from Institutions INNER JOIN Researchers on Institutions.Institution = Researchers.institution "
        return query

    @staticmethod
    def institutions_table_search_query(value):
        columns = ["Institutions.institution", " Institutions.location"]
        query = SQL_queries.institutions_table() + " WHERE "
        skip = 1
        for i in range(len(columns)):
            if skip == 1:
                query += " " + columns[i] + " LIKE " + "\"%" + value + "%\""
                skip = 0
            else:
                query += " OR " + columns[i] + " LIKE " + "\"%" + value + "%\""
        query += " GROUP BY Institutions.institution "
        return query

    @staticmethod
    def clean_data(specializations, table="Researchers"):
        condition = "SecondaryResearch LIKE \"%Artificial Intelligence%\" OR PrimaryResearch " \
                    "LIKE \"%Artificial Intelligence%\""
        for spec in specializations:
            wrapped_spec = "\"%" + spec + "%\""
            condition += SQL_queries.compare_to_other("Specializations", wrapped_spec, operator="LIKE",
                                                      conjunction="OR")
        query = SQL_queries.delete_subset(table, condition, negate=True)
        query = query[0:len(query)-1] + " or (SecondaryResearch is NULL or Specializations is NULL)"
        return query
