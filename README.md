- - - - - - - - - - - - 

This is my personal version:

- Remove ec2 functions

- fix bug in nrpe decompress tar.gz (Line 204/205) adding run(NRPE_EXT_CMD)

- add symlink for ssl library


- - - - - - - - - - - - - 

============
Nagios-Fabric
=============

Nagios-Fabric Script

This is Nagios Fabric Script for installation of NAGIOS, NAGIOS_PLUGIN & NRPE. This script can be used to deploy Nagios. You can also use this script to deploy Nagios on your server. just uncomment
the line env.host & add env.host="Ipaddress of Your Server" or if you want to install on multiple servers just add comma
seperated list of servers, for ex: env.host = "Ip-Server-1","Ip-Server-2"..."Ip-Server-n"

Usage :

install python fabric 

using easy install:

	easy_install fabric


using python-pip:

	pip install fabric

git clone https://github.com/agmance/Nagios-Fabric.git

cd Nagios-Fabric/

fab -l

fab NagiosFullInstall

fab NagiosPluginFullInstall

fab NrpeFullInstall

After Installation point your browser to http://IP-ADDRESS/nagios

- - - - - 
Ubuntu 12.04 (maybe 11.10) x64.

nrpe -> compile fails to find SSL libraries. Solution:

Add in line 6630 in configure file this path: /usr/lib/x86_64-linux-gnu/

or

ln -s /usr/lib/x86_64-linux-gnu/libssl.so /usr/lib/libssl.so <- Added in fabfile.py
