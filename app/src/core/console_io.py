import configparser
import datetime
from time import sleep
import serial
import serial.tools.list_ports
import multiprocessing as mp

from core.parse_logic import parse_entrypoint
from core.utils import log, log_error


def main_console_io():
    console = ConsoleIO()
    console.guess_monitor_parameters()
    while True:
        console.open_connection()


class ConsoleIO:
    monitor_port: str = ""
    monitor_speed: str = "2000000"

    is_raw_output_saved: bool = False
    file_output_raw = None
    raw_output_path: str = None

    def __init__(self, monitor_port: str = monitor_port, monitor_speed: str = monitor_speed):
        self.monitor_port = monitor_port
        self.monitor_speed = monitor_speed

    def __int__(self):
        pass

    def guess_monitor_parameters(self):
        # self.set_monitors_parameters_from_board_config()
        self.set_monitor_parameters_auto()

    def set_monitor_parameters_auto(self):
        # automatically find ports opened
        self.monitor_port = self.retrieve_ports_available_machine()

    def set_monitors_parameters_from_board_config(self, config_file_path: str = "../info_board.ini"):
        monitor_params = self.get_board_info_values(config_file_path=config_file_path)
        try:
            self.monitor_speed = monitor_params["monitorSpeed"]
        except KeyError:
            pass
        try:
            self.monitor_port = monitor_params["monitorPort"]
        except KeyError:
            pass

    def set_monitors_parameters(self, monitor_port: str = monitor_port, monitor_speed: str = monitor_speed):
        self.monitor_port = monitor_port
        self.monitor_speed = monitor_speed

    def open_connection(self, lis=None):
        while True:
            try:
                log("Opening port...")
                ser = serial.Serial(port=self.monitor_port, baudrate=int(self.monitor_speed), timeout=10)
                if ser.is_open:
                    log("Port opened")
                else:
                    break
            except serial.SerialException as e:
                log_error("error port opening")
                print(e)
                log("Moniteur serie - erreur ouverture")
                sleep(2)
                break
            else:

                # spawn new process for parsing serial input (from PC's perspective) use a Pipe for inter process
                # communication: we will pass line by line of serial input to the input parser
                # mp.set_start_method('spawn')
                parent_conn = None
                if lis is None:
                    child_conn, parent_conn = mp.Pipe(duplex=False)
                    process_parse_input = mp.Process(target=parse_entrypoint, args=(child_conn,))
                    process_parse_input.start()
                log("input parser started")

                self.mode_options_init()

                while True:
                    # log("Starting receiving input")
                    try:
                        if ser.in_waiting > 0:
                            line = ser.readline().decode('utf-8').rstrip()
                            print(line)
                            # print("blabla")
                            self.mode_serial_line_options(line)
                            if lis is None:
                                parent_conn.send(line)
                            else:
                                lis.call(line)
                    except serial.SerialException as e:
                        log("line error")
                        print(e)
                        ser.close()
                        # process_parse_input.join()
                        break

    # read config file: get current settings for communication with board, info shared by platformio our board's
    # programmer
    @staticmethod
    def get_board_info_values(config_file_path: str = "../info_board.ini") -> dict:
        config = configparser.ConfigParser()
        config.read(config_file_path)
        try:
            monitor_port: str = config['BOARD_INFO']['monitor_port']
        except KeyError:
            monitor_port = ""
        try:
            monitor_speed: str = config['BOARD_INFO']['monitor_speed']
        except KeyError:
            monitor_speed = ""

        if not monitor_port or not monitor_speed:
            log("Error get board info value(s) from config file - platformio shared canal")

        return {"monitorSpeed": monitor_speed, "monitorPort": monitor_port}

    @staticmethod
    def retrieve_ports_available_machine():
        serial_port_list = serial.tools.list_ports.comports()
        monitor_port: serial.Serial.port = ""
        log(serial_port_list)
        # retrieve port available on machine : could override config found in board_info
        for serial_port in serial_port_list:
            log(serial_port.device)
            log(serial_port.vid)
            # log(serial_port.description)
            monitor_port = serial_port.device
            if serial_port.vid == 6790 or serial_port.description == "USB2.0-Serial":
                monitor_port = serial_port.device
                log("Good port")
            else:
                log("Bad port")
                continue
        return monitor_port

    def mode_options_init(self):
        if self.is_raw_output_saved:
            date = datetime.datetime.now().isoformat()
            self.file_output_raw = None
            file_path = self.raw_output_path + date + "_raw_output.txt"
            log(f"Starting logging at: {file_path}")
            self.file_output_raw = open(file_path, "wt")

    def mode_serial_line_options(self, line: str):
        if self.is_raw_output_saved:
            try:
                self.file_output_raw.write(line)
                # log("line written in output file")
                self.file_output_raw.write('\n')
                self.file_output_raw.flush()
            except OSError:
                log("raw output error: line not saved")
