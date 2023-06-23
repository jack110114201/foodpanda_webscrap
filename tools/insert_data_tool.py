import psycopg2
import csv
from config.db_config import config

class DataInserter:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred during connection:", error)
    
    def execute_query(self, query, values):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
        except psycopg2.Error as error:
            print("Error occurred during query execution:", error)
    
    def insert_data(self, table_name, data_path, column_names, conflict_columns, update_columns=None):
        try:
            self.connect()
            with open(data_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                for row in reader:
                    placeholders = ', '.join(['%s'] * len(column_names))
                    conflict_placeholders = ', '.join(k for k in conflict_columns)

                    if update_columns:
                        update_placeholders = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_columns])
                        query = f"INSERT INTO {table_name} ({', '.join(column_names)})\
                                  VALUES ({placeholders})\
                                  ON CONFLICT ({conflict_placeholders})\
                                  DO UPDATE SET {update_placeholders};"
                    else:
                        query = f"INSERT INTO {table_name} ({', '.join(column_names)})\
                                  VALUES ({placeholders})\
                                  ON CONFLICT ({conflict_placeholders})\
                                  DO NOTHING;"
                    
                    values = tuple(row[column_names.index(col)] for col in column_names)
                    self.execute_query(query, values)

            self.conn.commit()
            print(f'Data {table_name} insertion {values} completed successfully.')

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred during data insertion:", error)

            if self.conn is not None:
                self.conn.rollback()

        finally:
            if self.conn is not None:
                self.conn.close()
                #print('Database connection closed.')
    def insert_consumer_data(self, table_name, consumer_data, column_names, conflict_columns, update_columns=None):
        try:
            self.connect()
            placeholders = ', '.join(['%s'] * len(column_names))
            conflict_placeholders = ', '.join(k for k in conflict_columns)
            if update_columns:
                update_placeholders = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_columns])
                query = f"INSERT INTO {table_name} ({', '.join(column_names)})\
                          VALUES ({placeholders})\
                          ON CONFLICT ({conflict_placeholders})\
                          DO UPDATE SET {update_placeholders};"
            else:
                query = f"INSERT INTO {table_name} ({', '.join(column_names)})\
                          VALUES ({placeholders})\
                          ON CONFLICT ({conflict_placeholders})\
                          DO NOTHING;"
            data_adr_values = tuple(consumer_data.get(col) for col in column_names)
            self.execute_query(query, data_adr_values)

            self.conn.commit()
            print(f'Data {table_name} insertion {data_adr_values} completed successfully.')

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error occurred during data insertion:", error)

            if self.conn is not None:
                self.conn.rollback()

        finally:
            if self.conn is not None:
                self.conn.close()
                #print('Database connection closed.')
if __name__ == '__main__':
    DataInserter()