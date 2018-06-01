# Cristata - sql
This is the data model for time series data management and the associated mechanism for deployment. The data model itself is located in the `src/main/resources/db/migration` directory. This contains the required DB2 tables and procedures for Cristata data management.

For deployment, a lightweight, Java based SQL data model deployment component built around the [Flyway](https://flywaydb.org/) library is provided. It provides a simple method to deploy data models represented as one or more plain `.sql` files.

### Flyway Concepts

Flyway is built around the concept of versioned SQL migrations, and their ordered application to a database. 

Migrations are represented as ordinary SQL files that contain DDL commands such as `CREATE`, `ALTER`, or `DROP`, as well as DML commands to `INSERT` 
or `DELETE` to prepopulate a DB with initial data.

Migration files have a well defined naming format:

`V*__Description_Of_Migration.sql` where * represents the data model version - note the double underscore after the version
number.

Flyway locates migrations by scanning the Java classpath for a `db/migration` directory and loads all `.sql` files in that directory conforming to the naming convention above.

It also has bundled with it a small number of JDBC drivers, but it does not include a driver for DB2. To use a DB2 JDBC endpoint, 
ensure a compatible driver JAR exists in the local Maven repository.


### Project Dependencies

The project has the following first-order dependencies defined in `pom.xml`:

- `flyway-core`, is an Apache v2 licensed open-source library that makes database migrations easy.
- `db2jcc4`, is the DB2 Java client library. **NB**: The DB2 driver JAR is not available from Maven Central - it needs to be 
downloaded and [manually installed in your local Maven repository](https://maven.apache.org/guides/mini/guide-3rd-party-jars-local.html) 
prior to a build.
This can be downloaded from the IBM website -> http://www-01.ibm.com/support/docview.wss?uid=swg21363866 , IBM Data Server Driver for JDBC and SQLJ (JCC Driver). Most recent verified version is 11.1.

Upon download of the jar file, the following command installs it in the local Maven repository:

`mvn install:install-file -Dfile=db2jcc4.jar -DgroupId=com.ibm.db2.jcc -DartifactId=db2jcc4 -Dversion=11.1 -Dpackaging=jar`


### Build, Package, and Run

The project is Maven based - to build and package the project: 

`mvn clean package`

which will generate an executable uber-JAR.
