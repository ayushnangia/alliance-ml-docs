# Using a new empty volume on a Windows VM

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

This page describes the steps to partition and format a volume attached to a Windows VM

1. If a new volume is not already attached, create and attach a new empty volume to a Windows VM as described in [working with volumes](Working_with_volumes.md).
2. Connect to the Windows VM using a [Remote desktop connection](Cloud_Quick_Start.md#Remote_desktop_connection)
3. Open up "Computer Management" on the Windows VM.
4. Go to "Storage"->"Disk Management" and then right click on the new disk label probably "Disk 1" and select "online" to bring the disk online.
5. Initialize the disk by right clicking again on the disk label and selecting "Initialize Disk".
6. Right click on the "unallocated" disk pane and select create new simple volume.