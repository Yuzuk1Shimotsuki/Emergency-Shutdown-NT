"""
MIT License

Copyright (c) 2025 Yuzuk1Shimotsuki

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import argparse
import ctypes
import sys
from enum import Enum

"""
This is a Python reimplementation of the emergency shutdown script that uses the Windows API to trigger a system shutdown. The souce code is based on the original C++ code from
https://www.codeproject.com/Articles/34194/Performing-emergency-shutdowns

One of the perfect example of Python to interact with low-level system APIs, similar to C or C++, without any noticeable perforamance degradation while having a much simpler syntax.

WARNING: This script will attempt to shut down your system by triggering `NtShutdownSystem()` directly.

It is intended for emergency situations only, and generally, requires Administrators Privilege to execute.

Do not run it unless you are prepared for an immediate hard shutdown.

HARDWARE DAMAGE or DATA LOSS may occur if this action was not done in a proper way. I am not responsible for any unwanted behavior of this program.

In case your computer doesn't start up again afterwards, it is not my fault. You are using this script at your own risk.

Proceed with caution and make sure you have saved all work before running it!!!

"""

class ShutdownAction(Enum):
    """
    An enum representing different shutdown actions.

    Each action corresponds to a specific shutdown behavior when calling `NtShutdownSystem()`.

    The values are based on the NTSTATUS codes used by the Windows API.

    Attributes
    ----------

    ShutdownNoReboot:
        Halts the system without rebooting or powering off.

    ShutdownReboot:
        Shuts down the system and then automatically reboots.

    ShutdownPowerOff:
        Completely halts and powers off the system.

    Details are provided in the docstrings for each action.

    """

    ShutdownNoReboot = 0
    """
    Halts the system without rebooting or powering off.
    - The OS kernel stops execution
    - All drivers and services shut down
    - No further action is taken
    - The screen may freeze or go black
    - You must manually reset or power off the machine afterwards

    Similar as the action after "It is now safe to turn off your computer." in older Windows or DOS versions (Windows 95, 98...)

    However, it would completely shut down the computer for modern systems based on some test, which is generally, not recommend.

    """

    ShutdownReboot = 1
    """
    Shuts down the system and then automatically reboots.
    - The OS kernel stops execution
    - Drivers and services shut down cleanly
    - Machine restarts after shutdown

    Same as the hidden "Emergency Restart" on Windows 10 or 11, which is not waiting for any software shutdown.
    """

    ShutdownPowerOff = 2
    """
    Completely halts and powers off the system.
    - The OS kernel stops execution
    - All drivers and services shut down
    - System is then powered off
    
    The most commonly used option for emergency shutdowns
    """

# Constants for privilege adjustment
# These constants are used to enable the shutdown privilege in the Windows API.
SE_SHUTDOWN_PRIVILEGE = 19

# Load ntdll.dll
ntdll = ctypes.WinDLL("ntdll")

# Load RtlAdjustPrivilege and NtShutdownSystem from ntdll.dll. Required for the shutdown operations
RtlAdjustPrivilege = ntdll.RtlAdjustPrivilege
RtlAdjustPrivilege.argtypes = [ctypes.c_ulong, ctypes.c_bool, ctypes.c_bool, ctypes.POINTER(ctypes.c_bool)]
RtlAdjustPrivilege.restype = ctypes.c_ulong

NtShutdownSystem = ntdll.NtShutdownSystem
NtShutdownSystem.argtypes = [ctypes.c_ulong]
NtShutdownSystem.restype = ctypes.c_ulong

def enable_shutdown_privilege():
    """
    Enable the shutdown privilege for the current process.
    
    This is necessary to allow the process to perform shutdown operations.

    Returns
    ----------

    bool
        Returns `True` if the privilege was successfully enabled, otherwise `False`.

    """
    return RtlAdjustPrivilege(SE_SHUTDOWN_PRIVILEGE, True, False, ctypes.byref(ctypes.c_bool())) == 0   # True if successful, False otherwise

def emergency_shutdown(action: ShutdownAction):
    """
    Perform an emergency shutdown of the system based on the specified action.
    
    Parameters
    ----------
    action : ShutdownAction
        The action to perform, which can be one of the `ShutdownAction` enum values.

    Returns
    ----------
    Any
        Returns `True` if the shutdown operation was successful, otherwise raises `SystemExit` with an error message.

        The return value is only useful for remote debugging, as the system will shut down immediately if you execute this script in your local environment.

    Raises
    ---------
    SystemExit
        An error message will be printed with the `NTSTATUS` code if the shutdown operation fails.

    """
    has_privilege = enable_shutdown_privilege()

    if not has_privilege:
        raise SystemExit(f"Failed to enable shutdown privilege. Please check if you are running this script with sufficient privileges (SE_SHUTDOWN_PRIVILEGE).", has_privilege)
    
    status = NtShutdownSystem(action.value)

    if status != 0 and status == 3221225569:    # STATUS_PRIVILEGE_NOT_HELD, as this is the most common error when the process does not have the required privilege
        raise SystemExit(f"Failed to issue the selected shutdown command. Please check if you are really sure about that the current process was has SE_SHUTDOWN_PRIVILEGE, and try again later. NTSTATUS: 0x{status:08X}", status)
    
    if status != 0:   # Other errors
        raise SystemExit(f"Failed to issue the selected shutdown command. Please try again later. NTSTATUS: 0x{status:08X}", status)
    
    # The system may already be shutting down if you execute this script in your local environment. This was purposed for remote debugging.
    return True

def parse_args():
    """
    Helper function to parse command line arguments
    This is only used when the script is run directly from the command line.

    Returns
    ----------
    argparse.Namespace
        Returns the parsed command line arguments as an `argparse.Namespace` object.
    
    """
    class CustomArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help()
            self.exit(2, f"\n[ERROR] {message}\n")

    parser = CustomArgumentParser(description="Perform an emergency system shutdown using Windows native API (NtShutdownSystem).")
    # Mutually exclusive group - only one shutdown type can be selected
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--noreboot", "--ShutdownNoReboot", action="store_true", help="Halt system")
    group.add_argument("-r", "--reboot", "--ShutdownReboot", action="store_true", help="Emergency reboot")
    group.add_argument("-p", "--poweroff", "--ShutdownPowerOff", action="store_true", help="Emergency power off")

    return parser.parse_args()





# Entry point for the script
# This allows the script to be run directly from the command line.
# The script may also be imported as a module without executing the shutdown immediately.
if __name__ == "__main__":
    args = parse_args()

    if args.noreboot:
        action = ShutdownAction.ShutdownNoReboot

    elif args.reboot:
        action = ShutdownAction.ShutdownReboot

    elif args.poweroff:
        action = ShutdownAction.ShutdownPowerOff

    else:
        # This should never happen theoretically due to the mutually exclusive group in argparse
        action = None
        raise SystemExit("Error: No valid shutdown action provided.", 1)

    # Shut down the system with the selected action
    emergency_shutdown(action)

