# See LICENSE file in top directory!

from subprocess import PIPE, Popen
from time import sleep

class AzureProcess:
    def __init__(self, command, wait=True, printcmd=False):
        # Initialize all fields.
        self.proc = None
        self.out = None
        self.err = None

        # Start the process.
        command.insert(0, "azure")
        if printcmd:
            print command
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

def azure_create_server(name, location="Central US", image=""):
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
