
"""

Copyright (c) 2012, 2013 Rob Cakebread
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
            version='0.2',
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
        try:
            return myapp.run(argv)
        except ValueError, err:
            #Command does not exist
            MusubiApp.log.error(err)
            sys.exit(2)
        except KeyboardInterrupt, err:
            MusubiApp.log.error(err)
            pass
    else:
        return myapp.run(['-h'])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
