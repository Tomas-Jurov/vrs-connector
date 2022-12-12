import serial
import time
import serial.tools.list_ports as st


class Joystick():
    _ports = st.comports()

    @staticmethod
    def _get_port(_ports:list) -> str:
        for port, desc, hwid in sorted(_ports):
            _port = port
        return _port  



    def __init__(self):
        self._port = Joystick._get_port(Joystick._ports)
        self._serial = serial.Serial(self._port, 234000, timeout=0.2)
        self._cm = 0
        self._lr = 0
        self._fb = 0
        self._ud = 0
        self._yv = 0

    def flush_buffers(self):
        time.sleep(2)
        self._serial.flushInput()
        self._serial.flushOutput()
        time.sleep(0.5)

    def _get_serial_read(self) -> int:
        return int.from_bytes(self._serial.read(1),'big',signed='True')

    def _get_read_tuple(self):
        self._lr = self._get_serial_read()
        self._fb = self._get_serial_read()
        self._ud = self._get_serial_read()
        self._yv = self._get_serial_read()

    @property
    def tuple(self):
        _start_bit = self._serial.read(1)
        if(_start_bit==b'\x6E'):
            self._cm=110
        elif(_start_bit==b'\x70'):
            self._cm=112
        elif(_start_bit==b'\x6F'):
            self._cm=111
        if(self._cm!=0):
            self._get_read_tuple()
        return((self._cm,self._lr,self._fb,self._ud,self._yv))


