# https://replit.com/@henryprosser/Databases-Lab-32#main.py #

# This program enables management of employees' data for ABC company. Simply run the program and choose an option from the list provided #

from tabulate import tabulate
import sqlite3

class DBOperations:
  # SQL operations
  sql_create_table = "CREATE TABLE employee (ID INTEGER UNSIGNED, Title VARCHAR(20), Forename VARCHAR(20), Surname VARCHAR(20), EmailAddress CHAR(1), Salary INTEGER UNSIGNED)"
  sql_select_all = "SELECT * from employee"
  sql_search = "SELECT * FROM employee where ID = ?"
  sql_delete_all = "DELETE FROM employee"
  sql_drop_table = "DROP TABLE IF EXISTS employee"
 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("EmployeesABC.db")
      self.cur = self.conn.cursor()
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("EmployeesABC.db")
    self.cur = self.conn.cursor()

  # Function to create table
  def create_table(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table)
      print("Table created successfully")
    except Exception:
      print("This table is already created")
    finally:
      self.conn.close()

  # Insert data in the table
  def insert_data(self):
    try:
      self.get_connection()

      emp = Employee()
      while True:
        try:
          employeeID = int(input("Enter Employee ID: "))
          emp.set_employee_id(employeeID)
          break
        # Check for invalid input
        except ValueError:
          print("Invalid input. Please enter a positive integer.")

      self.cur.execute("SELECT * FROM employee where ID = ?", (employeeID,))
      result = self.cur.fetchall()
      # Checks for duplicate employee ID
      if result:
        print('Error! EmployeeID already exists')
      else:
        emp.set_employee_title(input("Enter Title: "))
        emp.set_forename(input("Enter Forename: "))
        emp.set_surname(input("Enter Surname: "))
        emp.set_email(input("Enter Email: "))

        while True:
          try:
            emp.set_salary(int(input("Enter Salary: ")))
            break
          except ValueError:
            print("Invalid input. Please enter a positive integer.")

        self.conn.execute("INSERT INTO employee (ID,Title,Forename,Surname,EmailAddress,Salary)VALUES (?, ?, ?, ?, ?, ?)",(emp.employeeID,emp.empTitle,emp.forename,emp.surname,emp.email,emp.salary))
        self.conn.commit()
        print("Inserted the following row successfully")
        self.cur.execute("SELECT * FROM employee")
        print(self.cur.fetchall()[-1])

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Select all data to be viewed
  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      # Fetch all employee records
      results = self.cur.fetchall()
      # Create headings
      headings = ['EmployeeID', 'Title', 'Forename', 'Surname', 'Email Address', 'Salary']
      # Print the database
      print("\n")
      print(tabulate(results, headers=headings))

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
  # Search database for a given employee
  def search_data(self):
    try:
      self.get_connection()
      while True:
        try:
          employeeID = int(input("Enter Employee ID: ")) 
          break
        except ValueError:
          print("Invalid input. Please enter a positive integer.")

      self.cur.execute("SELECT * FROM employee where ID = ?", (employeeID,))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        # Loop to print employee details
        for index, detail in enumerate(result):
          if index == 0:
            print("\nEmployee ID: " + str(detail))
          elif index == 1:
            print("Employee Title: " + detail)
          elif index == 2:
            print("Employee Name: " + detail)
          elif index == 3:
            print("Employee Surname: " + detail)
          elif index == 4:
            print("Employee Email: " + detail)
          else:
            print("Salary: "+ str(detail))
      else:
        print ("No Record")
  
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Update data for a given employee
  def update_data(self):
    col_list = ['Title', 'Forename', 'Surname', 'EmailAddress', 'Salary']
    try:
      self.get_connection()
      employeeID = int(input("Enter the EmployeeID for the record you want to update: "))
      while True:
        column = input("Enter the column you want to update from the following list [Title, Forename, Surname, EmailAddress, Salary]: ")
        # Check if input is a valid column name
        if column in col_list:
          break
        else:
          print("Column does not exist. Please try again.")
        
      entry = input("Enter the updated entry: ")

      # Update the given entry
      result = self.conn.execute("UPDATE employee SET {} = ? WHERE ID = ?".format(column), (entry, employeeID))

      self.cur.execute("SELECT * FROM employee where ID = ?", (employeeID,))

      if result.rowcount != 0:
        print("\nUpdated the following row successfully:")
        print(self.cur.fetchone())
        self.conn.commit()
        print (str(result.rowcount)+ " Row(s) affected.")
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

# Delete record for a given employee
  def delete_data(self):
    try:
      self.get_connection()
      while True:
        try:
          employeeID = int(input("Enter the EmployeeID for the record you want to delete: ")) 
          break
        except ValueError:
          print("Invalid input. Please enter a positive integer.")

      self.cur.execute("SELECT * FROM employee where ID = ?", (employeeID,))
      
      # Delete the given entry
      result = self.conn.execute("DELETE FROM employee WHERE ID = ?", (employeeID,))
      
      if result.rowcount != 0:
        print("\nDeleted the following row successfully:")
        print(self.cur.fetchone())
        self.conn.commit()
        print (str(result.rowcount)+ " Row(s) affected.")
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally: 
      self.conn.close()

  # Delete all records
  def delete_all_records(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_delete_all)

      confirm = None 
      while confirm not in ("y", "n"): 
        confirm = input("Are you sure you want to delete all records? (y/n): ")
        if confirm == "y":
          self.conn.commit()
          print("\nAll records deleted sucessfully")
          print(self.cur.fetchall())
        elif confirm == "n":
          self.conn.close()
        else:
          print("Invalid response. Please enter 'y' for yes or 'n' for no")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Delete entire table
  def delete_table(self):
    try:
      self.get_connection()
      confirm = None
      while confirm not in ("y","n"):
        confirm = input("Are you sure you want to delete the table? (y/n): ")
        if confirm == "y":
          self.cur.execute(self.sql_drop_table)
          print("\nTable deleted succesfully")
        elif confirm == "n":
          self.conn.close()
        else:
          print("Invalid response. Please enter 'y' for yes or 'n' for no")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

    
class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary
  
  def get_employee_id(self):
    return self.employeeId

  def get_employee_title(self):
    return self.empTitle
  
  def get_forename(self):
    return self.forename
  
  def get_surname(self):
    return self.surname
  
  def get_email(self):
    return self.email
  
  def get_salary(self):
    return self.salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)


# The main function will parse arguments. 
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
  
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeesABC")
  print (" 2. Insert data into EmployeesABC")
  print (" 3. Select/view all data in EmployeesABC")
  print (" 4. Search an employee")
  print (" 5. Update data (to update a record)")
  print (" 6. Delete data (to delete a record)")
  print (" 7. Delete all records")
  print (" 8. Delete table")
  print (" 9. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    db_ops.delete_all_records()
  elif __choose_menu == 8:
    db_ops.delete_table()
  elif __choose_menu == 9:
    print("You have quit. Goodbye! \n")
    exit(0)
  else:
    print ("Invalid Choice")



