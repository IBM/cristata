/*
* Author: markpurcell@ie.ibm.com
* Using Flyway to delete/add db schema
*/

package ibm.drl.sqldeploy;

import org.flywaydb.core.Flyway;


public class Execute {
    public static void main(String[] args) {
        if (args.length != 4) {
		System.err.println("Usage: DB_JDBC_URL DB_Username DB_Passsword DB_Schema");
		return;
        }

    	Flyway flyway = new Flyway();
        flyway.setDataSource(args[0], args[1], args[2]);
        flyway.setSchemas(args[3]);

        //Delete everything first
	flyway.clean();
	//Now apply the sql commands
        flyway.migrate();
    }
}
