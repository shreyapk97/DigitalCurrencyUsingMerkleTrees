import sqlite3
conn = sqlite3.connect('participants_db.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE PARTICIPANT_BALANCE 
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         BALANCE            INT     NOT NULL);''')
print("Table created successfully")
conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (1, 'a', 2000)");
conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (2, 'b', 5000)");
conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (3, 'c', 3000)");

conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (4, 'd', 6000)");
conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (5, 'e', 7000)");
conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (6, 'f', 8000)");
conn.execute("INSERT INTO PARTICIPANT_BALANCE (ID,NAME,BALANCE) \
      VALUES (7, 'g', 8000)");

conn.commit()
print("Records created successfully");
conn.close()


