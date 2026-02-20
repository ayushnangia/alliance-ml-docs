# SSH configuration file

Other languages:

- English
- [français](SSH_configuration_file_fr.md)

*Parent page: [SSH](SSH.md)*

On Linux and macOS, you can modify your local SSH configuration file to change the default behaviour of `ssh` and simplify the login procedure. For example, if you want to log into `narval.alliancecan.ca` as `username` using an [SSH key](Using_SSH_keys_in_Linux.md), you may need to use the following command:

```
[name@yourLaptop ~] ssh -i ~/.ssh/your_private_key username@narval.alliancecan.ca

```

To avoid having to type this command each time you want to connect to Narval, add the following to `~/.ssh/config` on your local machine:

```
 Host narval
   User username
   HostName narval.alliancecan.ca
   IdentityFile ~/.ssh/your_private_key

```

You can now log into Narval by typing

```
[name@yourLaptop ~] ssh narval

```

This also changes the behaviour of `sftp`, `scp`, and `rsync` and you can now [transfer files](Data_transfer.md) by typing for example

```
[name@yourLaptop ~] scp local_file narval:work/

```

If you frequently log into different clusters, modify the above `Host` block as follows instead of adding individual entries for each cluster separately:

```
 Host narval beluga graham cedar
   [...]
   HostName %h.alliancecan.ca
   [...]

```

Note that you need to install your public [SSH key](SSH_Keys.md) on each cluster separately or use [CCDB](SSH_Keys.md#Using_CCDB).

Note that other options of the `ssh` commands have corresponding parameters that you can put in your `~/.ssh/config` file on your machine. In particular, the command line options

- `-X` (X11 forwarding)
- `-Y` (trusted X11 forwarding)
- `-A` (agent forwarding)

can be set through your configuration file by adding lines with

- `ForwardX11 yes`
- `ForwardX11Trusted yes`
- `ForwardAgent yes`

in the corresponding sections of your configuration file. However, we do not recommend doing so in general, for these reasons:

- Enabling X11 forwarding by default for all of your connections can slow down your sessions, especially if your X11 client on your computer is misconfigured.
- Enabling trusted X11 forwarding comes with a risk. Should the server to which you are connecting to be compromised, a privileged user (`root`) could intercept keyboard activity on your local computer. Use trusted X11 forwarding *only when you need it*.
- Similarly, while forwarding your SSH agent is convenient and more secure than typing a password on a remote computer, it also comes with a risk. Should the server to which you are connecting to be compromised, a privileged user (`root`) could use your agent and connect to another host without your knowledge. Use agent forwarding *only when you need it*. We also recommend that, if you use this feature, you should combine it with `ssh-askpass` so that any use of your SSH agent triggers a prompt on your computer, preventing usage of your agent without your knowledge.