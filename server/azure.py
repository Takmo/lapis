# See LICENSE file in top directory!

import os
from shutil import copytree
from StringIO import StringIO
from subprocess import call, PIPE, Popen
from time import sleep
from thread import start_new_thread

class AzureProcess:
    def __init__(self, command, wait=True, printcmd=False):
        # Initialize all fields.
        self.proc = None
        self.out = None
        self.err = None

        # Start the process.
        command.insert(0, "azure")
        if printcmd:
            print(command)
        self.proc = Popen(command, stdout=PIPE, stderr=PIPE)

        # Perhaps wait until completed.
        while wait and self.proc.poll() is None:
            self.communicate()

    def communicate(self):
        if self.proc.poll() is None:
            self.out, self.err = self.proc.communicate()
        return (self.out, self.err)

    def kill(self):
        if self.proc.poll() is None:
            self.proc.terminate()

    def poll(self):
        return self.proc.poll()

    def readline(self):
        if self.proc.poll() is None:
            return self.proc.stdout.readline()
        return ""

    def wait(self):
        return self.proc.wait()

# We want to use this method on the future, but we need something to show.
def azure_login_longterm():
    # Launch the login process.
    proc = AzureProcess(["account", "download"])
    
    out = proc.communicate()[0]
    index = out.find("http")
    url = out[index:index+60].partition("\n")[0]
    
    print url

def azure_login():
    # Launch the login process.
    proc = AzureProcess(["login"], wait=False)

    # Wait for the code, then print it!
    while True:
        out = proc.readline()
        if "sign in" in out:
            # Isolate the code by itself.
            ci = out.find("code") + 5
            code = out[ci:ci+9]

            # Print the code.
            print "Go to https://aka.ms/devicelogin and enter the following code: " + code
            break
        else:
            sleep(0.5)

    # Wait for login to finish.
    proc.wait()

    # Display results.
    if proc.poll() is 0:
        print "Azure login successful!"
    else:
        print "There was an error logging in."

def azure_create_server(name, location="Central US", image="", sshkey=""):
    # Set the image appropriately.
    if image is "":
        image = "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_5-LTS-amd64-server-20151117-en-us-30GB"

    # First we have to create a cloud service.
    print "Creating CloudService %s." % name
    proc = AzureProcess(["service", "create", "--location", location, name], printcmd=True)
    if proc.poll() is not 0:
        print proc.communicate()[1]
        return
    else:
        print "CloudService %s successfully created in zone %s." % (name, location)

    # Next create the VM.
    username = "minecraft"
    password = "Lap1sTemp!"
    print "Creating VM %s. This might take a while..." % name
    proc = AzureProcess(["vm", "create", "--ssh", "22", name, image, username, password], printcmd=True)
    if proc.poll() is not 0:
        print proc.communicate()[1]
        return
    else:
        print "VM %s successfully created." % name

    # Open an Endpoint for Minecraft Server (25565)
    print "Opening port 25565 for Minecraft."
    proc = AzureProcess(["vm", "endpoint", "create", name, "25565", "25565"])
    if proc.poll() is not 0:
        print proc.communicate()[1]
        return
    else:
        print "Port opened successfully."

    # Attempt to copy home SSH key to authorized_keys.
    # Make sure the directory exists.
    if not os.path.exists("./.ssh"):
        os.makedirs("./.ssh")
    with open("./.ssh/authorized_keys", "w") as outfile:
        with open("/home/celdir/.ssh/id_rsa.pub", "r") as infile:
            outfile.write(infile.read())
            outfile.write("\n")
        outfile.write(sshkey)

    # Wait until we can SSH into server (or alternatively fail after 10 minutes).
    print "Waiting for server to become active."
    tries = 0
    while call(["sshpass", "-p", password, "ssh", "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
        "%s@%s.cloudapp.net" % (username, name), "uname -a"]) is not 0:
        if tries is 60:
            print "Server never became active. Giving up."
            return
        tries = tries + 1
        sleep(10)
    print "Server is online and accessible!"

    # Copy everything to the server.
    print "Copying files to server."
    if call(["sshpass", "-p", password, "scp", "-o", "StrictHostKeyChecking=no", "-r", "../ShutdownManager",
        "%s@%s.cloudapp.net:~" % (username, name)]) is not 0:
        print "Error copying ShutdownManager to server. Giving up."
        return
    if call(["sshpass", "-p", password, "scp", "-o", "StrictHostKeyChecking=no", "-r", "./.ssh",
        "%s@%s.cloudapp.net:~" % (username, name)]) is not 0:
        print "Error copying authorized_keys to server. Giving up."
        return
    if call(["scp", "-o", "StrictHostKeyChecking=no", "../install.sh",
        "%s@%s.cloudapp.net:~" % (username, name)]) is not 0:
        print "Error copying install.sh to server. Giving up."
        return
    print "Finished copying files to server!"

    # Run the install.sh script
    print "Running install script on server."
    if call(["ssh", "-o", "StrictHostKeyChecking=no",
        "%s@%s.cloudapp.net" % (username, name), "chmod +x ./install.sh"]) is not 0:
        print "Error making installer executable. Giving up."
        return
    if call(["ssh", "-o", "StrictHostKeyChecking=no",
        "%s@%s.cloudapp.net" % (username, name), "./install.sh"]) is not 0:
        print "Error running install script. Giving up."
        return
    print "Install script completed successfully."

    # Everything should be done!
    print "Installation should have completed successfully!"
    print "Try connecting to %s.cloudapp.net in Minecraft!" % name

def azure_start(name):
    # Start the VM.
    print "Starting VM %s. This might take a while..." % name
    proc = AzureProcess(["vm", "start", name])
    if proc.poll() is not 0:
        print proc.communicate()[1]
        return
    else:
        print "VM %s successfully started." % name

    # Wait for it to come up.
    tries = 0
    while not can_ssh("minecraft", name):
        if tries is 60:
            print "Server never became active. Giving up."
            return
        tries = tries + 1
        sleep(10)
    print "Server is online and accessible!"

    # Run start.sh
    if call(["ssh", "-o", "StrictHostKeyChecking=no",
        "%s@%s.cloudapp.net" % ("minecraft", name), "screen -d -m ./spigot/start.sh"]) is not 0:
        print "Error running start script. Giving up."
        return
    print "Start script completed successfully."
    
def azure_stop(name):
    # Stop the VM
    print "Stopping VM %s. This might take a while..." % name
    proc = AzureProcess(["vm", "shutdown", name])
    if proc.poll() is not 0:
        print proc.communicate()[1]
        return
    else:
        print "VM %s successfully stopped." % name

def can_ssh(username, name):
    if call(["ssh", "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
        "%s@%s.cloudapp.net" % (username, name), "uname -a"]) is not 0:
        return False
    return True


