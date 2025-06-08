# Emergency-Shutdown-NT

A Python utility to shutdown or restart Windows instantly

> [!WARNING]
> This script will attempt to shut down your system by triggering `NtShutdownSystem()` directly. It is intended for emergency situations only, and generally, requires Administrators Privilege to execute. Do not run it unless you are prepared for an immediate hard shutdown.
>
> **HARDWARE DAMAGE** or **DATA LOSS** may occur if this action was **not done in a proper way**. I am **not responsible** for any **unwanted behavior** of this program.
>
> In case your computer **doesn't start up again afterwards**, it is **not my fault**. You are using this script **at your own risk**.
> Proceed with caution and make sure you have **saved all work** before running it!!!

## Introduction

This is a Python reimplementation of the Emergency Shutdown script that uses the Windows API `NtShutdownSystem()` to trigger a system shutdown. It provides in a cleaner form and becomes more beginner-friendly.

One of the perfect example of Python to interact with low-level system APIs, similar to C or C++, without any noticeable perforamance degradation while having a much simpler syntax.


> [!NOTE]
> The souce code is based on the original C++ code from https://www.codeproject.com/Articles/34194/Performing-emergency-shutdowns

## Background

I was wondering if there are any methods to simulate the long-press of Power Button or Reset button on my PC case, which I figured out the article mentioned above serval years ago.

However, when I was planning to re-visit the artcle on my new PC, all the file links in that article were dead though the article still opens...

I didn't think much of it and tried to recompile a copy for myself based on their info, which was a total failure.

Looking on most of the bloggers who also failed to replicate it makes me desperate. The project was halted at that moment.

This was happened until a few months ago, when I was planning to integrate a Remote PC control system with HA, which the force restart and shutdown feture would likely be implemented.

I then came up with an idea: Why not just rewrite it completely in Python? Why I'm just overcompilcating things?

So, I decided to rewrite the entire script from C++ into Python. And that's pretty much it.

## Features

- Shut down or restart your computer by force. Nothing else.

## Using the code

### Options:
  - `-h`, `--help`: Show the help message and exit
  - `-n`, `--noreboot`, `--ShutdownNoReboot`: Halt system
  - `-r`, `--reboot`, `--ShutdownReboot`: Emergency reboot
  - `-p`, `--poweroff`, `--ShutdownPowerOff` Emergency power off

<br>

There are 2 ways to use the code:
- Using the `.exe` file
   - Head over to [Release](https://github.com/Yuzuk1Shimotsuki/Emergency-Shutdown-NT/releases) section and download the lastest pre-compiled `.exe` file. Run it as an administrator.
     ```bash
     YOUR_DOWNLOAD_LOCATION\EmergencyShutdown.exe --YOUR_OPTION
     ```
  
- Execute the source code
   - Download / Clone the repo and execute the `.py` source code in your Terminal. Run the Terminal as an administrator.
     ```bash
     git clone https://github.com/Yuzuk1Shimotsuki/Emergency-Shutdown-NT.git YOUR_LOCATION
     ```
     
     ```bash
     YOUR_LOCATION\EmergencyShutdown.py --YOUR_OPTION
     ```
     
Replace `YOUR_OPTION` with the options above.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
