import asyncio
import logging
from curses import ascii

import serial
from serial_asyncio import open_serial_connection

from .errors import ErrorCode
from .messages import ReadRequest, Request, Response, SaveRequest, WriteRequest


class TTM214:
    """
    TTM214 control class
    """

    def __init__(self, address: int, use_bcc: bool = False) -> None:
        self.logger = logging.getLogger(__name__)
        self._address = address
        self._is_open = False
        self._use_bcc = use_bcc

        # Receive event
        self._receive_event: asyncio.Event = asyncio.Event()
        self._response: Response | None = None

    async def open_port(
        self,
        port: str,
        baudrate: int = 9600,
        parity: serial.PARITY_NONE = serial.PARITY_NONE,
        stopbits: serial.STOPBITS_ONE = serial.STOPBITS_TWO,
        bytesize: serial.EIGHTBITS = serial.EIGHTBITS,
    ) -> None:
        """
        Open the serial port for communication with the device.

        Parameters
        ----------
        port : str
            Serial port name (e.g., 'COM1', '/dev/ttyUSB0')
        baudrate : int, optional
            Baud rate for serial communication, by default 9600
        parity : serial.PARITY_NONE, optional
            Parity setting, by default serial.PARITY_NONE
        stopbits : serial.STOPBITS_ONE, optional
            Stop bits setting, by default serial.STOPBITS_TWO
        bytesize : serial.EIGHTBITS, optional
            Byte size setting, by default serial.EIGHTBITS

        Raises
        ------
        Exception
            If opening the port fails
        """
        if self._is_open:
            self.logger.info("Port is already opened")
            return

        try:
            self._reader, self._writer = await open_serial_connection(
                url=port,
                baudrate=baudrate,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize,
            )

            # Polling
            self._poll = asyncio.create_task(self._polling())

        except Exception as e:
            self.logger.error("Failed to open port: %s", port)
            raise e

        self._is_open = True
        self.logger.debug("Connected to serial port (port: %s)", port)

    async def close_port(self) -> None:
        """
        Close the serial port.

        Cancels any ongoing polling tasks and properly closes the serial connection.
        """
        if not self._is_open:
            self.logger.info("Port is already closed")
            return

        # Cancel reception
        if self._poll:
            self._poll.cancel()

        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

        self._is_open = False
        self.logger.info("Closed serial connection")

    async def _polling(self) -> None:
        """
        Internal polling method to continuously read from the serial port.

        Runs in a loop to receive and parse incoming messages from the device.
        Sets the receive event when a complete message is received.
        """

        while self._is_open:
            try:
                # Wait until STX is read
                stx = await self._reader.read(1)
                if stx[0] != ascii.STX:
                    continue

                # Wait until ETX is read
                data = await self._reader.readuntil(bytes([ascii.ETX]))

                if self._use_bcc:
                    # Check BCC
                    bcc = self._calc_bcc(bytes([ascii.STX, *data]))
                    # Wait until BCC is read
                    bcc_data = await self._reader.readexactly(1)
                    if bcc_data != bytes([bcc]):
                        self.logger.warning("BCC mismatch")
                        continue

                self.logger.debug("Received: %s", data)

                # Parse
                self._response = self._parse_bytes_to_response(bytes([ascii.STX, *data]))

                self._receive_event.set()

            except Exception as e:
                self.logger.error("Failed to receive: %s", e)
                continue

    async def _get_response(self, timeout: float = 1) -> Response:
        """
        Wait for and retrieve a response from the device.

        Parameters
        ----------
        timeout : float, optional
            Maximum time to wait for a response in seconds, by default 1

        Returns
        -------
        Response
            The response received from the device

        Raises
        ------
        TimeoutError
            If no response is received within the timeout period
        """

        if not await asyncio.wait_for(self._receive_event.wait(), timeout=timeout):
            raise TimeoutError("Timeout")

        # Wait 2ms
        await asyncio.sleep(2e-3)

        return self._response

    async def _transmit(self, request: Request) -> Response:
        """
        Transmit a request to the device.

        Parameters
        ----------
        request : Request
            The request to send to the device
        """

        if not self._is_open:
            self.logger.warning("Port is not opened")
            return

        # Clear receive event
        self._receive_event.clear()

        # Convert request to bytes
        request_bytes = self._parse_request_to_bytes(request)

        # Calculate BCC
        if self._use_bcc:
            bcc = self._calc_bcc(request_bytes)
            request_bytes = bytes([*request_bytes, bcc])

        self.logger.debug("Transmit: %s", request_bytes)

        # Send request
        self._writer.write(request_bytes)

        # Empty the send buffer
        await self._writer.drain()

    async def query(self, request: Request) -> Response:
        """
        Send a request and wait for a response.

        This is a convenience method that combines transmit() and get_response().

        Parameters
        ----------
        request : Request
            Request to send to the device

        Returns
        -------
        Response
           Response from the device
        """

        await self._transmit(request)

        try:
            return await self._get_response()
        except TimeoutError:
            self.logger.warning("Timeout")
            return Response(error_code=ErrorCode.TIMEOUT)

    def _parse_request_to_bytes(self, request: Request) -> bytes:
        """
        Convert a request object to a byte sequence for transmission.

        Parameters
        ----------
        request : Request
            The request object to convert

        Returns
        -------
        bytes
            The byte sequence representing the request
        """

        ret = bytearray([ascii.STX])
        ret.extend(bytes(f"{self._address:02d}", "ascii"))  # Address

        if isinstance(request, ReadRequest):
            ret.extend(b"R")  # Read
            ret.extend(request.identifier.encode())  # Read target

        elif isinstance(request, WriteRequest):
            ret.extend(b"W")  # Write
            ret.extend(request.identifier.encode())  # Write target
            ret.extend(bytes(f"{request.data:05d}", "ascii"))  # Data

        elif isinstance(request, SaveRequest):
            ret.extend(b"STR")  # Store

        else:
            self.logger.warning("Invalid request")

        ret.extend(bytes([ascii.ETX]))

        return bytes(ret)

    def _parse_bytes_to_response(self, received_bytes: bytes) -> Response:
        """
        Convert a received byte sequence to a Response object.

        Parameters
        ----------
        received_bytes : bytes
            The byte sequence received from the device

        Returns
        -------
        Response
            The parsed response object with appropriate data and error code
        """

        # Check STX
        if received_bytes[0] != ascii.STX:
            self.logger.warning("Invalid start code")

        # Check address
        if int(received_bytes[1:3]) != self._address:
            self.logger.warning("Invalid address: %d", int(received_bytes[1:3]))

        # Check response/negative code

        if received_bytes[3] == ascii.ACK:
            # If end code, it's a response to a write request or save request
            if received_bytes[4] == ascii.ETX:
                return Response(error_code=ErrorCode.NO_ERROR)

            # Response to read request
            else:
                self.logger.debug("Received: %s (len: %d)", received_bytes, len(received_bytes))
                # If data is short
                if len(received_bytes) < 13:
                    self.logger.warning("Invalid response: %s", received_bytes)
                    return Response(error_code=ErrorCode.ILLEGAL_RESPONSE_LENGTH)

                # Identifier
                identifier = received_bytes[4:7]

                # Data
                data = received_bytes[7:12]

                # End code
                if received_bytes[12] != ascii.ETX:
                    self.logger.warning("Invalid response: %s", received_bytes[3:])
                    return Response(error_code=ErrorCode.ILLEGAL_RESPONSE_LENGTH)

                return Response(identifier=identifier, data=data, error_code=ErrorCode.NO_ERROR)

        # If an error occurred
        elif received_bytes[3] == ascii.NAK:
            return Response(error_code=ErrorCode(received_bytes[4]))

        else:
            self.logger.warning("Invalid response: %s", received_bytes[3:])
            return Response(error_code=ErrorCode.ILLEGAL_RESPONSE_CODE)

    def _calc_bcc(self, data: bytes) -> int:
        bcc = 0x00

        for byte in data:
            bcc ^= byte

        return bcc
