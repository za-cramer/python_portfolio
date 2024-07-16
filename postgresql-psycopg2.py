## Working with PSYCOPG2 package to write Postgresql database tables ## 
import psycopg2
conn = psycopg2.connect(dbname="postgres", user="postgres", password = 'XXXX')
cursor = conn.cursor()
cursor.execute("CREATE TABLE notes(id integer PRIMARY KEY, body text, title text)")

# Insert 10 rows of data into the 'notes' table
data_to_insert = [
    (1, "Body of note 1", "Title of note 1"),
    (2, "Body of note 2", "Title of note 2"),
    (3, "Body of note 3", "Title of note 3"),
    (4, "Body of note 4", "Title of note 4"),
    (5, "Body of note 5", "Title of note 5"),
    (6, "Body of note 6", "Title of note 6"),
    (7, "Body of note 7", "Title of note 7"),
    (8, "Body of note 8", "Title of note 8"),
    (9, "Body of note 9", "Title of note 9"),
    (10, "Body of note 10", "Title of note 10")
]

insert_statement = """
    INSERT INTO notes (id, body, title)
    VALUES (%s, %s, %s)
"""

for row in data_to_insert:
    cursor.execute(insert_statement, row)
conn.commit()    
cursor.execute("SELECT * from notes")
results = cursor.fetchall() 
print(results)
conn.close()
