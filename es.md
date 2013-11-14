				ELASTICSEARCH and MYSQL DATABASE INTEGRATION

Tested on Operating System: UBUNTU 13.10

NECESSARY DOWNLOADS AND INSTALLATIONS
=====================================
1. OpenJDK (Java Development Kit)
	$ sudo apt-get install openjdk-7-jdk
	
2. Curl
	$ sudo apt-get install curl
	
3. MySQL Database
	$ sudo apt-get install mysql-server
   (During the installation it will ask you to provide password (here 123456) for the database.)

4. MySQL JDBC (Java Database Connectivity) driver
	$ sudo apt-get install libmysql-java
   
   Setting up the user to use JDBC
	$ gedit .bashrc
   Append these two lines to /home/[user]/.bashrc file as it is
	CLASSPATH=$CLASSPATH:/usr/share/java/mysql.jar
	export CLASSPATH

   Also download the following file for now.
	http://cdn.mysql.com/Downloads/Connector-J/mysql-connector-java-5.1.27.zip
   We will unzip and use this download afterwards.
   
5. GIT
	$ sudo apt-get install git



ELASTICSEARCH INSTALLATION
==========================
1. Download the tar.gz file from the given link:
	https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.7.tar.gz
	
2. Extract the tar.gz file using 
	$ tar -zxvf Downloads/elasticsearch-0.90.7.tar.gz

	
STARTING AN ELASTICSEARCH INSTANCE
==================================
Before starting the node ,give a name to the instance and assign a cluster name (not necessarily) to the node 
rather than any arbitrary name assigned by Elasticsearch itself, follow the following steps:
1. Edit elasticsearch.yml file from the config folder
	$ gedit elasticsearch-0.90.7/config/elasticsearch.yml

2. Append the following lines to the file (This will also specify the path to store logs and data)

	cluster.name: Elasticsearch-Ubuntu
	node.name: "Node 1"
	path:
	logs: ./logs
	data: ./data

3. Close the file

Now we are ready to start the instance:
1. Provide the following command
	$ elasticsearch-0.90.7/bin/elasticsearch -f

2. Checkout for correct starting up of the node using following command in a new terminal
	$ curl -XGET http://localhost:9200/
   	
   You may see the output similar to following output if everything is fine:
	{
	  "ok" : true,
	  "status" : 200,
	  "name" : "Node 1",
	  "version" : {
		"number" : "0.90.7",
		"build_hash" : "36897d07dadcb70886db7f149e645ed3d44eb5f2",
		"build_timestamp" : "2013-11-13T12:06:54Z",
		"build_snapshot" : false,
		"lucene_version" : "4.5.1"
	  },
	  "tagline" : "You Know, for Search"
	}

	
KIBANA DOWNLOAD
===============
1. Download the tar.gz file from the given link:
	https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz
	
2. Extract the tar.gz file using 
	$ tar -zxvf Downloads/kibana-3.0.0milestone4.tar.gz

KIBANA SETUP
============
1. Open config.js from extracted folder, in an editor.
	$ gedit kibana-3.0.0milestone4/config.js

2. Set the elasticsearch parameter to the fully qualified hostname of your Elasticsearch server( http://localhost:9200 )
   21st line of the file should now look like:
   
	elasticsearch: "http://localhost:9200",

3. Enter a sample data to visualize a tweet:

	$ curl -XPUT 'http://localhost:9200/twitter/tweet/1' -d '{
		"user" : "kimchy",
		"post_date" : "2009-11-15T14:12:12",
		"message" : "trying out Elastic Search"
	}'	
4. You must see the following output
	{
		"ok" : true,
		"_index" : "twitter",
		"_type" : "tweet",
		"_id" : "1",
		"_version" : 1
	}	
	
5. Copy the contents of the extracted directory to the web-server or 
   Simply open index.html and start using KIBANA with "Sample Dashboard"

6. If Everything seems alright now it's time to delete the tweet document we created with following command

	$ curl -XDELETE 'localhost:9200/twitter'
	
   Output must be	
   
	{"ok":true,"acknowledged":true}

7. Kibana is installed correctly.	
	
ELASTICSEARCH PARAMEDIC SETUP
=============================
1. Clone the git file from the given link:
	$ git clone git://github.com/karmi/elasticsearch-paramedic.git

2. Open the index.html file in web browser
	$ firefox index.html

3. Now we will able to see the status of our cluster nodes and many other useful information.


SETTING UP MYSQL DATABASE
=========================
1. Add some tables to the database. I am using here "exampledb.sql" file to import sample biometric data.

	$ mysql -u root -p123456
	mysql> use exampledb;
	mysql> source <<path_to_exampledb.sql>>
	
2. 	We will choose "vendor" table for indexing it to Elasticsearch node.
	
	mysql> select * from vendor;
	+-----------+--------------+--------------------------+------------+-----------------+-----------------------------+
	| vendor_id | product_type | vendor_name              | product_id | product_name    | description                 |
	+-----------+--------------+--------------------------+------------+-----------------+-----------------------------+
	|        24 | sensor       | Cross Match Technologies |          1 | LSCAN Guardian  | 10 print fingerprint sensor |
	|        24 | sensor       | Cross Match Technologies |          2 | I Scan 2        | dual iris imager            |
	|        24 | Sensor       | Cross Match Technologies |          3 | TP-4101/Agile   | 10 print finger scanner     |
	|        24 | Sensor       | Cross Match Technologies |          4 | I Scan 3        | Iris imager                 |
	+-----------+--------------+--------------------------+------------+-----------------+-----------------------------+
	4 rows in set (0.00 sec)
   This is what you should see.

SETTING UP MYSQL-JDBC ELASTIC SEARCH RIVER 
==========================================

1. 







curl -XPUT 'localhost:9200/_river/my_jdbc_river/_meta' -d '{
    "type" : "jdbc",
    "jdbc" : {
    "versioning" : false,
    "autocommit" : true,
    "digesting" : true, 
        "driver" : "com.mysql.jdbc.Driver",
        "url" : "jdbc:mysql://localhost:3306/exampledb",
        "user" : "root",
        "password" : "123456",
        "sql" : "select vendor_id, product_type, vendor_name, product_id as _id, product_name, description from vendor",
    "strategy" : "simple",
    "poll" : "5s"
    },
    "index" : {
        "index" : "jdbc",
        "type" : "jdbc",
    "versioning" : false,
    "digesting" : true,
    "autocommit" : false, 
    "bulk_size" : 100,
    "max_bulk_requests" : 1000
    }
}'
