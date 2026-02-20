# Mounting /project space on a VM in the cloud

Other languages:

- English
- [français](Mounting__project_space_on_a_VM_in_the_cloud_fr.md)

### Introduction

This document describes how to let a virtual machine (VM) access [/project](Project_Layout.md) filesystems on the national systems. VMs hosted on our [Cloud](Cloud.md) do not have direct access to the filesystems on the national HPC clusters. In order to access files stored on /project from a VM, please use SSHFS and observe the requirements mentioned below.

### SSHFS

SSHFS enables mounting your /project folder inside your VM.
SSHFS mounts appear like regular folders in your VM and can be accessed via regular Linux commands.

A reference can be found at [https://wiki.archlinux.org/index.php/SSHFS](https://wiki.archlinux.org/index.php/SSHFS)

### Requirements

In order to avoid security issues, the following requirements are needed if you choose to mount /project inside your VM:

- Do *not* store your password in plain text on the VM.
- Create an SSH key specifically for use with SSHFS, and *only* use it for that. Do *not* use the same SSH key that you use for logging in.
- Keep your VM up to date and only open ports that are required and secured.