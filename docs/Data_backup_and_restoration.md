# Data backup and restoration

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

Some important numbers include the maximum number of file changes everyday by a user are needed to prevent users individual backups from becoming bottlenecks for the whole backup processes.

TSM /project backup

- The most recent version is always kept
- Number of inactive versions of files to be kept : 1 (2nd copy)
- Time to keep inactive versions : 60 days
- Number of deleted versions to be kept : 1
- Time to keep deleted versions : 60 days
- Maximum number of file changes per day by every project : 50k files

TSM /project archival

- Default archival allocation per project : 10 TB
- Maximum time to keep archive : 1 year
- Maximum number of files to be archived : 50k files
- Number of copies of archived files to keep : 1

TSM /project restore

- Maximum number of files to be restored per project per day : 50k files
- Maximum restore size per day : 10TB