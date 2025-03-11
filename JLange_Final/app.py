# module defines an application to curate a playlist
# with a sqlite3 db as a backend for data storage

from helper import helper
import mysql.connector

data = helper.data_cleaner("Athletes.csv")
data1 = helper.data_cleaner("Coaches.csv")
data2 = helper.data_cleaner("Medals.csv")
data3 = helper.data_cleaner("Teams.csv")
data4 = helper.data_cleaner("EntriesGender.csv")
#data5 = helper.data_cleaner("athelete_events.csv")


connection = mysql.connector.connect(
    host = "34.122.238.177", # Public IP address of cloud MySQL instance
    user="root",
    password="j)^33NItR!^*", #root password for cloud MySQL
    database='cpsc408' #database
)
cursor = connection.cursor(buffered = True)
print("connection made..")

#using Mysql functions
#function that execute many insert values to the table
def bulk_insert(query,records):
    cursor.executemany(query,records)
    connection.commit()
    print("query executed..")

# function to return a single value from table
def single_record(query):
    cursor.execute(query)
    return cursor.fetchone()[0]

# function to return a single attribute values from table
def single_attribute(query):
    cursor.execute(query)
    results = cursor.fetchall()
    results = [i[0] for i in results]
    return results
#fuction to return all of the attribute vlues from table
def multiple_attributes(query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results
#function that only executes the query. Used for create
def execute_query(query):
    cursor.execute(query)
    connection.commit()

# close connection
def destructor():
    connection.close()

#The App section
# function inserts data into table if it is empty
def pre_process():
    query = '''
    SELECT COUNT(*)
    FROM Athletes;
    '''
    #if table has no records, input values from the csv file to the table
    result = single_record(query)
    if result == 0:
        attribute_count = len(data[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = "INSERT INTO Athletes (Name,NOC,Discipline) VALUES("+placeholders+");"
        bulk_insert(query,data)

        #creating view tables for later use
        query = "CREATE VIEW group_discipline AS SELECT Discipline, COUNT(*) FROM Athletes GROUP BY Discipline;"
        execute_query(query)
        query = "CREATE VIEW group_country AS SELECT NOC, COUNT(*) FROM Athletes GROUP BY NOC;"
        execute_query(query)

        #num table is used later for joining
        query = "Create Table numAthletes AS (SELECT NOC, COUNT(*) AS Total FROM Athletes GROUP BY NOC);"
        execute_query(query)
    query = '''
    SELECT COUNT(*)
    FROM Teams;
    '''

    result = single_record(query)
    if result == 0:
        attribute_count = len(data3[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = "INSERT INTO Teams (Name,Discipline,NOC,Event) VALUES("+placeholders+");"
        bulk_insert(query,data3)

        #num table is used later for joining
        query = "Create Table numTeams AS (SELECT NOC, COUNT(*) AS Total FROM Teams GROUP BY NOC);"
        execute_query(query)

    query = '''
    SELECT COUNT(*)
    FROM Medals;
    '''

    result = single_record(query)
    if result == 0:
        attribute_count = len(data2[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = "INSERT INTO Medals (Ranking,TeamNOC,Gold,Silver,Bronze,Total,RankByTotal) VALUES("+placeholders+");"
        bulk_insert(query,data2)

        #num table is used later for joining
        query = "Create Table numMedals AS (SELECT NOC, Total FROM Medals);"
        execute_query(query)

    query = '''
    SELECT COUNT(*)
    FROM EntriesGender;
    '''

    result = single_record(query)
    if result == 0:
        attribute_count = len(data4[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = "INSERT INTO EntriesGender (Discipline,Female,Male,Total) VALUES("+placeholders+");"
        bulk_insert(query,data4)

    query = '''
    SELECT COUNT(*)
    FROM Coaches;
    '''

    result = single_record(query)
    if result == 0:
        attribute_count = len(data1[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = "INSERT INTO Coaches (Name,NOC,Discipline,Event) VALUES("+placeholders+");"
        bulk_insert(query,data1)

        #num table is used later for joining
        query = "Create Table numCoaches AS (SELECT NOC, COUNT(*) AS Total FROM Coaches GROUP BY NOC);"
        execute_query(query)


def start_screen():
    print("Welcome to Olympics Dataset!")


# show user options
def options():
    print("Select from the following menu options:\n1 Add new athlete\n" \
    "2 Update an athlete\n3 Delete an athlete info\n4 Search an athlete info" \
    "\n5 Search a Coach info \n6 Search how many athletes per Discipline\n7" \
    " Top Popular Disciplines\n8 Top Popular Represented Countries\n9" \
    " Find Total Gold, silver, and bronze medal earned from country given athlete name" \
    "\n10 Total Athletes, Coaches, Teams, and Medals earned per Country\n11 Exit")
    return helper.get_choice([1,2,3,4,5,6,7,8,9,10,11])
#option 1, function that adds an athelete to the table
def add_athlete():
    name = input("Insert Name:")
    noc = input("Insert NOC:")
    discipline = input("Insert Discipline:")

    query = "INSERT INTO Athletes (Name, NOC, Discipline) VALUES ('"+name+"','"+noc+"','"+discipline+"');"
    execute_query(query)
#option 2 function that updates an athlete row
def update_athlete():
    query ='''
    SELECT DISTINCT Name
    FROM Athletes;
    '''


    name = single_attribute(query)
    choices = {}
    for i in range(len(name)):
        print(i,name[i]) #prints the list of names
        choices[i] = name[i]
    print("Which Name to update from athletes (Enter ID Number):")
    index = helper.get_choice(choices.keys())
    print("Athlete Name: " + choices[index])

    print("Which information do you want to modify?")
    information = ['Name','NOC','Discipline'] # attributes showed to user that can be changed
    choices2 = {}
    for i in range(len(information)):
        print(i,information[i])
        choices2[i] = information[i]
    index2 = helper.get_choice(choices2.keys())

    #series of if statements for each attribute and updates it depending on the user input
    if index2 == 0:
        new_value = input("Enter new name for Athletes' Name: ")
        query = "SELECT athleteID FROM Athletes WHERE Name = \'" + choices[index] +"\'"
        id = single_record(query)
        strid = str(id) #converts int to string since can only concatenate str
        query = "UPDATE Athletes SET Name = \'" + new_value + "\' WHERE athleteID = \'" + strid + "\'"
        execute_query(query)
        print("Successfully Updated...")

    elif index2 == 1:
        new_value = input("Enter new NOC: ")
        query = "SELECT athleteID FROM Athletes WHERE Name = \'" + choices[index] +"\'"
        id = single_record(query)
        strid = str(id)
        query = "UPDATE Athletes SET NOC = \'" + new_value + "\' WHERE athleteID = \'" + strid + "\'"
        execute_query(query)
        print("Successfully Updated...")

    elif index2 == 2:
        new_value = input("Enter new Discipline: ")
        query = "SELECT athleteID FROM Athletes WHERE Name = \'" + choices[index] +"\'"
        id = single_record(query)
        strid = str(id)
        query = "UPDATE Athletes SET Discipline = \'" + new_value + "\' WHERE athleteID = \'" + strid + "\'"
        execute_query(query)
        print("Successfully Updated...")

#option 3 delete an athlete row
def delete_athelete():
    query = '''
    SELECT DISTINCT Name
    FROM Athletes;
    '''
    print("List of Athletes:")
    athletes = single_attribute(query)

    # show athletes in table, also create dictionary for choices
    choices = {}
    for i in range(len(athletes)):
        print(i,athletes[i])
        choices[i] = athletes[i]

    print("Insert ID to delete from record ")
    index = helper.get_choice(choices.keys())
    query = "DELETE FROM Athletes WHERE Name = \'" + choices[index] +"\'"
    execute_query(query)

#option 4, search an athlete given the ID
def search_by_athlete():
    query = '''
    SELECT Name
    FROM Athletes;
    '''
    print("List of Athletes:")
    athletes = single_attribute(query)

    choices = {}
    for i in range(len(athletes)):
        print(i,athletes[i])
        choices[i] = athletes[i]

    print("Which Athlete information do you want to see?")
    print("Enter ID")
    index = helper.get_choice(choices.keys())

    query = "Select * FROM Athletes WHERE Name = \'" + choices[index] +"\'"
    name = multiple_attributes(query)

    for i in range(len(name)):
        print(name[i])
#option 5, search a coach information given the ID
def search_by_coach():
    query = '''
    SELECT Name
    FROM Coaches;
    '''
    print("List of Coaches:")
    athletes = single_attribute(query)

    choices = {}
    for i in range(len(athletes)):
        print(i,athletes[i])
        choices[i] = athletes[i]

    print("Which Coaches information do you want to see?")
    print("Enter ID")
    index = helper.get_choice(choices.keys())

    query = "Select * FROM Coaches WHERE Name = \'" + choices[index] +"\'"
    name = multiple_attributes(query)

    for i in range(len(name)):
        print(name[i])
#option 6, search number of participants for each country given ID
def search_by_gender():
    query = '''
    SELECT Discipline
    FROM EntriesGender;
    '''
    print("List of Entries for each sport:")
    athletes = single_attribute(query)

    choices = {}
    for i in range(len(athletes)):
        print(i,athletes[i])
        choices[i] = athletes[i]

    print("Which Team information do you want to see?")
    print("Enter ID")
    index = helper.get_choice(choices.keys())

    query = "Select * FROM EntriesGender WHERE Discipline = \'" + choices[index] +"\'"
    discipline = multiple_attributes(query)

    print("ID, Discipline, # of Males, # of Females, Total")
    for i in range(len(discipline)):
        print(discipline[i])
#option 7, create a view table to use to view how many atheletes per discipline
def group_by_discipline():
    query = "SELECT * FROM group_discipline;"
    discipline = single_attribute(query)

    choices = {}
    for i in range(len(discipline)):
        print(i,discipline[i])
#option 8, create a view table to use to view how many Athletes participated per country
def group_by_country():
    query = "SELECT * FROM group_country;"
    noc = single_attribute(query)

    # show artists in table, also create dictionary for choices
    choices = {}
    for i in range(len(noc)):
        print(i,noc[i])
#option 9, find total medals earned for the athelete's country
def sub_query():
    query = '''
    SELECT Name
    FROM Athletes;
    '''
    athletes = single_attribute(query)
    choices = {}
    for i in range(len(athletes)):
        print(i,athletes[i])
        choices[i] = athletes[i]
    print("From which Athlete do you want to see their country's total earned medals?")
    print("Enter ID")
    index = helper.get_choice(choices.keys())
    print("From: " + choices[index])
    #sub_query to get the gold, silver, and bronze medals earned in the athelete's country
    query = "SELECT Gold, Silver, Bronze FROM Medals WHERE NOC = (SELECT NOC FROM Athletes WHERE Name = \'" + choices[index] +"\')"
    name = multiple_attributes(query)

    print("Gold earned,Silver earned,Bronze earned")
    for i in range(len(name)):
        print(name[i])
#option 10, joins tables to recieve the total number of people per country
def join():
    query = "Select numAthletes.NOC, numAthletes.Total, numCoaches.Total, numTeams.Total, numMedals.Total FROM (((numAthletes " \
    "INNER JOIN numCoaches ON numAthletes.NOC = numCoaches.NOC) " \
    "INNER JOIN numTeams ON numAthletes.NOC = numTeams.NOC) " \
    "INNER JOIN numMedals ON numAthletes.NOC = numMedals.NOC);"

    join = multiple_attributes(query)

    choices = {}
    print("NOC, Total Athletes, Total Coaches, Total Teams, Total Medals Earned")
    for i in range(len(join)):
        print(join[i])


# main program
pre_process()
start_screen()
while True:
    user_choice = options()
    if user_choice == 1:
        add_athlete()
    elif user_choice == 2:
        update_athlete()
    elif user_choice == 3:
        delete_athelete()
    elif user_choice == 4:
        search_by_athlete()
    elif user_choice == 5:
        search_by_coach()
    elif user_choice == 6:
        search_by_gender()
    elif user_choice == 7:
        group_by_discipline()
    elif user_choice == 8:
        group_by_country()
    elif user_choice == 9:
        sub_query()
    elif user_choice == 10:
        join()
    elif user_choice == 11:
        print("Goodbye")
        break



destructor()
