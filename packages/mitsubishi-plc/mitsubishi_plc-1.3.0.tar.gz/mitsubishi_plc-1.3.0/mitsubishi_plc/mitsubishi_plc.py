"""三菱PLC模块."""
import logging
from typing import Union
from threading import Lock

from HslCommunication import MelsecMcNet

from mitsubishi_plc.exception import PLCConnectError


class MitsubishiPlc:
    """MitsubishiPlc class."""

    def __init__(self, plc_ip, port):
        self.plc_ip = plc_ip
        self.logger = logging.getLogger(__name__)
        self.melsec_net = MelsecMcNet(plc_ip, port)
        self._connection_state = False
        self.lock = Lock()

    @property
    def open_state(self) -> bool:
        """Return the connection state of the PLC.

        Returns:
            bool: True if the connection is open, False otherwise.
        """
        return self._connection_state

    def communication_open(self) -> bool:
        """Open the connection to the PLC.

        Returns:
            bool: True if the connection is open, False otherwise.

        Raises:
            PLCConnectError: If the connection is not open.
        """
        try:
            if not self._connection_state:
                result = self.melsec_net.ConnectServer()
                if result.IsSuccess:
                    self._connection_state = True
                    return True
            return False
        except Exception as e:
            self.logger.error("Error connecting to PLC: %s", e)
            raise PLCConnectError(f"Error connecting to PLC: {e}") from e

    def communication_close(self):
        """Close the connection to the PLC."""
        if self._connection_state:
            self.melsec_net.ConnectClose()
            self._connection_state = False
            self.logger.info("Closed connection to PLC")

    def execute_read(
            self, data_type: str, address: str, size: int = None, save_log: bool = True
    ) -> Union[str, int, float, bool, list]:
        """Execute a read operation on the PLC.

        Args:
            data_type: The data type to read.
            address: The address to read from.
            size: The size of the data to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[str, int, float, bool, list]: The value read from the PLC.
        """
        with self.lock:
            read_func = getattr(self, f"read_{data_type}")
            return read_func(address, size=size, save_log=save_log)

    def read_bool(self, address: str, size: int = None, save_log: bool = True) -> Union[bool, list]:
        """Read a boolean value from the PLC.

        Args:
            address: The address to read from.
            size: The size of the data to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[bool, list]: The value read from the PLC.
        """
        bool_result = self.melsec_net.ReadBool(address, size)
        bool_value = bool_result.Content
        if save_log:
            self.logger.info("Read bool on %s, returned bool value: %s", address, bool_value)
        return bool_value

    def read_int16(self, address: str, size: int = None, save_log: bool = True) -> Union[int, list]:
        """Read an integer value from the PLC.

        Args:
            address: The address to read from.
            size: The size of the data to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[int, list]: The value read from the PLC.
        """
        int_result = self.melsec_net.ReadInt16(address, size)
        int_value = int_result.Content
        if save_log:
            self.logger.info("Read int on %s, returned int value: %s", address, int_value)
        return int_value

    def read_int32(self, address: str, size: int = None, save_log: bool = True) -> Union[int, list]:
        """Read an 4 byte integer value from the PLC.

        Args:
            address: The address to read from.
            size: The size of the data to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[int, list]: The value read from the PLC.
        """
        int_result = self.melsec_net.ReadInt32(address, size)
        int_value = int_result.Content
        if save_log:
            self.logger.info("Read int32 on %s, returned int value: %s", address, int_value)
        return int_value

    def read_float(self, address: str, size: int = None, save_log: bool = True) -> Union[float, list]:
        """Read a float value from the PLC.

        Args:
            address: The address to read from.
            size: The size of the data to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[float, list]: The value read from the PLC.
        """
        float_result = self.melsec_net.ReadFloat(address, size)
        float_value = float_result.Content
        if save_log:
            self.logger.info("Read float on %s, returned float value: %s", address, float_value)
        return float_value

    def read_double(self, address: str, size: int = None, save_log: bool = True) -> Union[float, list]:
        """Read a double value from the PLC.

        Args:
            address: The address to read from.
            size: The size of the data to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[float, list]: The value read from the PLC.
        """
        double_result = self.melsec_net.ReadDouble(address, size)
        double_value = double_result.Content
        if save_log:
            self.logger.info("Read double on %s, returned double value: %s", address, double_value)
        return double_value

    def read_str(self, address: str, size: int, save_log: bool = True) -> Union[str, list]:
        """Read a string value from the PLC.

        Args:
            address: The address to read from.
            size: The size of the string to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[str, list]: The value read from the PLC.
        """
        string_result = self.melsec_net.ReadString(address, size)
        string_value = string_result.Content.strip().replace("\x00", "")
        if save_log:
            self.logger.info("Read string on %s, returned string value: %s", address, string_value)
        return string_value

    def execute_write(
            self, data_type: str, address: str, value: Union[str, int, float, bool], save_log: bool = True
    ) -> bool:
        """Execute a write operation on the PLC.

        Args:
            data_type: The data type to write.
            address: The address to write to.
            value: The value to write.
            save_log: Whether to save the log or not, default save.

        Returns:
            bool: True if the wrote was successful, False otherwise.
        """
        with self.lock:
            write_func = getattr(self, f"write_{data_type}")
            return write_func(address, value, save_log=save_log)

    def write_bool(self, address: str, value: bool, save_log: bool = True) -> bool:
        """Write a boolean value to the PLC.

        Args:
            address: The address to write to.
            value: The value to write.
            save_log: Whether to save the log or not.

        Returns:
            bool: True if the wrote was successful, False otherwise.
        """
        result = self.melsec_net.WriteBool(address, value)
        if save_log:
            self.logger.info("Wrote bool on %s, wrote value: %s", address, value)
        return result.IsSuccess

    def write_int16(self, address: str, value: int, save_log: bool = True) -> bool:
        """Write an integer value to the PLC.

        Args:
            address: The address to write to.
            value: The value to write.
            save_log: Whether to save the log or not.

        Returns:
            int: The number of bytes written.
        """
        result = self.melsec_net.WriteInt16(address, value)
        if save_log:
            self.logger.info("Wrote int on %s, wrote value: %s", address, value)
        return result.IsSuccess

    def write_float(self, address: str, value: float, save_log: bool = True) -> bool:
        """Write a float value to the PLC.

        Args:
            address: The address to write to.
            value: The value to write.
            save_log: Whether to save the log or not.

        Returns:
            int: The number of bytes written.
        """
        result = self.melsec_net.WriteFloat(address, value)
        if save_log:
            self.logger.info("Wrote float on %s, wrote value: %s", address, value)
        return result.IsSuccess

    def write_double(self, address: str, value: float, save_log: bool = True) -> bool:
        """Write a double value to the PLC.

        Args:
            address: The address to write to.
            value: The value to write.
            save_log: Whether to save the log or not.

        Returns:
            int: The number of bytes written.
        """
        result = self.melsec_net.WriteDouble(address, value)
        if save_log:
            self.logger.info("Wrote double on %s, wrote value: %s", address, value)
        return result.IsSuccess

    def write_str(self, address: str, value: str, save_log: bool = True) -> bool:
        """Write a string value to the PLC.

        Args:
            address: The address to write to.
            value: The value to write.
            save_log: Whether to save the log or not.

        Returns:
            int: The number of bytes written.
        """
        result = self.melsec_net.WriteString(address, value)
        if save_log:
            self.logger.info("Wrote string on %s, wrote value: %s", address, value)
        return result.IsSuccess
