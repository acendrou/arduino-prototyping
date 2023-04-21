import asyncio
import multiprocessing as mp

from core.console_io import ConsoleIO
from core.parse_logic import Parser
from core.plugins.plugins_objects import Plugins
from core.serial_objects.configuration import Configuration


class App:
    lis = None

    console: ConsoleIO = None

    def __init__(self, multiprocessing=False):
        self.multiprocessing = multiprocessing
        self.process_parse_input = None
        self.child_conn = None
        self.parent_conn = None

        self.console = ConsoleIO()
        self.console.guess_monitor_parameters()
        self.lis = Listener(callback=self.call)

        self.config = Configuration()
        self.plugins_loaded = Plugins()
        self.plugins_loaded.load_from_config_files()
        self.parser = Parser(config=self.config, plugins_loaded=self.plugins_loaded)

        self.queue = asyncio.Queue()

    def run(self):
        if self.multiprocessing:
            self.child_conn, self.parent_conn = mp.Pipe(duplex=False)
            self.process_parse_input = mp.Process(target=self.parse_entrypoint_mp, args=(self.child_conn,))
            self.process_parse_input.start()
        self.console.open_connection(self.lis)

    def console_entrypoint(self):
        pass

    def parse_entrypoint_mp(self, serial_input: mp.Pipe):
        while True:
            if serial_input.poll(timeout=1):
                line = serial_input.recv()
                print(line)
                print("Line received")
                self.parser.start_parsing(line)

    def parse_entrypoint_non_mp(self, line: str):
        self.parser.start_parsing(line)

    async def parse_entrypoint_async(self):
        line = await self.queue.get()
        print(line)
        print("Line received")
        self.parser.start_parsing(line)

    async def call_async(self, line):
        self.queue.put_nowait(line)

    def call(self, line: str):
        if self.multiprocessing:
            self.parent_conn.send(line)
        else:
            self.parse_entrypoint_non_mp(line=line)

    def __del__(self):
        pass


class Listener:
    callback = None

    def __init__(self, callback):
        self.callback = callback

    def call(self, arg):
        self.callback(arg)
