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

  - - - - - - - - - - - - 

This is my personal version:

- Remove ec2 functions

- fix bug in nrpe decompress tar.gz
