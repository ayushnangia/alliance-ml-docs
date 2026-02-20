# Git

Other languages:

- English
- [français](Git_fr.md)

[Git](https://en.wikipedia.org/wiki/Git) is a distributed, fast and secure source code management tool. The official Git website is [git-scm.com](https://git-scm.com/). Git was created by [Linus Torvalds](http://en.wikipedia.org/wiki/Linus_Torvalds) for the Linux project and is currently maintained by Junio Hamano.

## Operating principle

Contrary to older source code management tools, Git works in a distributed way. This means that developers do not depend on a central repository to commit their changes. Each Git repository contains the full history of the project. Each Git object (changeset, file, directory) is the leaf of a tree with multiple branches. Developing a project with Git is based on a model in which one branch corresponds to one feature. Many revisions of the feature may be archived before the branch gets merged with the main trunk. For a detailed explanation of branch development, we recommend reading [this page](http://nvie.com/posts/a-successful-git-branching-model/).

One especially interesting technique is *cherry-picking*, which is essentially taking part of a branch and merging it with another one.

## Basic usage

Generally, a project developer will:

1. configure the global Git environment;
2. clone or create a repository;
3. make changes;
4. commit changes;
5. push changes to another repository.

Since Git is distributed, there may not be an authoritative repository.

### Summary of commands

| Command | Description |
| --- | --- |
| git config | Configure git |
| git init | Create a new repository |
| git clone | Clone an existing repository |
| git add | Add a file or directory to a repository |
| git rm | Delete a file or directory from the repository |
| git commit | Commit changes to the repository |
| git push | Push changes to another repository |
| git pull | Pull changes from another repository and merge them with your own repository |
| git fetch | Fetch changes from another repository without merging them with yours |
| git merge | Merge changes to the repository |

| Command | Description |
| --- | --- |
| git blame | Show which authors last modified a file |
| git log | Show the commit history |
| git diff | Compare two versions |
| git status | Display the status of the current files |
| git show | Display various git objects |
| git cat-file | Display the content, type or size of objects |

| Command | Description |
| --- | --- |
| git branch | Manage development branches |
| git tag | Manage version tags |
| git remote | Manage remote repositories |
| git checkout | Check out a branch or a path |
| git reset | Change the head of a branch |

| Command | Description |
| --- | --- |
| git format-patch | Create a patch |
| git am | Apply a patch |
| git send-email | Send a patch by email |

| Command | Description |
| --- | --- |
| git bisect | Used to diagnose problems |
| git gc | Collect garbage objects |
| git rebase | Rebase history of the repository |
| git grep | Search for content |

### Configuring the global Git environment

This section is based on the [Software Carpentry - *Version Control with Git*](https://swcarpentry.github.io/git-novice/02-setup.html) lesson. When you start developing on a new system, you want to configure:

- Your name and email address, which will be associated with every commit. Note: this information will become **public** if you push your revisions to a public repository.

```
[name@server ~]$ git config --global user.name "First-name Last-name"
[name@server ~]$ git config --global user.email "email@address.ca"

```

- Limit yourself to only four threads, otherwise, your `git clone` commands may fail if they are using too many threads.

```
[name@server ~]$ git config --global pack.threads 4

```

- If you are not used to `vi`, you can set a different text editor for your commit messages.

```
[name@server ~]$ git config --global core.editor "nano -w"

```

- Finally, you may want to redefine the default name for the initial branch name. For example, `main`.

```
[name@server ~]$ git config --global init.defaultBranch main

```

To list all options set in the global environment, run the following command.

```
[name@server ~]$ git config --list --global

```

### Creating or cloning a repository

The first step is usually to create your own repository, or to clone an existing one.

To create a repository:

```
[name@server ~]$ git init my-project

```

To clone a repository:

```
[name@server ~]$ git clone git://github.com/git/git.git

```

### Committing a change

When the repository is ready, you change directory and edit the file.

```
[name@server ~]$ cd my-project
[name@server ~]$ nano file.txt

```

When work is done, you add the file

```
[name@server ~]$ git add file.txt

```

then commit the change

```
[name@server ~]$ git commit

```

If the repository was cloned, it is now possible to push your changes to the original repository with

```
[name@server ~]$ git push origin main

```

In the above command, *origin* is the remote repository and *main* is the current branch that will be pushed.

You might have to use git push origin master for older git repositories.

## Hosting Git repositories

[GitHub](http://github.com) and [Bitbucket](http://bitbucket.org) are two of the main Git repository hosting services. They are both available for commercial projects as well as free projects.

## Troubleshooting

### Unable to create thread

If you see:

```
fatal: unable to create thread: Resource temporarily unavailable
fatal: fetch-pack: invalid index-pack output

```

This is caused by resource limitations on the cluster login nodes. The solution is to limit the number of threads to 2. Use the following command on each cluster:

```
[name@server ~]$ git config --global pack.threads "2"

```