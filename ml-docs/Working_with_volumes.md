# Working with volumes

Other languages:

- English
- [français](Working_with_volumes_fr.md)

A volume provides storage which is not destroyed when a VM is terminated. On our clouds, volumes use [Ceph](https://en.wikipedia.org/wiki/Ceph_(software)) storage with either a 3-fold replication factor or [erasure codes](https://en.wikipedia.org/wiki/Erasure_code) to provide safety against hardware failure. On [Arbutus](Cloud_resources.md), the *Default* volume type uses erasure codes to provide data safety while reducing the extra storage costs of 3-fold replication while the *OS or Database* volume type still uses the 3-fold replication factor. More documentation about OpenStack volumes can be found [here](https://docs.openstack.org/cinder/latest/cli/cli-manage-volumes.html).

# Creating a volume

[![](/mediawiki/images/thumb/b/b3/Creating_a_volume_EN.png/300px-Creating_a_volume_EN.png)](FileCreating_a_volume_ENpng.md)

Create Volume dialog (Click for larger image)

To create a volume click on [![](/mediawiki/images/0/00/Create-Volume-Button.png)](FileCreate-Volume-Buttonpng.md) and fill in the following fields:

- *Volume Name*: `data`, for example
- *Description*: (optional)
- *Volume Source*: `No source, empty volume`
- *Type*: `No volume type`
- *Size (GiB)*: `40`, or some suitable size for your data or operating system
- *Availability Zone*: the only option is `nova`

Finally, click on the blue *Create Volume* button at the bottom.

# Mounting a volume on a VM

## Attaching a volume

[![](/mediawiki/images/thumb/e/eb/Manage_attachments_EN.png/400px-Manage_attachments_EN.png)](FileManage_attachments_ENpng.md)

Managing attachments command in the Actions menu (Click for larger image)

- **Attaching** is the process of associating a volume with a VM. This is analogous to inserting a USB key or plugging an external drive into your personal computer.
- You can attach a volume from the *Volumes* page in the dashboard.
- At the right-hand end of the line describing the volume is the *Actions* column; from the drop-down menu, select *Manage Attachments*.
- In the *Attach to Instance* drop-down menu, select a VM.
- Click on the blue *Attach Volume* button.

Attaching should complete in a few seconds. Then the volumes page will show the newly created volume attached to your selected VM on `/dev/vdb` or some similar location.

## Formatting a newly created volume

- **DO NOT FORMAT** if you are attaching an existing volume. Instead you can skip this step as the volume would have already been formatted if you had been previously using it to store data.
- **Formatting** erases all existing information on a volume and therefore should be done with care.
- Formatting is the process of preparing a volume to store directories and files.
- Before a newly created and attached volume can be used, it must be formatted.
- See instructions for doing this on a [Linux](Using_a_new_empty_volume_on_a_Linux_VM.md) or [Windows](Using_a_new_empty_volume_on_a_Windows_VM.md) VM.

## Mounting a volume

- **Mounting** is the process of mapping the volume's directory and file structure logically within the VM's directory and file structure.
- To mount the volume, use a command similar to `[name@server ~]$ sudo mount /dev/vdb1 /mnt` depending on the device name, disk layout, and the desired mount point in your filesystem.

This command makes the volume's directory and file structure available under the VM's /mnt directory. However, when the virtual machine reboots, the volume will need to be re-mounted using the same `mount` command.

It is possible to automatically mount volumes when a virtual machine boots. This requires editing the file named /etc/fstab to contain a new line with details about how the volume should be mounted.

To view mounting information, use the 'blkid' command  
`blkid`

Based on the UUID, add a line to /etc/fstab like this:

`/dev/disk/by-uuid/anananan-anan-anana-anan-ananananana /mnt auto defaults,nofail 0 3`

Where 'anananan-anan-anana-anan-ananananana' is substituted with UUID of the device you wish to auto-mount.

For more details about how to edit this file see this [Ubuntu community help page](https://help.ubuntu.com/community/Fstab).

# Booting from a volume

If you want to run a persistent machine, it is safest to boot from a volume. When you boot a VM from an image rather than a volume, the VM is stored on the local disk of the actual machine running the VM. If something goes wrong with that machine or its disk, the VM may be lost. Volume storage has redundancy, which protects the VM from hardware failure. Typically when booting from a volume VM flavors starting with the letter p are used (see [Virtual machine flavors](Virtual_machine_flavors.md)).

There are several ways to boot a VM from a volume. You can

- boot from an image, creating a new volume, or
- boot from a pre-existing volume, or
- boot from a volume snapshot, creating a new volume.

If you have not done this before, then the first one is your only option. The other two are only possible if you have already created a bootable volume or a volume snapshot.

If creating a volume as part of the process of launching the VM, select *Boot from image (creates a new volume)*, select the image to use, and the size of the volume. If this volume is something you would like to remain longer than the VM, ensure that the *Delete on Terminate* box is not checked. If you are unsure about this option, it is better to leave this box unchecked. You can manually delete the volume later.

# Creating an image from a volume

[![](/mediawiki/images/thumb/2/24/Upload_volume_from_image_EN.png/400px-Upload_volume_from_image_EN.png)](FileUpload_volume_from_image_ENpng.md)

Upload to Image form (Click for larger image)

Creating an image from a volume allows you to download the image. Do this if you want to save it as a backup, or to spin up a VM on a different cloud, e.g., with [VirtualBox](https://www.virtualbox.org/). If you want to copy a volume to a new volume within the same cloud see cloning a volume instead.

To create an image of a volume, it must first be detached from a VM. If it is a boot (root) volume, it can only be detached from a VM if the VM is terminated/deleted; however, make sure you have not checked *Delete Volume on Instance Delete* when creating the VM.

Large images (more than 10-20GB) may be very slow to create, upload, and otherwise manage. You may want to consider [separating data](Backing_up_your_VM.md#An_example_backup_strategy) if possible.

## Using the dashboard

1. Click on the *Volumes* left-hand menu.
2. Under the volume you wish to create an image of click on the drop-down *Actions* menu and select *Upload to Image*.
3. Choose a name for your new image.
4. Choose a disk format. QCOW2 is recommended for using within the OpenStack cloud as it is relatively compact compared to *Raw* and works well with OpenStack. If you wish to use the image with Virtualbox, the *vmdk* or *vdi* image formats might be better suited.
5. Finally, click on *Upload*.

## Using the command line client

The [command line client](OpenStack_Command_Line_Clients.md) can do this:

```
[name@server ~]$ openstack image create --disk-format <format> --volume <volume_name> <image_name>

```

where

- <format> is the disk format (two possible values are [qcow2](https://en.wikipedia.org/wiki/Qcow) and [vmdk](https://en.wikipedia.org/wiki/VMDK)),
- <volume\_name> can be found from the OpenStack dashboard by clicking on the volume name, and
- <image\_name> is a name you choose for the image.

You can then [download the image](Working_with_images.md#Downloading_an_Image).

# Cloning a volume

Cloning is the recommended method for copying volumes. While it is possible to make an image of an existing volume and use it to create a new volume, cloning is much faster and requires less movement of data behind the scenes. This method is handy if you have a persistent VM and you want to test out something before doing it on your production site. It is highly recommended to shut down your VM before creating a clone of the volume as the newly created volume may be left in an inconsistent state if there was writing to the source volume during the time the clone was created. To create a clone you must use the [command line client](OpenStack_Command_Line_Clients.md) with this command

```
[name@server ~]$ openstack volume create --source <source-volume-id> --size <size-of-new-volume> <name-of-new-volume>

```

# Detaching a volume

Before detaching a volume, it is important to make sure that the operating system and other programs running on your VM are not accessing files on this volume. If so, the detached volume can be left in a corrupted state or the programs could show unexpected behaviours. To avoid this, you can either shut down the VM before you detach the volume or [unmount the volume](Using_a_new_empty_volume_on_a_Linux_VM.md#Unmounting_a_volume_or_device).

To detach a volume, log in to the OpenStack dashboard (see the [list of links to our cloud systems](Cloud.md#Cloud_systems)) and select the project containing the volume you wish to detach. Selecting *Volumes -> Volumes* displays the project’s volumes. For each volume, the *Attached to* column indicates where the volume is attached.

- If attached to `/dev/vda`, it is a boot volume; you must delete the attached VM before the volume can be detached otherwise you will get the error message *Unable to detach volume*.

- With volumes attached to `/dev/vdb`, `/dev/vdc`, etc. you do not need to delete the VM it is attached to before proceeding. In the *Actions* column drop-down list, select *Manage Attachments*, click on the *Detach Volume* button and again on the next *Detach Volume* button to confirm.