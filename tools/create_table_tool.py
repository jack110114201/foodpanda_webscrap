import psycopg2
from config.db_config import config

class TableCreator:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            # Read connection parameters
            params = config()

            # Connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred during connection:", error)

    def create_table(self, sql_statement_path):
        try:
            self.connect()

            # Read SQL script from file
            with open(sql_statement_path, 'r') as file:
                sql_script = file.read()

            # Create a cursor and execute the statement
            cur = self.conn.cursor()
            cur.execute(sql_script)
            self.conn.commit()
            print(f'Create Table Success with {sql_statement_path}')
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')
if __name__ == '__main__':
    TableCreator()