# Managing your Linux VM

Other languages:

- English
- [français](Managing_your_Linux_VM_fr.md)

The majority of researchers use the Linux Operating System on their VMs. Common Linux distributions used are AlmaLunix, CentOS, Debian, Fedora, and Ubuntu. This page will help you with some common tasks to manage your Linux VM. VMs can also run the Microsoft Windows operating system. Some Windows management tasks are described [here](Cloud_Quick_Start.md#Windows).

# Linux VM user management

There are a number of ways to allow more than one person to log into a VM. We recommend creating new user accounts and adding public [SSH Keys](SSH_Keys.md) to these accounts.

## Creating a user account and keys

A new user account can be created on Ubuntu with the command

```
[name@server ~]$ sudo adduser --disabled-password USERNAME

```

To be able to connect, the new user will need to have a key pair, see [generating SSH keys in Windows](Generating_SSH_keys_in_Windows.md) or [creating a key pair in Linux or Mac](Using_SSH_keys_in_Linux.md#Creating_a_Key_Pair) depending on the operating system they will be connecting from. Then, their public key must be added to `/home/USERNAME/.ssh/authorized_keys` on the VM, ensuring permissions and ownership are correct as described in steps 2 and 3 of [Connecting using a key pair](Using_SSH_keys_in_Linux.md#Connecting_using_a_key_pair).

## Granting admin privileges

In Ubuntu, administrative or root user privileges can be given to a new user with the command

```
[name@server ~]$ sudo visudo -f /etc/sudoers.d/90-cloud-init-users

```

which opens an editor where a line like

```
USERNAME ALL=(ALL) NOPASSWD:ALL

```

can be added. For more detailed information about the `visudo` command and how to edit this file see this [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file-on-ubuntu-and-centos#what-is-visudo) tutorial.

## Dealing with system and security issues

See our guides for how to

- [recover data from a compromised VM](Recovering_data_from_a_compromised_VM.md)
- [recover your VM from the dashboard](VM_recovery_via_cloud_console.md)