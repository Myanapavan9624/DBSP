<h1 align="center">SQL Query Optimizer</h1>

An SQL query optimizer that executes an SQL query plan and visualizes its performance, made for a project for NTU's CZ4031 (Database System Principles) course.

![Tables present in the database](https://i.imgur.com/MrvHfD9.png)

Queries are tested against [TPC-H](http://www.tpc.org/tpch/), a benchmark for generating dummy data in a database that attempts to mimic real world operations. The tables present in the database are shown in the image above.

## Installation and setup

First, clone this repository to a local folder on your computer. This repository contains two main folders - the `/api` backend (server), and the `/frontend` (client). To ensure that this project runs correctly, we need to set up both the frontend and the backend, then run them concurrently.

1. **Ensure that you have [Yarn](https://yarnpkg.com/getting-started) (A package manager for javascript) and [NodeJS](https://nodejs.org/en/) installed.**
2. Run `yarn install` in this root folder.

### Setting up the frontend

We are using [React](https://reactjs.org/) as well as a few other dependencies for the frontend.

1. Ensure that you have [Yarn](https://yarnpkg.com/getting-started) (A package manager for javascript) installed.
2. `cd` into `/frontend` and run `yarn install` to install the dependencies needed for the client.

### Setting up the backend

We are using [Flask](https://palletsprojects.com/p/flask/) to run the web server.

1. Ensure that you have [Poetry](https://python-poetry.org/docs/) (A package manager for Python) and at minimum [Python 3.8](https://www.python.org/downloads/) installed. You can run `pip install poetry` in your environment to install Poetry.
2. `cd` into `/api` and run `poetry install` to install the Python package dependencies for this backend. We are using Flask as a web server.
3. By default, the API server starts in production mode. To run in development mode and enable hot reloading, create an `.env` file in this folder and add the following environment variables:

```
FLASK_APP=app.py
FLASK_ENV=development
```

4. You will have to connect to a Postgresql database to run the query. This database should be populated with dummy data generated by [TPC-H](http://www.tpc.org/tpch/). Continue reading the installation instructions below if you have not generated the TPC-H dataset.
5. There are two ways to connect to the database. The first way is to input your database details directly in the frontend client itself, but the state will only persist until the page is refreshed. If you do not want to type in your details every time, fill up the `.env` file with the connection details of your PostgreSQL database. You `api/.env` file should look something like this now

```bash
FLASK_APP=app.py
FLASK_ENV=development
DB_HOST=localhost     (The IP your database is hosted on)
DB_NAME=TPC-H         (The name of your database)
DB_USER=postgres      (The username of the user that owns the database)
DB_PASSWORD=postgres  (Password for your user)
DB_PORT=5432          (Port that your database runs on)
```

We recommend that you use this exact configuration for the PostgreSQL database (aka with a database named "TPC-H").

## Running the application

- To run both the api server and the frontend client concurrently, `cd` to the root folder and run `yarn start`. This is the option that you should go with most of the time for the application to work correctly.
- To run only the api server, `cd` to `/api` and run `poetry run flask run`.
- To run only the frontend client, `cd` to `/frontend` and run `yarn start`.

## Other installation instructions

Other than the above instructions, the following setup instructions below are required if you:

- Have not installed PostgreSQL on your computer.
- Have not generated a set of [TPC-H](http://www.tpc.org/tpch/) dummy data and populated a PostgreSQL database with it.

If you've already completed these two steps, feel free to ignore the setup instructions below and simply run `yarn start` from the root folder in order to start both the frontend and the API server concurrently. Otherwise, do set up the following to ensure that the project runs correctly.

### Setting up PostgreSQL and the TPC-H dataset

1. Ensure that you have [PostgreSQL](https://www.PostgreSQL.org/download/) installed. This project may work on other database management systems, but has only been tested on PostgreSQL.
2. Run [pgAdmin](https://www.pgadmin.org/), which should come bundled in the PostgreSQL installation. If it's your first time accessing it, it will prompt you to create a root user and password - name this user `postgres` and set the password as `postgres`. Alternatively, supply your own password, but you will have to change the password in the environment variable of the main application if you do. Create a new database named "TPC-H".
3. Clone this repository into a new folder.
4. Open your terminal and run `psql -U postgres -f dss.ddl TPC-H` from the cloned repository's folder. This command connects you to PostgreSQL as the default user `postgres`, and runs the SQL commands found in dss.ddl on the database `TPC-H`. The commands will initialize empty tables in the database similar to the ones shown in the image at the top.
5. You may generate your own dummy data using [TPC-H](http://www.tpc.org/tpch/), or use our pre-generated data, found in this [Google drive](https://drive.google.com/drive/folders/1i7FYWI1ePuFFZpMdRO7gwVD2lLw_j03B?usp=sharing). Download `data.zip` and extract it. Each csv file corresponds and contains data of a table in the database.
6. Navigate back to the pgAdmin interface. Right click each table and click on `Import/Export`. Import the corresponding csv file into each table, with the format set to `csv` and encoding set to `UTF-8`. Set the delimeter to `|` and click OK to import the data.
7. Once all data has been imported, right click each table and verify that the data has been correctly imported by clicking `View/Edit Data` > `First 100 Rows`.
8. If all the data seems correct, run `psql -U postgres -f dss.ri TPC-H` in your terminal. This command will create the constraints on the tables, including initializing the primary keys and foreign keys on the various tables.
9. Next, right click each table within pgAdmin and click on `Maintenance`. Tick `Vaccuum`, and turn `Analyze` and `Verbose Messages` on. Run this for each table.

## Optional installations

Additionally, if you wish to use [Picasso](https://dsl.cds.iisc.ac.in/projects/PICASSO/picasso_download/license.htm), a DBMS query optimization visualizer, you may follow the setup instructions below as well. This is <b>optional</b> and not required for this project to function correctly.

### Setting up Picasso (DBMS query optimization visualizer)

1. Download [Picasso](https://dsl.cds.iisc.ac.in/projects/PICASSO/picasso_download/license.htm). Make sure to select the full library (we recommend getting the zip file). Extract it.
2. Ensure you have at least JDK 6.0 installed. We suggest the latest version of [AdoptOpenJDK](https://adoptopenjdk.net/releases.html). If you have your Java environment set up, navigate to `./PicassoRun/Windows/` and run `activatedb.bat`, `compileServer.bat` and `compileClient.bat` in this order to compile the Java files.
3. To connect to the PostgreSQL database, we will need to update our JDBC driver to the latest version. The JDBC driver serves to connect the Java application to our PostgreSQL database. Download it [here](https://jdbc.PostgreSQL.org/download.html#current).
4. Navigate to `./Libraries/` and find the jar file for the old JDBC driver for PostgreSQL. It should be named something like `PostgreSQL-8.0-311.jdbc3`. Replace this file with the latest version that you just downloaded. Rename it so it matches the old name (e.g. `PostgreSQL-8.0-311.jdbc3`) exactly, so that Picasso can detect it. Alternatively, you can let Picasso detect the name of the new file by modifying the `runServer.bat` script to include the new jdbc driver in `./PicassoRun/Windows/`.
5. Navigate back to `./PicassoRun/Windows/`. We can now start the program. Run `runServer.bat` to start the Picasso server, then run `runClient.bat` to run the Picasso client. A GUI should pop up. Click on `Enter`, and enter the connection details (`localhost` and port `4444` by default).
6. The Picasso client GUI should appear. We need to create a new connection to our TPC-H database. In the top menu, click on `DBConnection`, then click `New`. The DB Connection Settings window should pop up.
7. Fill in the following details:

- Connection details: TPC-H (Arbitrary name to save this connection for use next time)
- Machine: localhost (Where your database is running on)
- Engine: POSTGRES (Which JDBC engine to use to connect to your database)
- Port: 5432 (Default port to connect to the database)
- Database: TPC-H (Name of your database)
- Schema: public (Default schema for the database)
- User: postgres (Your user that owns the database, default root user is postgres)
- Password: \*\*\*\*\*\*\* (Your login password for user postgres)

  Click on `Save`.

8. Now that we've created our connection profile, go to the orange `Settings` pane. Choose your new connection under `DBConnection Descriptor:`. For example, if you've named the connection you just created TPC-H, select that. Picasso then attempts to connect to the database, and prints `STATUS: DONE` at the bottom if it suceeds. If the server terminal window outputs errors about 'Authentication type 10 not supported', go back to step 12 to update your JDBC driver.
9. We also have to update our Java3D driver in order for Picasso to be able to show graphs on a 64-bit architecture (it's legacy software). Download the latest Java3D executable from [this link](https://www.oracle.com/java/technologies/java-archive-downloads-java-client-downloads.html#java3d-1.5.1-oth-JPR). We recommend the `java3d-1_5_1-windows-amd64.exe` for 64-bit Windows.
10. Run the executable and install it. Go to the install location (default `C:/Program Files/Java/Java3D/1.5.1/`) and go to `./lib/ext/`. Copy all the jar files there, and paste it into your libraries folder of Piccasso at `picasso/Libraries/`. Replace any existing files.
11. Next, go back to the install location of Java3D and go to `./bin/`. Copy the `j3dcore-ogl.dll` file, and paste it in `C:/Windows/`, replacing any file there. This basically updates your Java3D runtime to 64-bit architecture.
12. Finally, we can go back to Picasso and load in some query plans in the form of SQL queries to analyze. Ensure that you are connected to your database in the Settings tab (DBConnection Descriptor -> TPC-H).
13. Click on the `QueryTemplate` tab just below the Settings section, and click the `Load QueryTemplate` button on the right. It brings up a default folder. Navigate to the `postgres` folder, and select any query to start.
14. As Picasso loads the query in, you will see the SQL query displayed in the textbox. You can name this query for later retrieval by giving it a name in the `QueryTemplate Descriptor` field.
15. With your SQL query loaded, click on the `Plan Diag` tab to generate a diagram enumerating all the optimized plans. If a prompt appears, click on `Generate Exact Diagram`. Click OK. You should see a colorful 2D square, which is the plan diagram - a collection of the optimal plans generated by the DBMS as the selectivity of your chosen predicates vary.
16. Read the [Picasso documentation](https://dsl.cds.iisc.ac.in/projects/PICASSO/picasso_download/doc/Picasso2Doc.pdf) for more information on how to use Picasso.
