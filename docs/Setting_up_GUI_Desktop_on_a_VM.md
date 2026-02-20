# Setting up GUI Desktop on a VM

Other languages:

- English
- [français](Setting_up_GUI_Desktop_on_a_VM_fr.md)

Some software that you can install on your virtual machine (VM, or instance) are only, or best accessed, through their graphical user interface (GUI). It is possible to use a GUI through SSH + X11 forwarding. However, you may observe better performance when using VNC to connect to a remote desktop running on your VM.

Below, we outline steps for setting a remote desktop with VNC. Please note that these instructions are for a VM running a Ubuntu operating system.

1. Install a GUI Desktop on your VM.  
   There are lots of different Desktop packages available. For example some common Desktop packages available for the Ubuntu operating system are:
   - [ubuntu-unity-desktop](https://ubuntuunity.org/%7C)
   - [ubuntu-mate-desktop](https://ubuntu-mate.org/%7C)
   - [lubuntu-desktop](https://lubuntu.net/%7C)
   - [xubuntu-desktop](https://xubuntu.org/screenshots/%7C)
   - [xfce4](https://www.xfce.org/%7C)
   - ubuntu-desktop
   - [kde-plasma-desktop](https://kde.org/plasma-desktop/%7C)
   - ubuntu-desktop-minimal
   - [cinnamon](https://en.wikipedia.org/wiki/Cinnamon_(desktop_environment)%7C)
   - [icewm](https://ice-wm.org/%7C)[This article](https://cloudinfrastructureservices.co.uk/best-ubuntu-desktop-environments) shows a few of these different desktops. Below are the commands to install the MATE desktop.

   ```
   [name@server ~]$ sudo apt update
   [name@server ~]$ sudo apt upgrade -y
   [name@server ~]$ sudo apt install ubuntu-mate-desktop

   ```

   During the installation of the `ubuntu-mate-desktop` package it will ask you to choose the default display manager, a good option is [`lightdm`](https://en.wikipedia.org/wiki/LightDM%7C). Installing the `ubuntu-mate-desktop` package can take a fair amount of time (something like 15-30 mins).
2. Install TigerVNC server.  
   This software runs on your VM and allows you to use the GUI desktop you installed in step 1. remotely using a client software.

   ```
   [name@server ~]$ sudo apt install -y tigervnc-common tigervnc-standalone-server

   ```

   This command will install the TigerVNC server and some supporting software. For details about using VNC servers and clients see our docs on [VNC](VNC.md).
3. Start the vnc server

   ```
   [name@server ~]$ vncserver
   -> enter a password
   -> enter "n" for view-only password

   ```

   The first time you start a vnc server it will ask you to set a password. This password is used later when connecting to the vnc desktop. You don't need a view-only password. The `vncpasswd` command can later be used to change your password.
4. Test your connection by opening port `5901` (see [security groups](OpenStack.md#Security_Groups) for more information about opening ports to your VMs with OpenStack) and connecting using a VNC viewer, for example [TigerVNC](https://tigervnc.org/). However, this is not a secure connection; data sent to and from your VM will not be encrypted. This is only meant to test your server-client connection before connecting securely with an SSH tunnel (the next step). If you are confident in your ability to setup an SSH tunnel, you may skip this step.
5. Connect using an SSH tunnel (see [SSH\_tunnelling](SSH_tunnelling.md)). There is [an example of creating an SSH tunnel to a VNC server running on a compute node of one of our clusters](VNC.md#Compute_Nodes).
   Below are instructions for connecting using an SSH tunnel for linux or mac:
   - Open your terminal
   - Type the following in your local terminal: `SSH -i filepathtoyoursshkey/sshprivatekeyfile.key -L5901:localhost:5901 ubuntu@ipaddressofyourVM`
   - Start your VNC viewer.
   - In the VNC server field enter: `localhost:5901`.
   - Your GUI desktop for your remote session should now open
6. Close port `5901`. Once you are connected to your VNC server using an SSH tunnel, you no longer require port 5901 open so it is recommended that you remove this rule from your security groups. (see [security groups](OpenStack.md#Security_Groups) for more information).
7. Once you are finished using the remote desktop you may stop the vncserver with:

   ```
   [name@server ~]$ vncserver -kill :1

   ```