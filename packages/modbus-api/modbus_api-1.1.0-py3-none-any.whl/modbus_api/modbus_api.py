"""封装Modbus读写方法."""
import logging
import struct
from typing import Union, List

from modbus_tk import modbus_tcp
from modbus_tk import defines as cst


from modbus_api.exception import PLCConnectError, PLCReadError, PLCWriteError


class ModbusApi:
    """ModbusApi class."""

    def __init__(self, plc_ip, port=502):
        self.plc_ip = plc_ip
        self.port = port
        self.logger = logging.getLogger(__name__)

        self.client = modbus_tcp.TcpMaster(host=plc_ip, port=port)
        self._connection_state = False

    @property
    def ip(self):
        """获取plc ip."""
        return self.plc_ip

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
                self.client.open()
            self._connection_state = True
            return True
        except Exception as e:
            self.logger.error("Error connecting to PLC: %s", e)
            raise PLCConnectError(f"Error connecting to PLC: {e}") from e

    def communication_close(self):
        """Close the connection to the PLC."""
        if self._connection_state:
            self.client.close()
            self._connection_state = False
            self.logger.info("Closed connection to PLC")

    def read_bool(self, address: int, bit_index: int, save_log=True) -> bool:
        """Read a specific boolean bit from the PLC at a given address.

        Args:
            address: The address to read from.
            bit_index: The index of the bit within the address to read.
            save_log: Whether to save the log or not.

        Returns:
            bool: The value of the specified bit.
        """
        try:
            registers = self.client.execute(
                slave=1, function_code=cst.READ_HOLDING_REGISTERS, starting_address=address, quantity_of_x=1
            )
            value = (registers[0] & (1 << bit_index)) != 0
            if save_log:
                self.logger.info("Read boolean value %s from address %d, bit index %d", value, address, bit_index)
            return value
        except Exception as e:
            self.logger.error("读取保持寄存器时出错: %s", str(e))
            raise PLCReadError(f"读取保持寄存器时出错: {e}") from e

    def read_int(self, address: int, count: int = 1, save_log=True) -> int:
        """Read an integer value from the PLC.
        Args:
            address: The address to read from.
            count: The number of values to read.
            save_log: Whether to save the log or not.

        Returns:
            int: The value read from the PLC.
        """
        try:
            registers = self.client.execute(
                slave=1, function_code=cst.READ_HOLDING_REGISTERS, starting_address=address, quantity_of_x=count
            )
            if count == 1:
                int_value = registers[0]
            else:
                int_value = registers
            if save_log:
                self.logger.info("Read int value from %s to %s: %s", address, address + count - 1, int_value)
            return int_value
        except Exception as e:
            self.logger.error("读取输入寄存器时出错: %s", str(e))
            raise PLCReadError(f"读取输入寄存器时出错: {e}") from e

    def read_str(self, address: int, count: int, save_log=True) -> str:
        """Read a string value from the PLC.

        Args:
            address: The address to read from.
            count: The number of values to read.
            save_log: Whether to save the log or not.

        Returns:
            str: The value read from the PLC.
        """
        try:
            results = self.client.execute(1, cst.READ_HOLDING_REGISTERS, address, quantity_of_x=count)
            byte_data = b"".join(struct.pack(">H", result) for result in results)
            value_str = byte_data.decode("UTF-8").strip("\x00")
            if save_log:
                self.logger.info("Read string value from %s to %s: %s", address, address + count - 1, value_str)
            return value_str
        except Exception as e:
            self.logger.error("读取输入寄存器时出错: %s", str(e))
            raise PLCReadError(f"读取输入寄存器时出错: {e}") from e

    def write_bool(self, address: int, bit_index: int, value: bool, save_log=True) -> None:
        """Write a specific boolean bit to the PLC at a given address.

        Args:
            address: The address to write to.
            bit_index: The index of the bit within the address to write.
            value: The boolean value to write.
            save_log: Whether to save the log or not.
        """
        try:
            coils = self.client.execute(
                slave=1, function_code=cst.READ_HOLDING_REGISTERS, starting_address=address, quantity_of_x=1
            )
            current_value = coils[0]
            if value:
                new_value = current_value | (1 << bit_index)
            else:
                new_value = current_value & ~(1 << bit_index)
            self.client.execute(
                slave=1, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=address, output_value=new_value)
            if save_log:
                self.logger.info("Wrote boolean value %s to address %d, bit index %d", value, address, bit_index)
        except Exception as e:
            self.logger.error("写入保持寄存器时出错: %s", str(e))
            raise PLCWriteError(f"写入保持寄存器时出错: {e}") from e

    def write_int(self, address: int, value: Union[int, List[int]], save_log=True) -> None:
        """Write an integer value to the PLC.

        Args:
            address: The address to write to.
            value: The integer value or list of integer values to write.
            save_log: Whether to save the log or not.
        """
        if isinstance(value, int):
            value = [value]
        try:
            self.client.execute(
                slave=1, function_code=cst.WRITE_MULTIPLE_REGISTERS, starting_address=address, output_value=value
            )
            if save_log:
                self.logger.info("Wrote %s to address %d", value, address)
        except Exception as e:
            self.logger.error("写入输入寄存器时出错: %s", str(e))
            raise PLCWriteError(f"写入输入寄存器时出错: {e}") from e

    # pylint: disable=R0913, R0917
    def execute_read(self, data_type, address, size=1, bit_index=0, save_log=True) -> Union[int, str, bool]:
        """Execute read function based on data_type.

        Args:
            data_type: The data type to read.
            address: The address to read from.
            size: The number of values to read.
            bit_index: The index of the bit within the address to read.
            save_log: Whether to save the log or not.

        Returns:
            Union[int, str, bool]: The value read from the PLC.
        """
        if data_type == "bool":
            return self.read_bool(address, bit_index, save_log)
        if data_type == "int":
            return self.read_int(address, size, save_log)
        if data_type == "str":
            return self.read_str(address, size, save_log)
        raise ValueError(f"Invalid data type: {data_type}")

    # pylint: disable=R0913, R0917
    def execute_write(self, data_type, address, value, bit_index=0, save_log=True):
        """Execute write function based on data_type.

        Args:
            data_type: The data type to write.
            address: The address to write to.
            value: The value to write.
            bit_index: The index of the bit within the address to write.
            save_log: Whether to save the log or not.
        """
        if data_type == "bool":
            self.write_bool(address, bit_index, value, save_log)
        elif data_type == "int":
            self.write_int(address, value, save_log)
        elif data_type == "str":
            pass
        else:
            raise ValueError(f"Invalid data type: {data_type}")
