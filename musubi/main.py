
"""

Copyright (c) 2012, Rob Cakebread
All rights reserved.

"""

import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class MusubiApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(MusubiApp, self).__init__(
            description='Musubi DNSBL checker',
            version='0.1',
            command_manager=CommandManager('musubi.cli'),
        )

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = MusubiApp()
    if len(argv):
        return myapp.run(argv)
    else:
        # It goes into interactive mode by default if no args, we want help
        return myapp.run(['-h'])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
