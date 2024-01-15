# MySQL Database Setup Guide

This guide provides step-by-step instructions for setting up a MySQL database using Docker and performing various database operations. Follow the steps below to get started.

## Table of Contents

1. [Step 1: Download MySQL Docker Image](#step-1-download-mysql-docker-image)
2. [Step 2: Launch MySQL Container](#step-2-launch-mysql-container)
3. [Step 3: Connect To MySQL Database](#step-3-connect-to-mysql-database)
4. [Step 4: List Available Databases](#step-4-list-available-databases)
5. [Step 5: Create a Database](#step-5-create-a-database)
6. [Step 6: Enter Your Newly Created Database](#step-6-enter-your-newly-created-database)
7. [Step 7: Create a Table](#step-7-create-a-table)
8. [Step 8: Add a Default Value Constraint](#step-8-add-a-default-value-constraint)
9. [Step 9: Check Table Structure](#step-9-check-table-structure)
10. [Step 10: Add a Primary Key Constraint](#step-10-add-a-primary-key-constraint)
11. [Step 11: Check Primary Key Constraint](#step-11-check-primary-key-constraint)
12. [Step 12: Add a New Field](#step-12-add-a-new-field)
13. [Step 13: Verify Table Structure](#step-13-verify-table-structure)
14. [Step 14: Add a Constraint on Field](#step-14-add-a-constraint-on-field)
15. [Step 15: Insert New Student](#step-15-insert-new-student)
16. [Step 16: Retrieve All Rows](#step-16-retrieve-all-rows)
17. [Step 17: Create Another Table](#step-17-create-another-table)
18. [Step 18: Rename a Field](#step-18-rename-a-field)
19. [Step 19: Rename a Table](#step-19-rename-a-table)
20. [Step 20: List All Tables](#step-20-list-all-tables)

---

### Step 1: Download MySQL Docker Image

Pull the MySQL image from Docker Hub to your machine.

```bash
$ docker pull mysql:latest
```

### Step 2: Launch MySQL Container

Spin up a MySQL Docker container.

```bash
$ docker run --name mysql -p 3306:3306 -v mysql_volume:/var/lib/mysql/ -d -e "MYSQL_ROOT_PASSWORD=temp123" mysql
```

### Step 3: Connect To MySQL Database

Connect to the MySQL container.

```bash
$ docker exec -it mysql bash
```

Connect to the MySQL database as the root user.

```bash
$ mysql -u root -p
```

### Step 4: List Available Databases

List the available databases using the `SHOW DATABASES;` command.

```sql
SHOW DATABASES;
```

### Step 5: Create a Database

Create a new database named "Infinity."

```sql
CREATE DATABASE Infinity;
```

### Step 6: Enter Your Newly Created Database

Switch to the "Infinity" database using the `USE` command.

```sql
USE Infinity;
```

### Step 7: Create a Table

Create a table named "Students" with specific fields (Name, Age, Class).

```sql
CREATE TABLE Students (
   Name VARCHAR(50),
   Age SMALLINT DEFAULT 18,
   Class VARCHAR(10)
);
```

### Step 8: Add a Default Value Constraint

You've already added the default constraint in the table definition in Step 7.

### Step 9: Check Table Structure

Check the table structure using the `DESCRIBE` or `DESC` command.

```sql
DESCRIBE Students;
```

### Step 10: Add a Primary Key Constraint

Add a primary key constraint on the "Name" column.

```sql
ALTER TABLE Students ADD PRIMARY KEY (Name);
```

### Step 11: Check Primary Key Constraint

After adding the primary key constraint, verify it using the `DESCRIBE` command again.

```sql
DESCRIBE Students;
```

### Step 12: Add a New Field

Add a new field named "Months" to the "Students" table.

```sql
ALTER TABLE Students ADD Months INT;
```

### Step 13: Verify Table Structure

Verify the table structure using the `DESCRIBE Students;` command again.

```sql
DESCRIBE Students;
```

### Step 14: Add a Constraint on Field

Add a constraint to limit the "Months" column to a maximum value of 8.

```sql
ALTER TABLE Students ADD CONSTRAINT CheckMonths CHECK (Months <= 8);
```

### Step 15: Insert New Student

Attempt to insert a new student with values that violate the constraint, and then modify the constraint to allow it.

```sql
-- Attempt to insert (you'll get an error)
INSERT INTO Students (Name, Age, Class, Months) VALUES ('Noam', 25, '110', 9);

-- Modify the constraint to allow higher values
ALTER TABLE Students DROP CONSTRAINT CheckMonths;
ALTER TABLE Students ADD CONSTRAINT CheckMonths CHECK (Months <= 10);

-- Now insert successfully
INSERT INTO Students (Name, Age, Class, Months) VALUES ('Noam', 25, '110', 9);
```

### Step 16: Retrieve All Rows

Retrieve all rows from the "Students" table.

```sql
SELECT * FROM Students;
```

### Step 17: Create Another Table

Create another table named "Alumni" with the same data as "Students" except for the "Months" field.

```sql
CREATE TABLE copyStudents AS
SELECT Name, Age, Class FROM Students;
```

### Step 18: Rename a Field

Rename the "Name" field to "pastStudent" and change its data type.

```sql
ALTER TABLE copyStudents CHANGE Name pastStudent VARCHAR(20);
```

### Step 19: Rename a Table

Rename the "Alumni" table to "copyStudents."

```sql
RENAME TABLE copyStudents TO Alumni;
```

### Step 20: List All Tables

List all tables in the database.

```sql
SHOW TABLES;
```

You have now successfully set up a MySQL database, created tables, and performed various operations on it.
