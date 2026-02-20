# Using swift

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

## Object Storage in Arbutus cloud

The OpenStack Object Store project, known as Swift, offers cloud storage software so that you can store and retrieve lots of data with a simple API.

If you require s3 access to it, please contact our [Technical support](Technical_Support.md).

## Using the Object Storage via Browser

Swift can be accessed via the openstack cli and/or via the [Cloud webinterface](https://arbutus.cloud.computecanada.ca).

| Dashboard Menu | The object storage can be accessed via the menu on the left side. |
| --- | --- |
| Publicly accessible container | To store data a storage container needs to be created, which can hold the data. Multiple containers can be created if required, by clicking on Public Access , the container becomes public and will be accessible by anyone. If the container has no public access, it can only be used within the projects VMs. |
| File upload via browser | To upload files via browser into the container, click on the upload button. |

## Using the Object Storage via OSA cli