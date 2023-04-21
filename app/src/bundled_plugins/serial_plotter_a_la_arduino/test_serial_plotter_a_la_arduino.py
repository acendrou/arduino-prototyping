import time

import serial_plotter_a_la_arduino


class TestSerialPlotter:
    def __init__(self):
        super().__init__()
        self.test_data: list[list[int]] = [[1, 2, 3], [2, 3, 5], [6, 1, 9]]

    def test_basic_case(self):
        for data in self.test_data:
            serial_plotter_a_la_arduino.show(data)
            time.sleep(1)


if __name__ == '__main__':
    test = TestSerialPlotter()
    test.test_basic_case()
