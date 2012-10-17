
import os
from fabric.api import run,local,env 
from fabric.contrib import files
from fabric.operations import sudo
import time

dwndir = '/home/%s/installs' % env.user


def DownloadNagios():
	"""
	Used to Download Nagios
	"""
	MKDIR_CMD = "mkdir /home/%s/installs" % env.user
	run(MKDIR_CMD)
	DWNNAGIOS_CMD = "wget -P %s http://freefr.dl.sourceforge.net/project/nagios/nagios-3.x/nagios-3.4.1/nagios-3.4.1.tar.gz" % (dwndir)
	run(DWNNAGIOS_CMD)
def DependencesSSL():
	sudo("apt-get install -y --force-yes openssl libssl-dev")

def UbuntuDependencyInstall():
        sudo("apt-get install -y --force-yes apache2")
        sudo("apt-get install -y --force-yes libapache2-mod-php5")
        sudo("apt-get install -y --force-yes build-essential")
        sudo("apt-get install -y --force-yes libgd2-xpm-dev")
        sudo("apt-get install -y --force-yes xinetd")
	DependencesSSL()

def DependencyInstall():
	"""
	Used to install Dependencies
	"""
	os = run("uname -a | cut -d' ' -f4 | cut -c 5-10")
	if os == "Ubuntu":
		UbuntuDependencyInstall()
	else:
		NonUbuntuDependencyInstall()

def ExtractNagios():
	"""
	Used TO Extract Nagios Downloaded Package
	"""
	TAR_CMD = "cd %s && tar -zxvf nagios-3.4.1.tar.gz" % (dwndir)
	run(TAR_CMD)

def Createuser():
	"""
	Used to Create Nagios User, Group & Adding Nagios User & Apache USer to Nagios Group
	"""
	CHCK_USR_CMD = "cat /etc/shadow | grep nagios | awk -F: '{ print $1 }'"
	if sudo(CHCK_USR_CMD) == "nagios":
		run("echo 'user nagios already exists'")
	else:
		sudo("useradd -m nagios")
	CHCK_GRP_CMD = "cat /etc/group | grep nagcmd | awk -F: '{ print $1 }'"
	if sudo(CHCK_GRP_CMD) == "nagcmd":
		run("echo 'group nagcmd already exist'")
	else: 
		sudo("groupadd nagcmd")
		sudo("usermod -a -G nagcmd nagios")
		sudo("usermod -a -G nagcmd apache")

def RunConfigScript():
	"""
	Used to Run Nagios Configure Script
	"""
	CONF_CMD = "cd %s/nagios && ./configure --with-command-group=nagcmd" % (dwndir)
	sudo(CONF_CMD)

def CompileSource():
	"""
	Used to Compile Nagios Source Code
	"""
	COMP_CMD = "cd %s/nagios && make all" % (dwndir)
	sudo(COMP_CMD)

def InstallSource():
	"""
	Used to Install Compiled Source Code
	"""
	INST_CMD = "cd %s/nagios && make install" % (dwndir)
	sudo(INST_CMD)
	INIT_CMD = "cd %s/nagios && make install-init" % (dwndir)
	sudo(INIT_CMD)
	INST_CONF_CMD = "cd %s/nagios && make install-config" % (dwndir)
	sudo(INST_CONF_CMD)
	INST_CMD_MODE = "cd %s/nagios && make install-commandmode" % (dwndir)
	sudo(INST_CMD_MODE)
	INST_WEB_CMD = "cd %s/nagios && make install-webconf" % (dwndir)
	sudo(INST_WEB_CMD)
	CRT_USR_CMD = "cd %s/nagios && htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin" % (dwndir)
	sudo(CRT_USR_CMD)
	
def ApacheRestart():
	"""
	Used to Restart Apache Server
	"""
	sudo("/etc/init.d/apache2 restart")

def NagiosPluginDownload():
	"""
	Used to Download Nagios Plugin
	"""
	DWNPLUGIN_CMD = "wget -P %s http://heanet.dl.sourceforge.net/project/nagiosplug/nagiosplug/1.4.16/nagios-plugins-1.4.16.tar.gz" % (dwndir)
	run(DWNPLUGIN_CMD)
	TAR_PLG_CMD = "cd %s && tar -zxvf nagios-plugins-1.4.16.tar.gz" % (dwndir)
	run(TAR_PLG_CMD)

def PluginConfig():
	"""
	Used to Run Plugin Configure Script
	"""
	PLG_CONF_CMD = "cd %s/nagios-plugins-1.4.16 && ./configure --with-nagios-user=nagios --with-nagios-group=nagios" % (dwndir)
	run(PLG_CONF_CMD)
	
def InstallPlugin():
	"""
	Used to Install Nagios Plugin
	"""
	PLG_COMP_CMD = "cd %s/nagios-plugins-1.4.16 && make" % (dwndir)
	sudo(PLG_COMP_CMD)
	PLG_INST_CMD = "cd %s/nagios-plugins-1.4.16 && make install" % (dwndir)
	sudo(PLG_INST_CMD)

def NagiosServiceAdd():
	"""
	Used to Add Nagios Service in System Startup
	"""
	SRVC_ADD_CMD = "chkconfig --add nagios && chkconfig nagios on"
	sudo(SRVC_ADD_CMD)

def NagiosVerify():
	"""
	Used to Verify Nagios Sample Config Files
	"""
	NGS_VRF_CMD = "/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg"
	sudo(NGS_VRF_CMD)

def NagiosRestart():
	"""
	Used to Restart Nagios Service
	"""
	NGS_RST_CMD = "/etc/init.d/nagios restart"
	sudo(NGS_RST_CMD)

def NagiosFullInstall():
	"""
	Used to Install Full Nagios
	"""
	DependencyInstall()
	DownloadNagios()
	ExtractNagios()		
	Createuser()
	RunConfigScript()
	CompileSource()
	InstallSource()
	ApacheRestart()
	NagiosInit()

def NagiosPluginFullInstall():
	"""
	Used to Install Full Nagios Plugin
	"""
	NagiosPluginDownload()
	PluginConfig()
	InstallPlugin()
	NagiosServiceAdd()
	NagiosVerify()
	NagiosRestart()

def Nagiosnrpe():
	"""
	Used to Download Nagios NRPE Client
	"""
	NRPE_DWNL_CMD = "wget -P %s http://nchc.dl.sourceforge.net/project/nagios/nrpe-2.x/nrpe-2.13/nrpe-2.13.tar.gz" % (dwndir)
	run(NRPE_DWNL_CMD)
	NRPE_EXT_CMD = "cd %s && tar -zxvf nrpe-2.13.tar.gz" % (dwndir)
	run(NRPE_EXT_CMD)
	CHCK_LIB_CMD = "ls /usr/lib/x86_64-linux-gnu/libssl.so"
	if run(CHCK_LIB_CMD) == "/usr/lib/x86_64-linux-gnu/libssl.so":
		run("echo Exist!")
		NRPE_SSL_CMD = "ln -s /usr/lib/x86_64-linux-gnu/libssl.so /usr/lib/libssl.so"
		sudo(NRPE_SSL_CMD)
	else:
		DependencesSSL()

def NrpeSetup():
	"""
	Used to Configure & Install NRPE Client NOTE: Before Running this command make sure openssl & openssl-devel packages are installed
	"""
	NRPE_CONF_CMD = "cd %s/nrpe-2.13 && ./configure" % (dwndir)
	run(NRPE_CONF_CMD)
	NRPE_MAKE_CMD = "cd %s/nrpe-2.13 && make all" % (dwndir)
	sudo(NRPE_MAKE_CMD)
	NRPE_PLG_CMD = "cd %s/nrpe-2.13 && make install-plugin" % (dwndir)
	sudo(NRPE_PLG_CMD)
	NRPE_DMN_CMD = "cd %s/nrpe-2.13 && make install-daemon" % (dwndir)
	sudo(NRPE_DMN_CMD)
	NRPE_DMNCONF_CMD = "cd %s/nrpe-2.13 && make install-daemon-config" % (dwndir)
	sudo(NRPE_DMNCONF_CMD)
	NRPE_XINETD_CMD = "cd %s/nrpe-2.13 && make install-xinetd" % (dwndir)
	sudo(NRPE_XINETD_CMD)
	NRPE_SRVC_CMD = "echo 'nrpe               5666/tcp                                  # NRPE' >> /etc/services"
	sudo(NRPE_SRVC_CMD)
	NRPE_STRT_CMD = "/etc/init.d/xinetd restart"
	sudo(NRPE_STRT_CMD)

def NrpeRestart():
	"""
	Used to Restart NRPE Service
	"""
	NRPE_STRT_CMD = "/etc/init.d/xinetd restart"
	sudo(NRPE_STRT_CMD)

def NrpeFullInstall():
	"""
	Used to Install NRPE NOTE: Before Running this command make sure openssl & openssl-devel packages are installed
	"""
	Nagiosnrpe()
	NrpeSetup()
	
	

