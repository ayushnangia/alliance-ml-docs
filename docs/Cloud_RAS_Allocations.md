# Cloud RAS Allocations

Other languages:

- English
- [français](Cloud_RAS_Allocations_fr.md)

*Parent page: [Cloud](Cloud.md)*

Any Digital Research Alliance of Canada user can access modest quantities of resources as soon as they have an Alliance account. The Rapid Access Service (**RAS**) allows users to experiment and to start working right away. Many research groups can meet their needs with the Rapid Access Service only. Users requiring larger resource quantities can apply to our annual [Resource Allocation Competition](RAC_application_guide.md) (**RAC**). Primary Investigators (PIs) with a current RAC allocation are also able to request resources via RAS.

Using cloud resources, researchers can create ***cloud instances*** (also known as *virtual machines* or *VMs*). There are two options available for cloud resources:

- **Compute instances**: These are instances that have a **limited life-time** (wall-time) and typically have **constant high CPU** requirements. They are sometimes referred to as *batch* instances. Users may need a large number of compute instances for production activities. Maximum wall-time for compute instances is **one month**. Upon reaching their life-time limit these instances will be scheduled for deactivation and their owners will be notified in order to ensure they clean up their instances and download any required data. Any grace period is subject to resources availability at that time.
- **Persistent instances**: These are instances that are meant to run **indefinitely** and would include **Web servers**, **database servers**, etc. In general, these instances provide a persistent service and use **less CPU** power than compute instances.
- **vGPU**: Arbutus currently offers H100 GPUs in a single flavor for RAS use (**g1-12vgb-c3-35gb-125**). This flavor has 12GB GPU memory, 3 vCPUs, 35GB of memory, and 125GB of ephemeral storage. Alternative GPU flavors are available for RAC recipients; researcher feedback on useful resource combinations for those new flavors is welcomed. For more information on setting up your VM to use vGPUs, see [Using cloud vGPUs](Using_cloud_GPUs.md).

## Cloud RAS resources limits

| Attributes | Compute instances [ 1 ] | Persistent instances [ 1 ] |
| --- | --- | --- |
| May be requested by | PIs only | PIs only |
| vCPUs (see VM flavours ) | 80 | 25 |
| vGPUs [ 2 ] | 1 |
| Instances [ 3 ] | 20 | 10 |
| Volumes [ 3 ] | 2 | 10 |
| Volume snapshots [ 3 ] | 2 | 10 |
| RAM (GB) | 300 | 50 |
| Floating IP | 2 | 2 |
| Persistent storage (TB) | 10 |
| Object storage (TB) [ 2 ] | 10 |
| Shared filesystem storage (TB) [ 2 ] | 10 |
| Default duration | 1  year [ 4 ] , with 1 month wall-time | 1 year (renewable) [ 4 ] |
| Default renewal | April [ 4 ] | April [ 4 ] |

## Requesting RAS

To request RAS, please [fill out this form](https://docs.google.com/forms/d/e/1FAIpQLSeU_BoRk5cEz3AvVLf3e9yZJq-OvcFCQ-mg7p4AWXmUkd5rTw/viewform).

## Notes

1. ↑ 1.0 1.1 Users may request both a compute and persistent allocation to share a single project. Storage is shared between the two allocations and is limited to 10TB/PI per storage type. PIs may request a 1-year renewal of their cloud RAS allocations an unlimited number of times; however, allocations will be given based on available resources and are not guaranteed. Requests made after January 1 will expire March of the following year and therefore may be longer than 1 year. Allocation requests made between May-December will be less than 1 year. Renewals will take effect in April.
2. ↑ 2.0 2.1 2.2 Currently only available at Arbutus.
3. ↑ 3.0 3.1 3.2 This is a metadata quota and not a hard limit, users can request an increase beyond these values without a RAC request.
4. ↑ 4.0 4.1 4.2 4.3 This is to align with the RAC allocation period of April-March.