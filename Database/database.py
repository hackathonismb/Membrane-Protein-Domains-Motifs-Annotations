import mysql.connector

from getpass import getpass
from mysql.connector import connect, Error
import json


def main():
    try:
        with connect(
                host="localhost",
                user='root',
                password=getpass("Enter password: "),
                database="pandos"
        ) as connection:
            conn = connection.cursor()
            create_tables(conn)  # creates database and all tables (only used once to initialize)
            # drop_all_tables(cursor)

            # show_all_tables()  # debugging
            # display_table_schema('uniprot_t')
            # display_table_schema('pdb_t')
            # display_table_schema('pdb_chains_t')
            # display_table_schema('pdb_chains_data_t')
            #
            # json_to_db('Json_output')
            # query("""SELECT * FROM uniprot_t LIMIT 5""", conn)
            # drop_all_tables(connection.cursor())

            # insert_data_to_uniprot_table() # pass in list

    except Error as e:
        print(e)

########################################################################


def create_tables(cursor):

    create_db_query = """CREATE DATABASE pandos;"""
    query(create_db_query, cursor)
    create_uniprot_table_query = """
    CREATE TABLE uniprot_t ( 
        uniprot_t_id INT AUTO_INCREMENT NOT NULL UNIQUE,
        uniprot_id VARCHAR(10) NOT NULL UNIQUE,
        /* Entery_status VARCHAR(20), */
        uniprot_seq VARCHAR(35000) NOT NULL,
        PRIMARY KEY (uniprot_t_id)
    );
    """

    create_pdb_table_query = """
    CREATE TABLE pdb_t (
        pdb_t_id INT AUTO_INCREMENT NOT NULL UNIQUE,
        pdb_id VARCHAR(20),
        uniprot_t_id INT NOT NULL UNIQUE,
        PRIMARY KEY (pdb_t_id), /* open to suggestions for renaming */
        FOREIGN KEY (uniprot_t_id) REFERENCES uniprot_t(uniprot_t_id)
);
        """

    create_pdb_chains_table_query = """
    CREATE TABLE pdb_chains_t ( /* chains or chain? */
        pdb_chains_t_id INT AUTO_INCREMENT NOT NULL UNIQUE,
        pdb_t_id INT NOT NULL UNIQUE,
        chain TEXT,
        pdbsequence TEXT,
        PRIMARY KEY (pdb_chains_t_id),
        FOREIGN KEY (pdb_t_id) REFERENCES pdb_t(pdb_t_id)
    );
            """

    create_pdb_chains_data_table_query = """
    CREATE TABLE pdb_chains_data_t (
        pdb_chains_data_t_id INT AUTO_INCREMENT NOT NULL UNIQUE,
        pdb_chains_t_id INT NOT NULL UNIQUE,
        head_domain TEXT,
        hinge_domain TEXT,
        stalk_domain TEXT,
        neck_domain TEXT,
        transmembrane TEXT,
        cytoplasmic TEXT,
        PRIMARY KEY (pdb_chains_data_t_id),
        FOREIGN KEY (pdb_chains_t_id) REFERENCES pdb_chains_t(pdb_chains_t_id)
    );
            """

    with connect(
            host="localhost",
            user='root',
            password=getpass("Enter password: "),,
            database="pandos"
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
            cursor.execute(create_uniprot_table_query)
            cursor.execute(create_pdb_table_query)
            cursor.execute(create_pdb_chains_table_query)
            cursor.execute(create_pdb_chains_data_table_query)
            connection.commit()


def drop_all_tables(cursor):
    query("DROP TABLE pdb_chains_data_t;", cursor)
    query("DROP TABLE pdb_chains_t;", cursor)
    query("DROP TABLE pdb_t;", cursor)
    query("DROP TABLE uniprot_t;", cursor)
    query("DROP DATABASE pandos;", cursor)


########################################################################

def display_table_schema(table_name: str):
    show_table_query = "DESCRIBE " + table_name

    with connect(
            host="localhost",
            user='root',
            password=getpass("Enter password: "),,
            database="pandos"
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            result = cursor.fetchall()  # Fetch rows from last executed query
            print("Displaying " + table_name + " Table Schema:")
            for row in result:
                print(row)
            print("\n")


def show_all_tables():
    show_tables_query = "SHOW TABLES;"

    with connect(
            host="localhost",
            user='root',
            password=getpass("Enter password: "),,
            database="pandos"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(show_tables_query)
            result = cursor.fetchall()

            print("Showing all tables")
            for row in result:
                print(row)
            print("\n")

def insert_data_to_uniprot_table(uniprot_id, uniprot_seq): # uniprot_ID(accession #), Entery_status, uniprot_seq
    insert_uniprot_query = """
        INSERT INTO uniprot_t
        (uniprot_id, uniprot_seq)
        VALUES (%s, %s, %s, %s)
    """

    uniprot_records = [  # todo: change to list later
        (1, 2, 3, 4)
    ]

    with connect(
            host="localhost",
            user='root',
            password=getpass("Enter password: "),,
            database="pandos"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_uniprot_query, uniprot_records)
            connection.commit()


# def insert_data_to_uniprot_table(records: list): # uniprot_ID(accession #), Entery_status, uniprot_seq
#     insert_uniprot_query = """
#         INSERT INTO uniprot_t
#         (uniprot_ID, uniprot_seq)
#         VALUES (%s, %s, %s, %s)
#     """
#
#     uniprot_records = [  # todo: change to list later
#         (1, 2, 3, 4)
#     ]
#
#     with connect(
#             host="localhost",
#             user='root',
#             password=getpass("Enter password: "),,
#             database="pandos"
#     ) as connection:
#         with connection.cursor() as cursor:
#             cursor.executemany(insert_uniprot_query, uniprot_records)
#             connection.commit()


def json_to_db(file_name: str):
    uniprot_t_data = []
    pdb_t_data = []
    uniprot_t_data = []
    uniprot_t_data = []

    with open(file_name + '.json') as json_file:
        data = json.load(json_file)
        for protein_entry in data:
            uniprot_t_data.append((protein_entry['Uniprot_ID'],
                                   protein_entry['Uniprot_seq']))
            pdb_t_data.append(protein_entry['PDB_ID'])
            # insert_data_to_uniprot_table(protein_entry['Uniprot_ID'],
            #                              protein_entry['Uniprot_seq'])

        insert_data_to_uniprot_table(uniprot_t_data)
        # insert_data_to_pdb_table(pdb_t_data) # write this
        # insert_data_to_uniprot_table_next one...


def query(query: str, conn):
    # with connection.cursor() as cursor:
    with conn.cursor() as cursor:
        cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)


if __name__ == '__main__':
    main()

