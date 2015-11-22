yes | sudo apt-get install git openjdk-7-jre-headless openjdk-7-jdk tar ant
sed -i -- 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sudo service ssh restart
cd ~/
mkdir spigot
cd spigot/
curl -o BuildTools.jar https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
git config --global --unset core.autocrlf
java -jar BuildTools.jar 
echo "#/bin/sh" > start.sh
sed -i '$ a\java -Xms512M -Xmx1024M -jar spigot-1.8.8.jar' start.sh
chmod +x start.sh
./start.sh 
sed -i -- 's/false/true/g' eula.txt
cd ~/ShutdownManager
cp ~/spigot/Spigot/Spigot-API/target/spigot-api-1.8.8-R0.1-SNAPSHOT.jar spigot.jar
ant jar
cp server/plugins/ShutdownManager.jar ~/spigot/plugins/
cd ~/spigot/
./start.sh
