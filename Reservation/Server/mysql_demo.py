import mysql.connector
import hashlib


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yourpassword",
  database = "users"
)


mycursor = mydb.cursor()

#CREATE TABLE 
mycursor.execute("CREATE TABLE restauranta_book (id INT AUTO_INCREMENT PRIMARY KEY, customer VARCHAR(255), timeslot VARCHAR(255), seats INT)") 

#mycursor.execute("CREATE TABLE login_token (id INT AUTO_INCREMENT PRIMARY KEY, token VARCHAR(255), timestamp VARCHAR(255), res_id INT)") 

#mycursor.execute("CREATE TABLE restaurantA_timeslot (id INT AUTO_INCREMENT PRIMARY KEY, timeslot VARCHAR(255), available INT)") 

#sql = "INSERT INTO restaurants (restaurant_name, address) VALUES (%s, %s)"
#val = ("RestaurantB", "Helsinki")
#mycursor.execute(sql, val)

#salt = "_76dwDOPNiui"
#sql = "INSERT INTO login_info (username, password,res_id) VALUES (%s, %s,%s)"
#password_with_salt = "passwordRestaurantB"+salt
#password = hashlib.sha256(password_with_salt.encode()).hexdigest()
#val = ("restaurantB", password,1)
#mycursor.execute(sql, val)
#mydb.commit()

# mycursor.execute("SELECT company_name, address FROM basic_info")

#myresult = mycursor.fetchall()

# for x in myresult:
  # print(x) 
  # print(type(x))


