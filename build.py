import os
import urllib
import re

headless_path = os.getcwd()
eclipsky_path = os.environ["ECLIPSKY_PATH"] + "/no.hal.eclipsky"
emfs_path = os.environ["EMFS_PATH"]
p2_osgi_path =  os.environ["M2_PATH"]+"/repository/p2/osgi/bundle"
remove_unnecessary_directories = "^((?!tests)(?!ui)(?!.project)(?!.settings)(?!pom.xml)(?!.DS_Store)(?!.metadata)(?!jexercise).)*$"
osgi_framework_url = "http://ftp.halifax.rwth-aachen.de/eclipse//equinox/drops/S-NeonM5-201601282000/org.eclipse.osgi_3.11.0.v20160121-2005.jar"
paho_url = "https://repo.eclipse.org/content/repositories/paho-releases/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.0.2/org.eclipse.paho.client.mqttv3-1.0.2.jar"
filter_jars = "*.jar"
paho_path = os.environ["M2_PATH"] + "/repository/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.0.2/org.eclipse.paho.client.mqttv3-1.0.2.jar"




def build_emfs():
    command = "cp ./pom/emfs/pom.xml %s" % (emfs_path + "/pom.xml")
    os.system(command);
	os.chdir(emfs_path);
	os.system("mvn install; mvn package");
	for dir in os.listdir("."):
		match = re.match(remove_unnecessary_directories, dir)
		if (match):
			try:
				for file_name in os.listdir(dir+"/target/"):
					if ".jar" in file_name:
						command = "cp %s %s" % (dir+"/target/"+file_name, headless_path+"/plugins/")
						os.system(command)
			except:
				pass
	os.chdir(headless_path);


def build_eclipsky():
    command = "cp ./pom/eclipsky/pom.xml %s" % (emfs_path + "/pom.xml")
    os.system(command);
	os.chdir(eclipsky_path);
	os.system("mvn package");
	os.chdir("..")
	for dir in os.listdir("."):
		match = re.match(remove_unnecessary_directories, dir)
		if (match):
			try:
				for file_name in os.listdir(dir+"/target/"):
					if ".jar" in file_name:
						command = "cp %s %s" % (dir+"/target/"+file_name, headless_path+"/plugins/")
						os.system(command)

			except:
				print dir + ""
	os.chdir(headless_path)



def copy_p2_deps():
	os.chdir(p2_osgi_path)
	for dir in os.listdir("."):
		for file_name in os.listdir(dir + "/" + os.listdir(dir)[-1]):
			if ".jar" in file_name:
				command = "cp %s %s" % (dir + "/" + os.listdir(dir)[-1] + "/" + file_name, headless_path +"/plugins/")
				os.system(command)
	os.chdir(headless_path)


def copy_paho():
	command = "cp %s %s" % (paho_path, headless_path + "/plugins/")
	os.system(command)

def download_osgi_framework():
    osgi = urllib.URLopener()
    print "Downloading osgi framework"
    osgi.retrieve(osgi_framework_url, "plugins/org.eclipse.osgi_3.11.0.v20160121-2005.jar")
    print "Download osgi complete"
    os.chdir(headless_path)


build_emfs()
build_eclipsky()
copy_p2_deps()
copy_paho()
download_osgi_framework()
