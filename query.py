import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("database.db")
tup = ()
cur = con.cursor()
email = "a@gmail.com"  # just giving email and password in-case if doesn't work
password = "123"
# The result of a "cursor.execute" can be iterated over by row
#
# cur.execute("DELETE FROM scores_model WHERE score=1;")
# con.commit()
str = "Concatenation of strings in Python can be performed using:"
cur.execute("DELETE FROM question_model WHERE question='str';")
con.commit()
# for row in cur.execute("SELECT question, answer FROM question_model;"):
#     tup+=(row,)
#
# print(tup)
# new_tup = ()
# for row in cur.execute("SELECT question, option1, option2, option3, option4 FROM question_model;"):
#     new_tup += (row,)
# my_dict = {}
# new_tup2 = ()
# k = 0
# for i in range(len(new_tup)):
#     for j in range(1, 5):
#         new_tup2 += (new_tup[i][j],)
#
#     my_dict[new_tup[i][k]] = new_tup2
#     new_tup2 = ()
# print(my_dict)


# cur.execute("DELETE FROM register_model WHERE email=''")
# con.commit()
# list = []
# i = 0
# for row in cur.execute('SELECT email, password from register_model;'):
#     list.append(row)
#
# j = 0
# p = 1
# for i in range(len(list)):
#     print(list[i][j], list[i][p])

for row in cur.execute("SELECT * FROM scores_model;"):
    print(row)
# Be sure to close the connection
con.close()