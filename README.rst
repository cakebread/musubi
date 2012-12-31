=================
 Running Musubi
=================

Setup
-----

First, you need to create a virtual environment and activate it.

::

  $ pip install virtualenv
  $ virtualenv musubi
  $ . musubi/bin/activate
  (musubi)$ 

Next, install ``musubi`` in the environment.

::

  (musubi)$ pip install musubi


Usage
-----

With musubi setup, you can now play with it.

To see a list of commands availble, run::

  (musubi)$ musubi --help

One of the available commands is "mx", try running it on any domain

::

  (musubi)$ musubi mx cakebread.info

produces something like the following

   5 mx1.google.com
   10 mx.fake.google.com


::



To see help for an individual command, include the command name on the
command line::

  (musubi)$ musubi scan --help

Cleaning Up
-----------

Finally, when done, deactivate your virtual environment::

  (musubi)$ deactivate
  $
