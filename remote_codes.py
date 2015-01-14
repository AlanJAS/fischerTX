#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Remote shell

comms = [
'?',                 # Outputs the list of valid commands
'help',              # Outputs the list of valid commands
'version',           # Outputs the current version number of the firmware
'get_ser_num',       # Outputs the ROBO TX Controller serial number
'get_board_ver',     # Outputs the hardware revision ID
'get_eeprom',        # Outputs a structured representation of the board data
'clean_disk',        # Deletes unnecessary files from the specified disk
'erase_disk',        # Erases the specified disk of the ROBO TX Controller
'erase_flashdisks',  # Erases all flash disks of the ROBO TX Controller
'erase_boot',        # Erases the bootstrap of the ROBO TX Controller
'erase_phase0',      # Erases the boot loader of the ROBO TX Controller
'dir',               # Displays the directory contents
'type',              # Outputs the contents of a text file
'del',               # Deletes the specified file
'copy',              # Copies the specified file
'format',            # Formats the specified disk
'ren',               # Renames the specified file
'xrecv',             # Activates the file receiving process on the ROBO TX Controller
'load',              # Loads a ROBO program from one of the disks into the program memor
'run',               # Starts the ROBO program that is currently in the program memory
'stop',              # Stops the currently running ROBO program
]


def get_comm(command):
    if command in comms:
        ret = [ord(e) for e in command]
        return [13] + ret + [13]
