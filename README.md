# QUIPPL
Quick User Interface Portable Python Launcher - package a .py launcher
so you don't have to keep repackaging distributed code each update
----------

This tool is part of a complete package for rapid sharing of python
programs.  Many non-programmers would love to run your program but
don't want to worry about installing python and setting up the 
evironment.  QUIPPL helps the user to launch your program.

Step 1: package quippl using pyinstaller (ideally in the same python
environment used for the code you will be sharing) - the current 
prepackaged version is packaged using python 3.8

Step 2: copy the site-packages from your python environment/python 
installation that will run your code into the "dist" folder holding the
QUIPPL executable

Step 3: share the packaged QUIPPL with your user to have them run your 
code as a python file (instead of worrying about re-packaging every update, 
you can just send over the new .py version of your file)

QUIPPL includes a GUI for selecting the py file to be run.  Alternatively
you can provide the location of the file and its needed arguments via 
command line, bypassing the GUI tool.  You can also provide a 
QUIPPL_config.txt file to provide the necessary path to the .py file and it's
arguments to bypass the need for the user to select/do anything

@author: Christopher Scott Ward 2022
