# Arbutus object storage clients

Other languages:

- English
- [français](Arbutus_object_storage_clients_fr.md)

For information on obtaining Arbutus Object Storage, please see [this page](Arbutus_Object_Storage.md). For information on how to use an object storage client to manage your Arbutus object store, choose a client and follow instructions from these pages:

- [Accessing object storage with s3cmd](Accessing_object_storage_with_s3cmd.md)
- [Accessing object storage with WinSCP](Accessing_object_storage_with_WinSCP.md)
- [Accessing the Arbutus object storage with AWS CLI](Accessing_object_storage_with_AWS_CLI.md)
- [Accessing the Arbutus object storage with Globus](Globus.md#Object_storage_on_Arbutus)

It is important to note that Arbutus' Object Storage solution does not use Amazon's [S3 Virtual Hosting](https://documentation.help/s3-dg-20060301/VirtualHosting.html) (i.e. DNS-based bucket) approach which these clients assume by default. They need to be configured not to use that approach, as described in the pages linked above.