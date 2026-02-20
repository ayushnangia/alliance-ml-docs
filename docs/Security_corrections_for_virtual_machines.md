# Security corrections for virtual machines

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

If you are responsible for one or more virtual machines running in our cloud services, you may receive occasionally receive communications from our security team containing a list of security issues which have been detected on your VMs.
Here are suggested solutions to some issues which are commonly identified.

# HTTP TRACE / TRACK Methods Allowed

You can disable this in Apache by doing the following:

1. Add the line TraceEnable off to a configuration file such as /etc/httpd/conf.d/custom.conf.
2. Restart the httpd service.

# SSL Certificate Expiry, SSL Certificate Cannot Be Trusted, SSL Self-Signed Certificate, HSTS Missing From HTTPS Server

If you manage your own domain name for your VM, these error messages may be caused by Apache's default configuration, which serves a self-signed certificate that is installed when you install Apache. A simple solution is to tell Apache to not reply to requests other than your configured virtual hosts. This is done by removing the entire section for the default configuration, such as

```
<VirtualHost _default_:443>
...
</VirtualHost>

```

from your `/etc/httpd/conf.d/ssl.conf` file and then restarting the `httpd` service.