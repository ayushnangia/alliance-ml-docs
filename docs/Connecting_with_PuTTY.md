# Connecting with PuTTY

Other languages:

- English
- [français](Connecting_with_PuTTY_fr.md)

[![](/mediawiki/images/thumb/d/d5/Putty_basic.png/400px-Putty_basic.png)](FilePutty_basicpng.md)

Enter hostname or IP address (Click for larger image)

[![](/mediawiki/images/thumb/7/7a/Putty_username.png/400px-Putty_username.png)](FilePutty_usernamepng.md)

Specify username to use when connecting; this is optional as one can type it when connecting (Click for larger image)

[![](/mediawiki/images/thumb/9/9f/Putty_X11_forwarding.png/400px-Putty_X11_forwarding.png)](FilePutty_X11_forwardingpng.md)

Enable X11 forwarding (Click for larger image)

[![](/mediawiki/images/thumb/a/a5/Putty_ssh_key.png/400px-Putty_ssh_key.png)](FilePutty_ssh_keypng.md)

Specifying an SSH key (Click for larger image)

Start up [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/) and enter the host name or IP address of the machine you wish to connect to. You may also save a collection of settings by entering a session name in the *Save Sessions* text box and clicking the *Save* button. You can set the username to use when logging into a particular host under the *Connection->Data* section in the *Auto-login username* text box to saving typing the username when connecting.

# X11 forwarding

If working with graphical-based programs, X11 forwarding should be enabled. To do this, go to *Connection->SSH->X11* and check the *Enable X11 forwarding* checkbox. To use X11 forwarding one must install an X window server such as [Xming](http://www.straightrunning.com/xmingnotes/) or, for the recent versions of Windows, [VcXsrv](https://sourceforge.net/projects/vcxsrv/). The X window server should be actually started prior to connecting with SSH. Test that X11 forwarding is working by opening a PuTTY session and running a simple GUI-based program, such as typing the command `xclock`. If you see a popup window with a clock, X11 forwarding should be working.

# Using a key pair

To set the private key putty uses when connecting to a machine go to Connection->SSH->Auth and clicking the *Browse* button to find the private key file to use. Putty uses files with a *.ppk* suffix, which are generated using PuTTYGen (see [Generating SSH keys in Windows](Generating_SSH_keys_in_Windows.md) for instructions on how to create such a key). In newer versions of Putty, you need to click the "+" sign next to *Auth* and then select *Credentials* to be able to browse for the *Private key file for authentication*. Note that the additional fields in that newer interface, i.e. *Certificate to use* and *Plugin to provide authentication response*, should be left blank.