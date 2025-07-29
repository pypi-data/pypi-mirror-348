""" Module to launch one pipeline to install kits to the remote servers  """
import logging

from .logs import Log
from .view import Show
from .execute import Exec
from .config.config import Config
from .context import Context
from .remote.sftp import Sftp
from .commands import Commands
from .local.local_kits import RunLocalKits
from .remote.remote_kits import RunRemoteKits

class Pipeline:
    """ Class where we will initiation the process to install kits on remote servers """

    def __init__(self, options):

        name = __name__.split(".")
        self.name = name[-1]
        logging.basicConfig(handlers=[logging.StreamHandler()],
                            format="%(asctime)s - %(name)s - " "[%(levelname)s] - %(message)s",
                            level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        self.options = options
        self.log = Log()
        self.sftp = Sftp()
        self.data = Config()
        self.file = "ikctl.yaml"
        self.context = Context()
        self.exe = Exec(Commands, self.logger)
        self.version = Config().version
        self.config_kits, self.path_kits = self.data.load_config_file_kits()
        self.config_servers, self.path_servers = self.data.load_config_file_servers()
        self.config_mode = self.data.load_config_file_mode()
        self.secrets, self.path_secrets = self.data.extrac_secrets()
        self.config_contexts = self.context.config
        self.view = Show(self.config_kits, self.path_kits, self.config_servers, self.path_servers, self.config_contexts, self.config_mode, self.path_secrets)
        self.servers = self.data.extract_config_servers(self.config_servers, self.options.name)
        if options.install:
            self.kits, self.pipe = self.data.extrac_config_kits(self.config_kits, self.options.install)
            self.run_remote_kits = RunRemoteKits(self.servers, self.config_kits, self.kits, self.pipe, self.sftp, self.exe, self.log, self.options, self.secrets)
            self.run_local_kits = RunLocalKits(self.servers, self.kits, self.pipe, self.exe, self.log, self.options)
        self.init()

    def init(self):
        """ Function to initiation pipeline """

        # Manage context
        if self.options.context:
            self.context.change_context(self.options.context)
        
        # Show configuration
        if self.options.list:
            self.view.show_config(self.options.list)
        
        # Install kits in servers
        if self.options.install:

            # Run kits in local machine
            if self.config_mode == 'local' or self.options.mode == 'local':
                self.run_local_kits.run_kits()

            # Run kits in remote servers
            elif self.config_mode == 'remote' or self.options.mode == 'remote':
                self.run_remote_kits.run_kits()