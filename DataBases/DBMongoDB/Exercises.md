# Exercise 1

### 1. Install and Run MongoDB

#### Step 1: Create Compose File

To install and run MongoDB using Docker, follow these steps:

1. Create a `docker-compose.yml` file in Visual Studio Code.
2. Paste the following snippet into the file:

```yaml
version: '3.7'

services:
  mongodb-Cont:
    image: mongo:latest
    container_name: mongoDB-Cont
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    ports:
      - 27017:27017
    volumes:
      - mongodb_data_cont:/data/db

volumes:
  mongodb_data_cont:
```

In the provided code:

- "version" specifies the Docker Compose file version as "3.7".
- "services" lists the MongoDB service configuration.
- "mongodb-Cont" is the MongoDB service name.
- "image" specifies the Docker image as "mongo:latest".
- "container_name" sets the container name to "mongoDB-Cont".
- "environment" defines environment variables for the MongoDB container (username and password).
- "ports" maps port 27017 from the host to the container.
- "volumes" creates a volume named "mongodb_data_cont" to persist MongoDB data.

#### Step 2: Start the Compose Service

Execute the following command to start the MongoDB services defined in the compose file:

```bash
docker-compose up -d
```

This command starts the MongoDB server in detached mode.

### 2. Start MongoDB Shell

To open a Bash shell inside the running MongoDB container and connect to the MongoDB server, use the following command and enter the password when prompted:

```bash
docker exec -it mongoDB-Cont bash
mongosh admin -u root -p root
```

### 3. Display Available Databases

In the MongoDB shell, use the `show dbs` command to display the available databases.

### 4. Create Administrative User

To create an administrative user with the highest privileges, switch to the `admin` database using the `use admin` command. Then, create the user with the following command:

```javascript
db.createUser({
  user: "admin",
  pwd: "admin",
  roles: [{ role: "root", db: "admin" }]
})
```

### 5. Log in with Administrative User

Exit the MongoDB shell using `exit` and log back in using the administrative user you just created:

```bash
mongosh -u admin -p admin_password --authenticationDatabase admin
```

### 6. Create New Database

To create a new database named `students`, use the `use students` command.

### 7. Create Collection

Within the `students` database, create a collection named `DevOps` using the `db.createCollection()` method:

```javascript
db.createCollection("DevOps")
```

### 8. List Collections

To display the list of collections in the current database, use the `show collections` command.

### 9. Insert Document

Insert a document representing a student into the `DevOps` collection with the keys `Name`, `Age`, and `City`. For example:

```javascript
db.DevOps.insertOne({ Name: "Roy Bidani", Age: 25, City: "Beer-Sheva" })
```

### 10. Display Document

To display the information you just added to the `DevOps` collection, use the `find()` method:

```javascript
db.DevOps.find()
```

### 11. Make Displayed Information Readable

MongoDB's default output format may not be very readable. To display documents in a more readable format, use the `pretty()` method:

```javascript
db.DevOps.find().pretty()
```

### 12. Insert Multiple Documents

To insert two more documents as an array into the `DevOps` collection, use the `insertMany()` method:

```javascript
db.DevOps.insertMany([
  { Name: "Alice Smith", Age: 23, City: "Los Angeles" },
  { Name: "Bob Johnson", Age: 27, City: "Chicago" }
])
```

### 13. Delete First Added Student

To delete the first added student, use the `deleteOne()` method:

```javascript
db.DevOps.deleteOne({ Name: "John Doe" })
```

### 14. Delete Collection

To delete the `DevOps` collection, use the `drop()` method:

```javascript
db.DevOps.drop()
```

### 15. Delete Database

To delete the `students` database, switch to the `students` database and use the `db.dropDatabase()` method:

```javascript
use students
db.dropDatabase()
```

# Exercise 2

### 1. Import the restaurants.json Database

To import the `restaurants.json` file into MongoDB:

- Copy the "restaurants.json" file from your local machine to the container:

```bash
docker cp /home/parallels/Downloads/restaurants.json mongoDB-Cont:/home/
```

- From outside the MongoDB CLI, use the `mongoimport` tool to import the `restaurants.json` file into the `test` database and the `restaurants` collection:

```bash
mongoimport --db test --collection restaurants --file /home/restaurants.json --authenticationDatabase admin -u admin -p admin
```

### 2. Query Fields

To display the `restaurant_id`, `name`, `borough`, and `cuisine` fields for all documents in the `restaurants` collection, use the `find()` method with projection:

```javascript
db.restaurants.find({}, { restaurant_id: 1, name: 1, borough: 1, cuisine: 1 })
```

### 3. Restaurants in the Bronx

To display all restaurants in the borough of Bronx, use the `find()` method with a query filter:

```javascript
db.restaurants.find({ borough: "Bronx" })
```

### 4. First 5 Restaurants in the Bronx

To display the first 5 restaurants in the Bronx, chain the `limit()` method after the `find()` query:

```javascript
db.restaurants.find({ borough: "Bronx" }).limit(5)
```

### 5. Restaurants with Score 80-100

To find restaurants with a score of more than 80 but less than 100, use the `$gt` (greater than) and `$lt` (less than) operators:

```javascript
db.restaurants.find({ "grades.score": { $gt: 80, $lt: 100 } })
```

### 6. Special Restaurants Query

To find restaurants that do not prepare "American" cuisine, have achieved a grade of "A," and do not belong to the borough of "Brooklyn," use a query like this:

```javascript
db.restaurants.find({
  cuisine: { $ne: "American" }, // Filter restaurants where cuisine is not "American"
  "grades.grade": "A", // Filter restaurants with at least one grade of "A"
  borough: { $ne: "Brooklyn" } // Filter restaurants not located in "Brooklyn" borough
}).sort({
  cuisine: -1 // Sort the results in descending order based on cuisine
})
```

### 7. Restaurants with Names Starting with "Wil"

To find restaurants with names starting with "Wil," use a regular expression query:

```javascript
db.restaurants.find({ name: /^Wil/ }, { restaurant_id: 1, name: 1, borough: 1, cuisine: 1 })
```

### 8. Restaurants in Specific Boroughs

To find restaurants that belong to the boroughs of "Staten Island," "Queens," "Bronx," or "Brooklyn," use the `$in` operator:

```javascript
db.restaurants.find(
  { borough: { $in: ["Staten Island", "Queens", "Bronx", "Brooklyn"] } },
  { restaurant_id: 1, name: 1, borough: 1, cuisine: 1 }
)
```

# Exercise 3

To create a MongoDB replica set with one primary and two secondaries using Docker Compose, follow these steps:

1. Generate a key file (if you haven't already) using the following command:

```bash
openssl rand -base64 756 > mongodb-keyfile
chmod 600 mongodb-keyfile
```

Ensure that the key file (`mongodb-keyfile`) is in the same directory as your Docker Compose file or specify the correct path to it.

2. Update your Docker Compose file to include the `--keyFile` option for each MongoDB node. Here's an example modification to your Docker Compose file:

```yaml
version: '3.7'

services:
  # Primary MongoDB Node
  mongodb-Cont-primary:
    image: mongo:latest
    container_name: mongoDB-Cont-primary
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    ports:
      - 27017:27017
    volumes:
      - mongodb_data_cont:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile  # Bind mount the key file
    command: 
      - bash
      - -c
      - "ls /etc/mongodb-keyfile && mongod --auth --keyFile /etc/mongodb-keyfile --bind_ip_all --replSet rs0"  # Specify the replica set name and key file

  # Secondary MongoDB Node 1
  mongodb-Cont-secondary1:
    image: mongo:latest
    container_name: mongoDB-Cont-secondary1
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    volumes:
      - mongodb_data_cont_secondary1:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile  # Bind mount the key file
    depends_on:
      - mongodb-Cont-primary  # Ensure primary node is up first
    command:
      - bash
      - -c
      - "ls /etc/mongodb-keyfile && mongod --auth --keyFile /etc/mongodb-keyfile --bind_ip_all --replSet rs0"

  # Secondary MongoDB Node 2
  mongodb-Cont-secondary2:
    image: mongo:latest
    container_name: mongoDB-Cont-secondary2
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    volumes:
      - mongodb_data_cont_secondary2:/data/db
      - ./mongodb-keyfile:/etc/mongodb-keyfile  # Bind mount the key file
    depends_on:
      - mongodb-Cont-primary  # Ensure primary node is up first
    command:
      - bash
      - -c
      - "ls /etc/mongodb-keyfile && mongod --auth --keyFile /etc/mongodb-keyfile --bind_ip_all --replSet rs0"

volumes:
  # Volume for Primary Node
  mongodb_data_cont:

  # Volumes for Secondary Nodes
  mongodb_data_cont_secondary1:
  mongodb_data_cont_secondary2:
```

3. Make sure the `mongodb-keyfile` is in the same directory as your Docker Compose file or specify the correct path to it.

4. After making these changes, run `docker-compose up` again to start your MongoDB replica set with authentication enabled and the key file specified.
