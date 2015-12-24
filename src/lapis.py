# See the LICENSE file because you're pretty cool.

from json import loads
from logging import FileHandler, getLogger, StreamHandler
from Queue import Queue
from sys import stdout

# The lapis class represents the service itself.

class lapis:

    # Public Methods (you can call these)

    def get_state():
        """Returns the state of the server (since the last check_online())."""
        return self.state

    def start_server(self):
        """Attempt to start the server."""
        if not self.enabled or self.state != 'stopped':
            return False
        self.command_q.put(Command.START)
        return True

    def stop_server(self):
        """Attempt to stop the server."""
        if not self.enabled or self.state == 'stopped':
            return False
        self.command_q.put(Command.STOP)
        return True

    # Private Methods (you can technically call these, but don't)

    def __init__(self):
        # Setup logging.
        self.log = getLogger()
        self.log.addHandler(StreamHandler(stdout))
        self.log.addHandler(FileHandler("lapis.log"))

        # Setup lapis information.
        self.state = 'stopped'
        self.options = {}

        # Set ourselves enabled. If we discover that our configuration
        # is invalid, then we will disable ourself and prevent any
        # future interactions.
        self.enabled = True

        # Attempt to load configfile.
        self.load_config()

        # Prepare for multithreading goodness.
        self.command_q = Queue()
        self.last_cmd = Command.NONE

    def load_config(self, configfile='lapis.json'):
        """Load configuration information from a JSON file."""
        options = None
        try:
            with open(configfile) as cf:
                options = loads(cf.read())
        except(IOError):
            self.log.error("Unable to load configuration file. Does it exist?")
        except(ValueError):
            self.log.error("Invalid JSON in configuration file.")
        if options == None:
            return False
        self.options = options
        return True

    def tick(self):
        """Read and handle one command, then update state."""
        if not self.enabled:
            return

        # Get the next command (if any), but don't repeat the last command.
        cmd = Command.NONE
        if not self.command_q.empty():
            c = self.command_q.get()
            if c != self.last_cmd:
                cmd = c
                self.last_cmd = c

        # If state is not 'stopped', check if the server is online and SSHable.
        online = False
        ssh = False
        # TODO

        # Update state based on information.
        if online and ssh:
            self.state = 'running'

        # Handle the command.
        if cmd == Command.START and self.state == 'stopped':
            self.state = 'starting'
        if cmd == Command.STOP and self.state == 'running':
            self.state = 'stopping'

        # Interact with the server appropriately.
        # TODO

class Command:
    NONE = 0
    START = 1
    STOP = 2

