import os
import urllib
import re

headless_path = os.getcwd()
emfs_path = "../eclipsky/jexercise/no.hal.emfs.parent/"
eclipsky_path = "../eclipsky"
p2_osgi_path = "../../.m2/repository/p2/osgi/bundle"
remove_unnecessary_directories = "^((?!tests)(?!ui)(?!.project)(?!.settings)(?!pom.xml)(?!.DS_Store)(?!.metadata)(?!jexercise).)*$"
osgi_framework_url = "http://ftp.halifax.rwth-aachen.de/eclipse//equinox/drops/S-NeonM5-201601282000/org.eclipse.osgi_3.11.0.v20160121-2005.jar"
filter_jars = "*.jar"

    
def build_emfs():
	os.chdir(emfs_path);
	os.system("mvn install; mvn package");
	for dir in os.listdir("."):
		match = re.match(remove_unnecessary_directories, dir)
		if (match):
			for file_name in os.listdir(dir+"/target/"):
				if ".jar" in file_name:
					command = "cp %s %s" % (dir+"/target/"+file_name, headless_path+"/plugins/")
					os.system(command)

def build_eclipsky():
	os.chdir(eclipsky_path);
	os.system("mvn package");
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


def copy_p2_deps():
	os.chdir(p2_osgi_path)
	for dir in os.listdir("."):
		for file_name in os.listdir(dir + "/" + os.listdir(dir)[-1]):
			if ".jar" in file_name:
				command = "cp %s %s" % (dir + "/" + os.listdir(dir)[-1] + "/" + file_name, headless_path +"/plugins/")
				os.system(command)

def download_osgi_framework():
    osgi = urllib.URLopener()
    print "Downloading osgi framework"
    osgi.retrieve(osgi_framework_url, "plugins/org.eclipse.osgi_3.11.0.v20160121-2005.jar")
    print "Download osgi complete"


build_emfs()
os.chdir(headless_path);
build_eclipsky()
os.chdir(headless_path)
copy_p2_deps()
os.chdir(headless_path)
download_osgi_framework()
