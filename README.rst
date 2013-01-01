========================
Musubi the DNSBL Toolkit
========================

.. image:: http://imgur.com/WqRkx

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

Here are some of the commands you can try:

::

  (musubi)$ musubi mx cakebread.info
  (musubi)$ musubi ips cakebread.info
  (musubi)$ musubi spf dreamhost.com
  (musubi)$ musubi scan toad.com


::



To see help for an individual command, include the command name on the
command line::

  (musubi)$ musubi scan --help

Important
---------

If you pass an IP range in CIDR notation, please understand what you're 
doing. Each IP in that range will be tested against 70+ DNSBLs which
could potentially make thousands of DNS/UDP connections very quickly.
Do not try this at home! If you are an ISP or web hosting company,
it should not be a problem.

Cleaning Up
-----------

Finally, when done, deactivate your virtual environment::

  (musubi)$ deactivate
  $
