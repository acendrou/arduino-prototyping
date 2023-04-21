import argparse

from core.version import VERSION


# Parser for cli arguments
#
# options:
#
# - g
# --gui
# launch gui
#
# -v
# --verbose
# verbose mode: serial outputed to stdout
#
# -o <path>
# --output <path>
# save serial input to file, name by date to specified folder path
#
# -dp <plugin1> <plugin2>
# --disable-plugin <plugin1> <plugin2>
# disable plugin with list of plugin to disable
#
# -ep <plugin1> <plugin2>
# --enable-plugin <plugin1> <plugin2>
# enable plugin with list of plugin to enable - all other plugins loaded are disabled
#
# -sp <port>
# --serialport <port>
# serial port to open (takes precedence over other port config)
#
# -sr <baudrate>
# --serialrate <baudrate>
# serial baudrate to open port to (takes precedence over other port config)


# hold cli options
class CliState:
    is_raw_output_saved: bool = False
    raw_output_path = None

    verbose: bool = False
    gui: bool = False

    options: dict = {}

    monitorPort: str = None
    monitorSpeed: str = None

    enable_plugin_list: [str] = None
    disable_plugin_list: [str] = None

    def __init__(self):
        pass

    def set_raw_output_path(self, raw_output_path: str):
        self.is_raw_output_saved = True
        self.raw_output_path: str = raw_output_path

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def add_options(self, key: str, value):
        self.options[f"{key}"] = value

    def parser(self):
        try:

            parse = argparse.ArgumentParser(description='Analysis GUI' + " - " + VERSION,
                                            epilog="C3 Command, Control, Console - pretty console output & command and "
                                                   "control & see (c)")

            parse.add_argument('-v', '--verbose', action='store_true', help='verbose mode - serial output print to '
                                                                            'stdout', dest='verbose', required=False)
            parse.add_argument('-o', '--output', nargs='?', type=str, help='raw serial port output', dest='output_path',
                               default=None, required=False)
            parse.add_argument('-sp', '--serialport', nargs='+', type=str, help='serial port to open',
                               dest='monitorPort',
                               default=None, required=False)
            parse.add_argument('-sr', '--serialrate', nargs='+', type=str, help='serial baudrate port to open',
                               dest='monitorSpeed', default=None, required=False)

            parse.add_argument('-g', '--gui', action='store_true', help='gui mode', dest='gui', required=False)

            parse.add_argument('-dp', '--disable-plugin', nargs='+', type=str, help='disable plugin with list of '
                                                                                    'plugin to disable',
                               dest='disable_plugin', default=None, required=False)
            parse.add_argument('-ep', '--enable-plugin', nargs='+', type=str, help='enable plugin with list of plugin '
                                                                                   'to enable - all other plugins '
                                                                                   'loaded are disabled',
                               dest='enable_plugin', default=None, required=False)

            args = parse.parse_args()
            if args:
                self.set_verbose(args.verbose)
                if args.output_path:
                    self.set_raw_output_path(args.output_path)

                self.monitorPort = args.monitorPort
                self.monitorSpeed = args.monitorSpeed
                self.gui = args.gui
                self.disable_plugin_list = args.disable_plugin
                self.enable_plugin_list = args.enable_plugin
        except argparse.ArgumentError as e:
            print("Parsing values from cli entrypoint failed... abort")
            print(e)
            exit(-1)
