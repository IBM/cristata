# Cristata
With the ever increasing proliferation of IoT devices, and the resulting frequency of data emanating from many devices, the acquisition and management of this data is proving to be a challenge.

In dealing with this challenge, cloud-based sytems that provide service elasticity are helpful in handling the potentially intermittent bursts of high volume data from these devices.

Cristata is a system, targeted at the developer community, to support general IoT data ingestion. It utilises several existing IBM Cloud services and details how these services are wired together. Serverless computing is employed to provide service elasticity and reduce the infrastructure management burden. Sample code includes SQL code for data storage (schema), Openwhisk actions (Cloud Functions) for interfacing with this schema and IoT data submission code.


![Cristata Architecture](/images/Cristata-Architecture.gif)


## Assumptions
- An IBM Cloud account is already created (https://console.bluemix.net/)
- With an organisation and space created
- IBM Cloud (Bluemix) CLI (command line interface) is installed (see Vagrantfile for details)
- IBM Cloud (Bluemix) Functions CLI (command line interface) is installed (see Vagrantfile for details)


## IBM Cloud Login

Login, and set organisation and space, using a combination of the commands below:
```
bx login -a https://api.ng.bluemix.net
bx iam orgs  # Outputs available organisations
bx iam spaces # Outputs available spaces
bx target --cf # Interactively select organisation/space
bx target -o <ORG> # Manually select organisation
bx target -s <SPACE> # Manually select space
```


## Bulding Helper Components

Cristata is backed by a DB2 schema, which must be deployed. A helper component is built for this purpose using Maven. First, fetch the `IBM Data Server Driver for JDBC and SQLJ (JCC Driver) version 11.1` from here http://www-01.ibm.com/support/docview.wss?uid=swg21363866. This driver (db2jcc4.jar) must be installed in the local Maven repository before building the helper component.

```
cp /path/to/db2jcc4.jar ./sql
cd sql
mvn install:install-file -Dfile=db2jcc4.jar -DgroupId=com.ibm.db2.jcc -DartifactId=db2jcc4 -Dversion=11.1 -Dpackaging=jar
mvn clean package
cd -
```

Futher details about this component can be found [here](sql/README.md).


## Provision IBM Cloud Components

Cristata's data persistence layer requires an internet-facing DB2 instance as well as *Watson IoT* and *Message Hub*. A script to automatically provision and configure these instances is provided. Note: if not bringing up a virtual machine using the Vagrantfile, please check for required packages (openjdk-8-jdk, maven, python3.6, python3-pip, jq etc).

Run script:
```
./provision.sh
```

As part of this provisioning process:
1. DB2 tables and stored procedures will be created.
2. Watson IoT device types and devices will be created.
3. Device publish credentials will be created.
4. A Message Hub topic will be created.

Note: some of these IBM Cloud components are **not free**.


## Connect Watson IoT to MessageHub
Now, a manual step is required unfortunately, to connect Watson IoT and Message Hub. This is achieved in the Watson IoT dashboard [See here for details](wiotToMhub.md).


## Set up IBM Cloud Functions

1. Change into the `openwhisk` directory, which now contains `my_setup.sh`. This was generated automatically by the provisioning process.
2. Invoke the makefile to build the actions for IBM Cloud Functions.
3. Deploy the actions by invoking the install script.

The commands are:
```
cd openwhisk
make all
./install.sh <BLUEMIX SPACE>
cd -
```

Note: It may take a few moments for the installed IBM Cloud Functions triggers and actions to become ready for use.


## Test pipeline by sending a message to Watson IoT

At this point, all components are provisioned and configured. During the provisioning process, credentials for new devices were created (mqtt-config1/2.json). These credentials can now be used to send data to the platform.

```
cd iot
pip3 install ibmiotf

python3 publish.py mqtt-config1.json
cd -

```

To subsequently view all devices added to the Cristata database run:
```
cd openwhisk
bx wsk action invoke Cristata-DeviceListing --result
```

And to view measurements for a given device (as specified in `request.json`) run:
```
bx wsk action invoke Cristata-TimeSeriesRetrieve -P request.json --result
```


Cristata is a sub-component of the GOFLEX H2020 project.

The project Generalized Operational FLEXibility for Integrating Renewables in the Distribution Grid (GOFLEX) has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 731232.

![Horizon H2020](/images/EU.png)
