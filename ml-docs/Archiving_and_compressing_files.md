# Archiving and compressing files

Other languages:

- English
- [français](Archiving_and_compressing_files_fr.md)

*Parent page: [Storage and file management](Filesystem.md)*

[Archiving](https://en.wikipedia.org/wiki/Archive_file) means creating one file that contains a number of smaller files within it. Reducing the number of files by creating an archive can improve the efficiency of file storage and help you stay within [quota limits](Filesystem.md#Filesystem_quotas_and_policies). Archiving can also improve the efficiency of [file transfers](General_directives_for_migration.md). It is faster for the secure copy protocol ([scp](https://en.wikipedia.org/wiki/Secure_copy)), for example, to transfer one archive file of a reasonable size than thousands of small files of equal total size.

[Compressing](https://en.wikipedia.org/wiki/Data_compression) means encoding a file such that the same information is contained in fewer bytes of storage. The advantage for long-term data storage should be obvious. For [data transfers](General_directives_for_migration.md), the time spent for compressing data must be balanced against the time saved moving fewer bytes as described in this discussion of [data compression and transfer](https://bluewaters.ncsa.illinois.edu/data-transfer-doc) from the US National Center for Supercomputing Applications.

- The best-known tool for archiving files in the Linux community is tar. Here is [a tutorial on 'tar'](Tar.md).
- A replacement for tar called dar offers some advantages in functionality. Here is [a tutorial on 'dar'](Dar.md). Both tar and dar can compress files as well as archive.
- The zip utility, more commonly used in the Windows community but available on our clusters, also provides both archiving and compression.
- Compression tools gzip, bzip2 and xz can be used in conjunction with tar, or by themselves.