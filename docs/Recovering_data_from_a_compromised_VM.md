# Recovering data from a compromised VM

Other languages:

- English
- [français](Recovering_data_from_a_compromised_VM_fr.md)

*Parent page: [Cloud](Cloud.md)*

You are responsible for recovering data out of a VM that has been compromised.

The information in this page is not complete, but sets out what you need to do in this situation.

## What happens when we detect a compromised VM?

1. Our support team confirms this by investigating network traffic logs and other sources.
2. The VM is shut down and locked at the sysadmin level.
3. You are notified by email.

## Why do you need to rebuild?

- You cannot start an administratively locked VM.
- The contents of the VM are no longer trustworthy, but it is relatively safe to extract the data.
- You have to build a new VM.

## What steps should you take?

1. Send an email to cloud@tech.alliancecan.ca outlining your recovery plan; if access to the filesystem is required, the cloud support team will unlock the volume.
2. Log in to the OpenStack admin console.
3. Launch a new instance that will be used for data rescue operations.
4. Under *Volumes*, select *Manage Attachments* from the dropdown list at the far right for the volume that was compromised and click on the *Detach Volume* button.
5. Under *Volumes*, select *Manage Attachments* for the volume that was compromised and select *Attach To Instance* (select the recovery instance you just launched).
6. ssh in to your recovery instance: you will now see your old, compromised volume available as the “vdb” disk.
7. Mounting the appropriate filesystem out of a partition or an LVM logical volume depends on how the base OS image was created. Because instructions vary greatly, contact someone with experience to continue.