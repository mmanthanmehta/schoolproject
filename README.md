# schoolproject


set up mysql


Set up MySQL Database and User
Once MySQL is running, you need to create a database and a user with appropriate permissions. You can do this via MySQL command line or a graphical interface like MySQL Workbench.

Using MySQL Command Line:


#mysql -u root -p

Enter your root password when prompted.


#CREATE DATABASE bookstore;
#CREATE USER 'yourusername'@'localhost' IDENTIFIED BY 'yourpassword';
#GRANT ALL PRIVILEGES ON <database-name>.* TO 'yourusername'@'localhost';
#FLUSH PRIVILEGES;

Replace 'yourusername' and 'yourpassword' with your desired username and password.


https://chatgpt.com/c/690fdd3d-9519-45bd-b6d6-a57f88ae2d56
