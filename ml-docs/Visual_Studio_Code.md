# Visual Studio Code

Other languages:

- English
- [français](Visual_Studio_Code_fr.md)

[Visual Studio Code](https://code.visualstudio.com/) is an integrated development environment (IDE) from [Microsoft](https://www.microsoft.com) which can be used for local development with numerous extensions and is highly customizable.

Resources eager

Vs Code is notable for misbehaving on the login nodes. Whenever possible **strictly** use it locally or see to configure it below.

Running or debugging your code

If Visual Studio Code is connected to remote systems, avoid running or debugging your code, as this will execute code on the login nodes, which can lead to performance issues or system disruptions. Instead, use the code-server environment, which provides a safer and more appropriate context for debugging tasks.

- Use VS Code locally and avoid connecting it to the systems. Save your changes to your project files with Git, and pull the changes onto the systems when ready to test.
- Use nano or vim to edit files directly on the systems.
- For debugging and quick testing, you can load the code-server module.
- When all the above are not possible, one can configure VS Code for remote connections.

# Local usage

The advantages of using VS Code locally are

- speed & stability: running VS Code locally means fewer network interruptions and faster performance, which is ideal for iterative development;
- direct access: you can interact with files, extensions, and terminals directly on your machine with zero latency;
- offline capability: you’re not tied to an internet connection or remote server, so you can code anytime, anywhere.

It is recommended to develop locally with VS Code. You are then able to customize and extend VS Code with your preferred extensions and language.

Once you are ready to test your project on the systems, you can save your changes into a Git repository, push them to a remote host like GitHub or GitLab, then connect to the system and pull your changes to perform the test.

To learn more on how to work with source control, please see [VS Code Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview).

Once you have saved and pushed your changes to your remote repository, connect to the system via the terminal.

```
[name@server ~]$ ssh <username>@<hostname>.alliancecan.ca

```

Then clone your repository (if it does not exist).

```
[name@server ~]$ git clone git@github.com:username/reponame.git

```

or change directory to your repository and pull the changes with

```
[name@server ~]$ cd myrepo
[name@server ~]$ git pull

```

You can then test your changes in a short (with minimal resources) [interactive job](Scheduler.md#Interactive_jobs).

# File edition on the systems

While VS Code is great for local development, sometimes you need direct access to files on a remote system. In such cases, terminal-based editors like nano or vim offer a lightweight and efficient way to edit files directly from the command line.

If you prefer a graphical interface, the [JupyterLab](JupyterLab.md) text editor provides a versatile alternative. It supports Markdown, Python scripts, and other formats.

# Debugging and testing

If you need to debug or test your code on the systems, you can start a [code-server instance from Jupyter Lab](JupyterLab.md#VS_Code).

1. Access one of the [options to launch JupyterLab](JupyterLab.md#Launching_JupyterLab).
2. Select minimal resources and start an interactive JupyterLab job.
3. On the Launcher tab, click on the VS Code launcher button.

| The code-server instance you are accessing is running in a compute job that does not have internet access. |
| --- |

The code-server module has several common extensions already available, but we can add more upon request.

## Custom extension installation

TBD...

# Configuration of VS Code for remote connection

If none of the above works for your case, one can configure VS Code to connect to a remote host with the Remote SSH extension.

## SSH configuration

If not done already, [generate your SSH key](SSH_Keys.md#Generating_an_SSH_Key) and [add your *public* SSH key on the CCDB](SSH_Keys.md#Installing_your_key).

Then create (or add) an SSH configuration file to your local computer:

**File :** ~/.ssh/config

```
Host *
  ServerAliveInterval 30
  User your_username

Host rorqual narval nibi fir
  HostName %h.alliancecan.ca

```

## Local configuration

1. In VS Code, open the Command Palette: Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (macOS).

2. Open the user settings (Preferences: Open User Settings (JSON)) and paste (or merge) the following configuration:

**File :** local-settings.json

```
{
  // file-watch + search
  "files.watcherExclude": {
    "**/.git/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/build/**": true,
  },
  "search.exclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true,
  },
  "search.maxThreads": 2,
  "search.ripgrep.maxThreads": 2,
  "search.useIgnoreFiles": true,

  // extensions & updates
  "remote.extensionKind": {
    "*": [
      "ui"
    ],
    "ms-python.python": [
      "ui"
    ]
  },
  "remote.defaultExtensionsIfInstalledLocally": [
    "GitHub.vscode-pull-request-github"
  ],

  // remote-ssh
  "remote.SSH.showLoginTerminal": false,
  "remote.SSH.enableDynamicForwarding": false,
  "remote.SSH.enableServerAutoShutdown": 30,

  "workbench.startupEditor": "none",
}

```

3. Save it and restart VS Code.

## Remote system configuration

1. Log in to the system via an external terminal.

```
[name@server ~]$ ssh <username>@<host>.alliancecan.ca

```

2. Create the directory.

```
[name@server ~]$ mkdir -p ~/.vscode-server/data/Machine/

```

3. Create the settings.json machine configuration.

```
[name@server ~]$ nano ~/.vscode-server/data/Machine/settings.json

```

4. Copy the configuration below. You may need to manually merge settings with your own if any already.

**File :** system-settings.json

```
{
  // file-watch + search
  "files.watcherExclude": {
    "**/.git/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/build/**": true,
    "/**": true,
  },
  "search.exclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true,
    "/**": true,
  },
  "search.followSymlinks": false,
  "search.maxThreads": 2,
  "search.ripgrep.maxThreads": 2,
  "search.useIgnoreFiles": true,
  "search.searchOnType": false,

  // extensions & updates
  "extensions.autoCheckUpdates": false,
  "extensions.autoUpdate": false,
  "update.mode": "none",
  "remote.extensionKind": {
    "*": [
      "ui"
    ],
    "ms-python.python": [
      "ui"
    ]
  },

  // Copilot
  "chat.agent.enabled": false,
  "github.copilot.enable": {
    "*": false,
  },
  "remote.defaultExtensionsIfInstalledLocally": [
    "GitHub.vscode-pull-request-github"
  ],

  // telemetry & git
  "telemetry.enableTelemetry": false,
  "telemetry.enableCrashReporter": false,
  "telemetry.telemetryLevel": "off",
  "telemetry.feedback.enabled": false,
  "git.autofetch": false,
  "git.enableStatusBarSync": false,

  // remote-ssh
  "remote.SSH.showLoginTerminal": false,
  "remote.SSH.enableDynamicForwarding": false,
  "remote.SSH.enableServerAutoShutdown": 30,

  "workbench.startupEditor": "none",
}

```

## Connecting

1. Open the Command Palette in VS Code: Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (macOS).
2. Type remote and then select Connect to Host...
3. Choose the host (remote system) and confirm.

You'll now be connected to a **login node**.

Login Node

Do *not* test, debug or run your code as it runs on the login node!

## Closing your connection

1. Open the Command Palette in VS Code: Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (macOS).
2. Type remote and then select Remote-SSH: Kill VS Code Server on Host...
3. Choose the host (remote system) and confirm.
4. Open the File menu, and select Close Remote Connection.

## Advanced - Connecting to an interactive compute node

The following is only needed for advanced usage.

Update your ssh configuration to add the following lines:

NarvalRorqual

**File :** ~/.ssh/config

```
Host nc* ng* nl*
  ProxyJump narval
  User your_username

```

**File :** ~/.ssh/config

```
Host rc* rg* rl*
  ProxyJump rorqual
  User your_username

```

1. In an external terminal, connected to the system via an ssh connection, start a new **[interactive job](Scheduler.md#Interactive_jobs)** (with `salloc`) with at least 2000M of memory.
   1. Note the allocated compute node name.
   2. If you need to work with `SLURM_*` environment variables in VS Code, save them all in a *source* file:

```
[name@server ~]$ env | grep SLURM_ | sed -e 's/^\(.*\)=\(.*\)$/export \1="\2"/g' > slurm_var.sh

```

1. In VS Code, start a new remote session with the name of the allocated compute node.
   1. Press `F1` or `Ctrl+Shift+P` to start the command prompt `>` in the Command Palette.
   2. Start typing *Remote* and select *Remote-SSH: Connect to Host... **> Remote-SSH: Connect to Host...***
   3. Enter the noted compute node name.
      1. If you get prompted for the type of operating system, select **Linux**.
2. If you need to work with `SLURM_*` environment variables, navigate to the working directory in a VS Code terminal and *source* the `slurm_var.sh` file.

```
[name@server ~]$ source slurm_var.sh

```

# Special notes

- VScode is banned on tamIA login nodes.