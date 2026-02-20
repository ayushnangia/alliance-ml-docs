# SSH security improvements

Other languages:

- English
- [français](SSH_security_improvements_fr.md)

[![](/mediawiki/images/thumb/3/33/FINAL_Flowchart_SSHD_changes_-_Summer_2019_-_v1.4_-_Copy.jpg/300px-FINAL_Flowchart_SSHD_changes_-_Summer_2019_-_v1.4_-_Copy.jpg)](FileFINAL_Flowchart_SSHD_changes_-_Summer_2019_-_v14_-_Copyjpg.md)

SSH security improvements flowchart (click to enlarge)

[SSH](SSH.md) is the software protocol that you use to connect to our clusters. It protects the security of your communication by verifying the server’s identity and yours against known identification data, and by encrypting the connection. Because security risks evolve over time, we will have ended support for certain SSH options which are no longer deemed secure. You will have to make some changes on your part in order to continue using our clusters. The changes are outlined in the flowchart to the right, and explained in greater detail below.

# SSH changes (September-October 2019)

Email explaining these changes (with "IMPORTANT" in the subject line) was sent to all users on July 29, and with more detail on September 16.

## What is changing?

The following SSH security improvements have been implemented on September 24, 2019 on Graham, and one week later on Béluga and Cedar:

1. Disable certain encryption algorithms.
2. Disable certain public key types.
3. Regenerate the cluster's host keys.

If you do not understand the significance of "encryption algorithms", "public keys", or "host keys", do not be alarmed. Simply follow the steps outlined below. If testing indicates you need to update or change your SSH client, you may find [page](SSH.md) useful.

Because users do not connect to Arbutus via SSH but through a web interface, the upcoming changes do not concern them.

There were earlier, less comprehensive updates made to both Niagara (on May 31, 2019; see [here](https://docs.scinet.utoronto.ca/index.php/SSH_Changes_in_May_2019)) and Graham (early August) which would have triggered some of the same messages and errors.

## Updating your client's known host list

The first time you login to one of our clusters after the changes, you will probably see a warning message like the following:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:mf1jJ3ndpXhpo0k38xVxjH8Kjtq3o1+ZtTVbeM0xeCk.
Please contact your system administrator.
Add correct host key in /home/username/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /home/username/.ssh/known_hosts:109
ED25519 host key for graham.computecanada.ca has changed and you have requested strict checking.
Host key verification failed.
Killed by signal 1.

```

This warning is displayed because the host keys on the cluster (in this case [Graham](Graham.md)) were changed, and your SSH client software remembers the old host keys. (It does this to prevent ["man-in-the-middle" attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).) This will happen for your SSH client on each device from which you connect, so you may see it multiple times.

You may also get a warning regarding "DNS spoofing", which is related to the same change.

### MobaXterm, PuTTY, or WinSCP

If you are using [MobaXterm](Connecting_with_MobaXTerm.md), [PuTTY](Connecting_with_PuTTY.md), or [WinSCP](https://winscp.net/eng/download.php) as your ssh (or scp) client under Windows, the warning will appear in a pop-up window and will allow you to accept the new host key by clicking "Yes". **Only click yes if the fingerprint matches one listed in [SSH host key fingerprints](SSH_changes.md#SSH_host_key_fingerprints)** at the bottom of this page. If the fingerprint does not match any on the list, do not accept the connection, and contact [Technical support](Technical_Support.md) with the details.

### macOS, Linux, GitBash or Cygwin

If you are using the command line ssh command on macOS, Linux, GitBash or Cygwin, you should tell your system to "forget" the old host key by running one of the following commands:

- Graham

```
for h in 2620:123:7002:4::{2..5} 199.241.166.{2..5} {gra-login{1..3},graham,gra-dtn,gra-dtn1,gra-platform,gra-platform1}.{sharcnet,computecanada}.ca; do ssh-keygen -R $h; done

```

- Cedar

```
for h in 206.12.124.{2,6} cedar{1,5}.cedar.computecanada.ca cedar.computecanada.ca; do ssh-keygen -R $h; done

```

- Beluga

```
for h in beluga{,{1..4}}.{computecanada,calculquebec}.ca 132.219.136.{1..4}; do ssh-keygen -R $h; done

```

- Mp2

```
for h in ip{15..20}-mp2.{computecanada,calculquebec}.ca 204.19.23.2{15..20}; do ssh-keygen -R $h; done

```

Afterwards, the next time you ssh to the cluster you'll be asked to confirm the new host keys, e.g.:

```
$ ssh graham.computecanada.ca
The authenticity of host 'graham.computecanada.ca (142.150.188.70)' can't be established.
ED25519 key fingerprint is SHA256:mf1jJ3ndpXhpo0k38xVxjH8Kjtq3o1+ZtTVbeM0xeCk.
ED25519 key fingerprint is MD5:bc:93:0c:64:f7:e7:cf:d9:db:81:40:be:4d:cd:12:5c.
Are you sure you want to continue connecting (yes/no)? 

```

**Only type yes if the fingerprint matches one listed in the [SSH host key fingerprints](SSH_changes.md#SSH_host_key_fingerprints)** at the bottom of this page. If the fingerprint does not match any on the list below, do not accept the connection, and contact [Technical support](Technical_Support.md) with the details.

## Troubleshooting

See the list of [SSH host key fingerprints](SSH_changes.md#SSH_host_key_fingerprints).

### My SSH key no longer works

If you're being asked for a password, but were using SSH keys previously on the same system,
it's likely because 1024-bit DSA & RSA keys have been disabled.

You need to generate a new stronger key. The process for doing this depends on the operating system you use, either [Windows](Generating_SSH_keys_in_Windows.md) or [Linux/macOS](Using_SSH_keys_in_Linux.md). Those instructions also describe how to add your client's new public key to the remote host, so that you can authenticate with the key rather than needing to provide a password.

### I can't connect!

If you see any of the following error messages:

```
Unable to negotiate with 142.150.188.70 port 22: no matching cipher found.
Unable to negotiate with 142.150.188.70 port 22: no matching key exchange method found.
Unable to negotiate with 142.150.188.70 port 22: no matching mac found.

```

you need to upgrade your SSH client to one of the compatible clients shown below.

### Which clients are compatible with the new configuration?

**The list below is not exhaustive**, but we have tested the configuration with the following clients. Earlier versions of these clients may or may not work. We recommend that you update your operating system and SSH client to the latest version compatible with your hardware.

#### Linux clients

- OpenSSH\_7.4p1, OpenSSL 1.0.2k-fips (CentOS 7.5, 7.6)
- OpenSSH\_6.6.1p1 Ubuntu-2ubuntu2.13, OpenSSL 1.0.1f (Ubuntu 14)

#### OS X clients

You can determine the exact version of your SSH client on OS X using the command ssh -V.

- OpenSSH 7.4p1, OpenSSL 1.0.2k (Homebrew)
- OpenSSH 7.9p1, LibreSSL 2.7.3 (OS X 10.14.5)

#### Windows clients

- [MobaXterm Home Edition](Connecting_with_MobaXTerm.md) v11.1
- [PuTTY](Connecting_with_PuTTY.md) 0.72
- Windows Services for Linux (WSL) v1
  - Ubuntu 18.04 (OpenSSH\_7.6p1 Ubuntu-4ubuntu0.3, OpenSSL 1.0.2n)
  - openSUSE Leap 15.1 (OpenSSH\_7.9p1, OpenSSL 1.1.0i-fips)

#### iOS clients

- Termius, 4.3.12

# SSH host key fingerprints

To retrieve the host fingerprints remotely, one can use the following commands:

```
ssh-keyscan <hostname> | ssh-keygen -E md5 -l -f -
ssh-keyscan <hostname> | ssh-keygen -E sha256 -l -f -

```

Listed below are the SSH fingerprints for our clusters. If the fingerprint you get does not match any on the list below, do not accept the connection, and contact [Technical support](Technical_Support.md) with the details.

## [Béluga](Beluga.md)

ED25519
:   `SHA256:lwmU2AS/oQ0Z2M1a31yRAxlKPcMlQuBPFP+ji/HorHQ`
:   `MD5:2d:d7:cc:d0:85:f9:33:c1:44:80:38:e7:68:ce:38:ce`

RSA
:   `SHA256:7ccDqnMTR1W181U/bSR/Xg7dR4MSiilgzDlgvXStv0o`
:   `MD5:7f:11:29:bf:61:45:ae:7a:07:fc:01:1f:eb:8c:cc:a4`

## [Fir](Fir.md)

ED25519

- `SHA256:NJgHnZFzGX0zYyUwCMUdWccvfCaTgKmZKzPaqL8VNM8`
- `MD5:fc:b2:c8:c3:7a:a3:fd:36:75:78:df:dd:6f:e8:88:31`

RSA

- `SHA256:J4oLl1Nb2fp0DXdRsGhZhzgCAO/zbH2Wg/I7Opy6ypk`
- `MD5:85:6a:10:2c:55:21:a4:53:57:25:20:db:90:f9:23:91`

## [Killarney](Vector.md)

ED25519

- `SHA256:M8R87mGQthsmxASCufmSZ/Q0uPY+7Nm+nizC5RP6LPg`
- `MD5:f6:ce:64:48:14:45:f5:d6:ce:e4:92:e9:81:24:13:77`

RSA

- `SHA256:eAhG9S8ZMTKq797dSyim5dpRAGU4DlN9hIMEmH5Go04`
- `MD5:78:59:b4:87:04:f6:da:3c:4a:a8:e2:ec:ad:7d:0b:3b`

## [Narval](Narval.md)

ED25519

- `SHA256:pTKCWpDC142truNtohGm10+lB8gVyrp3Daz4iR5tT1M`
- `MD5:79:d5:b2:8b:c6:2c:b6:3b:79:d2:75:0e:3b:31:46:17`

RSA

- `SHA256:tC0oPkkY2TeLxqYHgfIVNq376+RfBFFUZaswnUeeOnw`
- `MD5:bc:63:b5:f9:e6:48:a3:b7:0d:4a:23:26:a6:31:19:ef`

## [Nibi](Nibi.md)

ED25519

- `SHA256:iDzUuOogiUaSq47xp/v4IAegE53uLP5VtiP0WFXikRc`
- `MD5:e3:9b:3c:ad:b6:ee:5f:2e:1b:04:22:d2:97:47:fb:db`

RSA

- `SHA256:86vGOlyvaHUb9bYvQb/VAxxBGb/x2t5XlS0TeSnHN0A`
- `MD5:dd:82:77:5b:71:ab:27:c8:ff:47:66:41:9d:2b:82:40`

## [Rorqual](Rorqual.md)

ED25519 (256b)
:   `SHA256:Xe4zQTOysm5MbI2Euuo5ZKbrnTsqMUgUBRorb9MfYoU`
:   `MD5:6a:11:2c:d4:46:ff:87:fa:8f:7c:2e:02:c5:77:d7:06`

RSA (4096b)
:   `SHA256:VaR7wZmR2vOLIXCtPWhsU0SvdqJUMnrxFEmpk3SxuP4`
:   `MD5:43:1e:7f:64:b0:dd:f7:98:63:fc:40:8f:b0:43:83:25`

## [Siku](https://www.ace-net.ca/wiki/Siku)

ED25519 (256b)
:   `SHA256:F9GcueU8cbB0PXnCG1hc4URmYYy/8JbnZTGo4xKflWU`
:   `MD5:44:2b:1d:40:31:60:1a:83:ae:1d:1a:20:eb:12:79:93`

RSA (2048b)
:   `SHA256:cpx0+k52NUJOf8ucEGP3QnycnVkUxYeqJQMp9KOIFrQ`
:   `MD5:eb:44:dc:42:70:32:f7:61:c5:db:3a:5c:39:04:0e:91`

## [tamIA](TamIA.md)

ED25519

- `SHA256:QuJnAQCqMWr1qYJfV16pRLTaZmGHBgwgHFZHB+hkCTI`
- `MD5:c6:d1:f2:2f:be:0b:c2:d7:a1:15:92:d2:4e:63:5e:34`

RSA

- `SHA256:XixC3FjZPf/xnALTTw6dqscGTPluByKk/yuQAdG+BrM`
- `MD5:aa:de:59:f5:52:5a:a4:c5:14:cb:8a:ad:60:54:8c:87`

## [Trillium](Trillium.md)

ED25519

- `SHA256:ZdxQWOLHPQb11qPxHh2Vq+trSULZA1+rvTU6pePelSc`
- `MD5:22:cc:78:01:3c:36:65:ac:1a:44:94:37:62:d4:a3:e4`

RSA

- `SHA256:7lMM6nG32IWndLfCZhrJ6a/jKcuuvvajS6XUiRclB74`
- `MD5:06:ab:2a:3a:48:97:67:c1:ce:57:f2:7d:71:71:32:3b`