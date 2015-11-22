sudo apt-get install git openjdk-7-jre-headless openjdk-7-jdk tar
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
./start.sh
