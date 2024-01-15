# MySQL Exercises

This guide contains a series of exercises to help you practice MySQL commands and queries. Each exercise is accompanied by SQL commands and explanations.

## Table of Contents

1. [Exercise 1: Database Setup](#exercise-1-database-setup)
2. [Exercise 2: SQL Queries](#exercise-2-sql-queries)
3. [Exercise 3: User Permissions](#exercise-3-user-permissions)

---

### Exercise 1: Database Setup

**1. Copy the SQL Script to the Container Volume:**

   First, copy the SQL script file from your host machine to a location within the container's volume. You can use the `docker cp` command to do this. Replace `container_name` with the actual name of your MySQL container:

   ```bash
   docker cp /home/parallels/Downloads/computer_mysql_scripts.sql container_name:/path/in/container
   ```

   For example:

   ```bash
   docker cp /home/parallels/Downloads/computer_mysql_scripts.sql mysql_container:/scripts.sql
   ```

**2. Create a New Database and Import SQL:**

   To create a new database named "Computer_Firm" and import the SQL file "computer_mysql_scripts.sql," you can use the following commands in a MySQL command-line interface or a MySQL client like phpMyAdmin:

   ```sql
   CREATE DATABASE Computer_Firm;
   USE Computer_Firm;
   SOURCE /path/to/computer_mysql_scripts.sql;
   ```

   Replace "/path/to/computer_mysql_scripts.sql" with the actual file path to your SQL file.

**3. Observe Table Structure:**

   To observe the tables in the database and draw the relationships and fields between these four tables, you would need to examine the structure of the tables in the "Computer_Firm" database. You can use the following SQL commands to list the tables and describe their structures:

   ```sql
   SHOW TABLES;
   ```

   For each table listed, you can use the following command to describe its structure:

   ```sql
   DESCRIBE table_name;
   ```

   Replace "table_name" with the actual name of each table listed. Based on the information obtained from these commands, let's draw the relationships and fields between these tables:

   **Laptop Table:**
   - Fields:
     - `code` (Primary Key): An integer identifier for the laptop.
     - `model`: The model name of the laptop.
     - `speed`: The speed (performance) of the laptop.
     - `ram`: The amount of RAM in the laptop.
     - `hd`: The size of the hard drive in the laptop.
     - `price`: The price of the laptop.
     - `screen`: The size of the laptop's screen.

   **PC Table:**
   - Fields:
     - `code` (Primary Key): An integer identifier for the PC.
     - `model`: The model name of the PC.
     - `speed`: The speed (performance) of the PC.
     - `ram`: The amount of RAM in the PC.
     - `hd`: The size of the hard drive in the PC.
     - `cd`: The type of optical drive (e.g., CD-ROM) in the PC.
     - `price`: The price of the PC.

   **Printer Table:**
   - Fields:
     - `code` (Primary Key): An integer identifier for the printer.
     - `model`: The model name of the printer.
     - `color`: Indicates whether the printer is color or not (usually 'Y' for Yes or 'N' for No).
     - `type`: The type of the printer (e.g., laser, inkjet).
     - `price`: The price of the printer.

   **Product Table:**
   - Fields:
     - `manufacturer`: The manufacturer of the product (commonly a company name).
     - `model` (Primary Key): The model name of the product.
     - `type`: The type of the product (generic description).

   Now, let's describe the relationships between these tables:

   - There is no explicit foreign key relationship provided in the table descriptions. However, based on the common fields (e.g., `model`) between tables, it's possible to infer some relationships:

     - The `model` field appears to be used as a reference between tables, linking products in the Product table to their respective models in the Laptop, PC, and Printer tables. This suggests that there is an implicit relationship between the Product table and the other three tables based on the `model` field.

     - To establish a formal relationship, you would typically create foreign keys in the Laptop, PC, and Printer tables that reference the `model` field in the Product table.

### Exercise 2: SQL Queries

**1. List all printer manufacturers, making sure not to list the same manufacturer more than once.**

   ```sql
   SELECT DISTINCT manufacturer FROM Product WHERE type = 'Printer';
   ```

**2. Select the model number, speed, and hard drive capacity for all the PCs with prices below $500.**

   ```sql
   SELECT model, speed, hd
   FROM PC
   WHERE price < 500;
   ```

**3. Find the model number, RAM, and screen size of the laptops with prices over $1000.**

   ```sql
   SELECT model, ram, screen
   FROM Laptop
   WHERE price > 1000;
   ```

**4. List all of the color printer models.**

   ```sql
   SELECT model
   FROM Printer
   WHERE color = 'Y';
   ```

**5. Find the most expensive printer, list its model and price.**

   ```sql
   SELECT model, price
   FROM Printer
   WHERE price = (SELECT MAX(price) FROM Printer);
   ```

**6. Find the laptop models with speeds lower than the slowest PC.**

   ```sql
   SELECT L.model
   FROM Laptop L
   WHERE L.speed < (SELECT MIN(speed) FROM PC);
   ```

**7. List all information about the laptops with models that start with the number 17.**

   ```sql
   SELECT *
   FROM Laptop
   WHERE model LIKE '17%';
   ```

**8. List the model number, speed, RAM, hard disk drive capacity, and price for all available computers (PCs and laptops) in one set.**

   ```sql
   SELECT model, speed, ram, hd, price
   FROM PC
   UNION ALL
   SELECT model, speed, ram, hd, price
   FROM Laptop;
   ```

**9. List the manufacturer and speed for all laptops having HDD capacity equal to or greater than 10 GB.**

   ```sql
   SELECT P.manufacturer, L.speed
   FROM Laptop L
   JOIN Product P ON L.model = P.model
   WHERE L.hd >= 10;
   ```

**10. Find out the models and prices for all the products (of any type) produced by manufacturer B.**

Way to achieve the desired result by using `COALESCE` along with `LEFT JOIN` to retrieve the prices from multiple tables ('PC,' 'Laptop,' and 'Printer').:


```sql
SELECT Product.model, COALESCE(PC.price, Laptop.price, Printer.price) AS price
FROM Product 
LEFT JOIN PC ON Product.model = PC.model 
LEFT JOIN Laptop ON Product.model = Laptop.model 
LEFT JOIN Printer ON Product.model = Printer.model 
WHERE manufacturer = 'B' AND (PC.price IS NOT NULL OR Laptop.price IS NOT NULL OR Printer.price IS NOT NULL);
```


**11. List the highest-priced PCs for each manufacturer.**

   ```sql
	SELECT P.manufacturer, PC.model, PC.price
	FROM PC
	JOIN Product P ON PC.model = P.model
	WHERE (P.manufacturer, PC.price) IN (
    SELECT P2.manufacturer, MAX(PC2.price) AS max_price
    FROM PC PC2
    JOIN Product P2 ON PC2.model = P2.model
    WHERE P2.manufacturer = P.manufacturer
    GROUP BY P2.manufacturer
	);

   ```

**12. Update the prices of all PCs from model 1232 to be $100 higher than their current prices.**

   ```sql
   UPDATE PC
   SET price = price + 100
   WHERE model = '1232';
   ```

### Exercise 3: User Permissions

**1. Create a New User with Your Name:**

   You can create a new user with your name using the `CREATE USER` command. Replace 'your_username' with your desired username and 'your_password' with your desired password.

   ```sql
   CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
   ```

**2. Give Your User Permissions to View All Information from the Computer_Firm Database:**

   To grant your user permissions to view all information from the 'Computer_Firm' database, you can use the `GRANT` command. Replace 'your_username' with your username and 'Computer_Firm' with the database name.

   ```sql
   GRANT SELECT ON Computer_Firm.* TO 'your_username'@'localhost';
   ```

**3. Use the SHOW Command to Check Your User's Permissions:**

   You can use the `SHOW GRANTS` command to check the permissions granted to your user.

   ```sql
   SHOW GRANTS FOR 'your_username'@'localhost';
   ```

**4. Log into the Database with Your User and Do a Query to Verify Permissions:**

   Exit the MySQL shell if you are currently logged in and log in with your newly created user:

   ```bash
   mysql -u your_username -p
   ```

   Then, execute a query to verify that you can select information from the 'Computer_Firm' database:

   ```sql
   USE Computer_Firm;
   SELECT * FROM TableName; -- Replace TableName with the specific table you want to query.
   ```

**5. Log Back In with Root and Remove the Permissions Granted to Your User:**

   Exit the MySQL shell and log back in as the MySQL root user:

   ```bash
   mysql -u root -p
   ```

   To revoke the permissions granted to your user, use the `REVOKE` command:

   ```sql
   REVOKE SELECT ON Computer_Firm.* FROM 'your_username'@'localhost';
   ```

**6. Try to SELECT Information Again with Your User:**

   Log in with your user and try to select information from the 'Computer_Firm' database again. You should receive an error indicating that you don't have permission.

**7. Delete Your User:**

   To delete your user, you can use the `DROP USER` command:

   ```sql
   DROP USER 'your_username'@'localhost';
   ```

   This will remove your user from the MySQL system.

Please make sure to replace 'your_username' and 'your_password' with your actual username and password when executing the commands. Additionally, be cautious when granting and revoking permissions, especially in a production environment.







