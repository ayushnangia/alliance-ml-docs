# Accessing object storage with WinSCP

Other languages:

- English
- [français](Accessing_object_storage_with_WinSCP_fr.md)

This page contains instructions on how to set up and access [Arbutus object storage](Arbutus_Object_Storage.md) with WinSCP, one of the [object storage clients](Arbutus_object_storage_clients.md) available for this storage type.

## Installing WinSCP

WinSCP can be installed from [https://winscp.net/](https://winscp.net/).

## Configuring WinSCP

Under "New Session", make the following configurations:

- File protocol: Amazon S3
- Host name: object-arbutus.cloud.computecanada.ca
- Port number: 443
- Access key ID: 20\_DIGIT\_ACCESS\_KEY

and "Save" these settings as shown below

[![](/mediawiki/images/thumb/9/97/WinSCP_Configuration.png/600px-WinSCP_Configuration.png)](FileWinSCP_Configurationpng.md)

WinSCP configuration screen

Next, click on the "Edit" button and then click on "Advanced..." and navigate to "Environment" to "S3" to "Protocol options" to "URL style:" which **must** changed from "Virtual Host" to "Path" as shown below:

[![](/mediawiki/images/thumb/1/1b/WinSCP_Path_Configuration.png/600px-WinSCP_Path_Configuration.png)](FileWinSCP_Path_Configurationpng.md)

WinSCP Path Configuration

This "Path" setting is important, otherwise WinSCP will not work and you will see hostname resolution errors, like this:

[![](/mediawiki/images/thumb/b/bc/WinSCP_resolve_error.png/400px-WinSCP_resolve_error.png)](FileWinSCP_resolve_errorpng.md)

WinSCP resolve error

## Using WinSCP

Click on the "Login" button and use the WinSCP GUI to create buckets and to transfer files:

[![](/mediawiki/images/thumb/2/2b/WinSCP_transfers.png/800px-WinSCP_transfers.png)](FileWinSCP_transferspng.md)

WinSCP file transfer screen

## Access Control Lists (ACLs) and Policies

Right-clicking on a file will allow you to set a file's ACL, like this:

[![](/mediawiki/images/thumb/d/d7/WinSCP_ACL.png/400px-WinSCP_ACL.png)](FileWinSCP_ACLpng.md)

WinSCP ACL screen