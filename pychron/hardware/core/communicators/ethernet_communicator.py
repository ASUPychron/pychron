# ===============================================================================
# Copyright 2011 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= standard library imports ========================
import socket
import time

from six.moves import range

# ============= enthought library imports =======================
from traits.api import Float

# ============= local library imports  ==========================
from pychron.globals import globalv
from pychron.hardware.core.checksum_helper import computeCRC
from pychron.hardware.core.communicators.communicator import (
    Communicator,
    process_response,
)
from pychron.regex import IPREGEX


class MessageFrame(object):
    def __init__(self, message_len=False, nmessage_len=4, checksum=False, nchecksum=4):
        self.nchecksum = nchecksum
        self.checksum = checksum
        self.nmessage_len = nmessage_len
        self.message_len = message_len

    def set_str(self, s):
        """
        L4,-,C4
        """
        if s:
            args = s.split(",")
            if len(args) == 3:
                ml = args[0]
                cs = args[2]
                self.nmessage_len = int(ml[1:])
                self.nchecksum = int(cs[1:])
                self.checksum = True
                self.message_len = True


class Handler(object):
    sock = None
    datasize = 2 ** 12
    address = None
    message_frame = None

    def set_frame(self, f):
        self.message_frame = MessageFrame()
        if f:
            self.message_frame.set_str(f)

    def get_packet(self):
        raise NotImplementedError

    def send_packet(self, p):
        raise NotImplementedError

    def end(self):
        pass

    # private
    def _recvall(self, recv, datasize=None, frame=None):
        """
        recv: callable that accepts 1 argument (datasize). should return a str
        """
        # ss = []
        sum = 0

        # disable message len checking
        # msg_len = 1
        # if self.use_message_len_checking:
        # msg_len = 0

        msg_len = 1
        nm = -1

        if frame is None:
            frame = self.message_frame

        if frame.message_len:
            msg_len = 0
            nm = frame.nmessage_len

        if datasize is None:
            datasize = self.datasize

        data = b""
        while 1:
            s = recv(datasize)

            if not s:
                break

            if not msg_len:
                msg_len = int(s[:nm], 16)

            sum += len(s)
            data += s
            if sum >= msg_len:
                break

        if frame.message_len:
            # trim off header
            data = data[nm:]

        if frame.checksum:
            nc = frame.nchecksum
            checksum = data[-nc:]
            data = data[:-nc]
            comp = computeCRC(data)
            if comp != checksum:
                print("checksum fail computed={}, expected={}".format(comp, checksum))
                return

        return data.decode("utf-8")


class TCPHandler(Handler):
    def open_socket(self, addr, timeout=1.0, **kw):
        self.address = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if globalv.communication_simulation:
            timeout = 0.01

        self.sock.settimeout(timeout)
        self.sock.connect(addr)

    def get_packet(self, datasize=None, message_frame=None):
        return self._recvall(self.sock.recv, datasize=datasize, frame=message_frame)

    def send_packet(self, p):
        self.sock.send(p.encode("utf-8"))

    def end(self):
        self.sock.close()


class UDPHandler(Handler):
    def open_socket(self, addr, timeout=1.0, bind=False):
        self.address = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if globalv.communication_simulation:
            timeout = 0.01
        self.sock.settimeout(timeout)

        try:
            if bind:
                addr = "", addr[1]
                self.sock.bind(addr)
        except BaseException:
            print("failed binding", addr)

    def get_packet(self, **kw):
        def recv(ds):
            rx, _ = self.sock.recvfrom(ds)
            return rx

        return self._recvall(recv)

    def send_packet(self, p):
        self.sock.sendto(p.encode("utf-8"), self.address)


class EthernetCommunicator(Communicator):
    """
    Communicator of UDP or TCP.
    """

    host = None
    port = None
    read_port = None
    handler = None
    kind = "UDP"
    test_cmd = None
    use_end = False
    verbose = False
    error_mode = False
    message_frame = ""
    timeout = Float(1.0)

    default_timeout = 3

    _comms_report_attrs = ("host", "port", "read_port", "kind", "timeout")

    @property
    def address(self):
        return "{}://{}:{}".format(self.kind, self.host, self.port)

    def load(self, config, path):
        """ """
        super(EthernetCommunicator, self).load(config, path)

        self.host = self.config_get(config, "Communications", "host")
        if self.host != "localhost" and not IPREGEX.match(self.host):
            result = socket.getaddrinfo(self.host, 0, 0, 0, 0)
            if result:
                for family, kind, a, b, host in result:
                    if family == socket.AF_INET and kind == socket.SOCK_STREAM:
                        self.host = host[0]

        # self.host = 'localhost'
        self.port = self.config_get(config, "Communications", "port", cast="int")
        self.read_port = self.config_get(
            config, "Communications", "read_port", cast="int", optional=True
        )
        self.timeout = self.config_get(
            config,
            "Communications",
            "timeout",
            cast="float",
            optional=True,
            default=1.0,
        )
        self.kind = self.config_get(config, "Communications", "kind", optional=True)
        self.test_cmd = self.config_get(
            config, "Communications", "test_cmd", optional=True, default=""
        )
        self.use_end = self.config_get(
            config,
            "Communications",
            "use_end",
            cast="boolean",
            optional=True,
            default=False,
        )
        self.message_frame = self.config_get(
            config, "Communications", "message_frame", optional=True, default=""
        )
        self.default_timeout = self.config_get(
            config,
            "Communications",
            "default_timeout",
            cast="int",
            optional=True,
            default=3,
        )

        if self.kind is None:
            self.kind = "UDP"

        return True

    def open(self, *args, **kw):

        for k in ("host", "port", "message_frame", "kind"):
            if k in kw:
                setattr(self, k, kw[k])

        return self.test_connection()

    def test_connection(self):
        self.simulation = False

        with self._lock:
            handler = self.get_handler()

        # send a test command so see if wer have connection
        cmd = self.test_cmd

        if cmd:
            self.debug("sending test command {}".format(cmd))
            r = self.ask(cmd)
            if r is None:
                self.simulation = True

                # if handler:
                #     if handler.send_packet(cmd):
                #         r = handler.get_packet(cmd)
                #         if r is None:
                #             self.simulation = True
                #     else:
                #         self.simulation = True
                # else:
                #     self.simulation = True
        ret = not self.simulation and handler is not None
        return ret

    def get_read_handler(self, handler, **kw):

        if self.read_port:
            handler = self.get_handler(
                addrs=(self.host, self.read_port), bind=True, **kw
            )

        return handler

    def get_handler(self, addrs=None, timeout=None, bind=False):
        if timeout is None:
            timeout = self.timeout
        if addrs is None:
            addrs = (self.host, self.port)

        try:

            h = self.handler
            if h is None or h.address != addrs:
                if self.kind.lower() == "udp":
                    h = UDPHandler()
                else:
                    h = TCPHandler()

                # self.debug('get handler cmd={}, {},{} {}'.format(cmd.strip() if cmd is not None else '---', self.host,
                #                                                  self.port, timeout))
                h.open_socket(addrs, timeout=timeout or 1, bind=bind)
                h.set_frame(self.message_frame)
                self.handler = h
            return h
        except socket.error as e:
            print("ewafs", e, self.host, self.port)
            self.debug(
                "Get Handler {}. timeout={}. comms simulation={}".format(
                    str(e), timeout, globalv.communication_simulation
                )
            )
            self.error_mode = True
            self.handler = None

    def ask(
        self,
        cmd,
        retries=3,
        verbose=True,
        quiet=False,
        info=None,
        timeout=None,
        message_frame=None,
        delay=None,
        use_error_mode=True,
        *args,
        **kw
    ):
        """
        @param cmd: ASCII text to send
        @param retries: number of retries if command fails
        @param verbose: add to log
        @param quiet: if true do not log the response
        @param info: str to add to response
        @param timeout: timeout in seconds
        @param message_frame: MessageFrame object
        @param delay: delay in seconds to wait before a `cmd` is sent

        """

        if self.simulation:
            if verbose:
                self.info("no handle    {}".format(cmd.strip()))
            return

        cmd = "{}{}".format(cmd, self.write_terminator)

        r = None
        with self._lock:
            if use_error_mode and self.error_mode:
                retries = 2

            if timeout is None:
                timeout = self.default_timeout

            re = "ERROR: Connection refused: {}, timeout={}".format(
                self.address, timeout
            )
            for i in range(retries):
                r = self._ask(
                    cmd,
                    timeout=timeout,
                    message_frame=message_frame,
                    delay=delay,
                    use_error_mode=use_error_mode,
                )
                if r is not None:
                    break
                else:
                    time.sleep(0.025)
                    self.debug("doing retry {}".format(i))
                    # else:
                    #     self._reset_connection()

            if r is not None:
                re = process_response(r)
            # else:
            #     self.error_mode = True

            if self.use_end:
                # self.debug('ending connection. Handler: {}, cmd={}'.format(self.handler, cmd))
                if self.handler:
                    self.handler.end()
                self._reset_connection()

            if verbose or (self.verbose and not quiet):
                self.log_response(cmd, re, info)

        return r

    def reset(self):
        if self.handler:
            self.handler.end()
        self._reset_connection()

    def read(self, datasize=None, *args, **kw):
        with self._lock:
            handler = self.get_handler()
            if handler:
                return handler.get_packet(datasize=datasize)

    def tell(self, cmd, verbose=True, quiet=False, info=None):
        with self._lock:
            handler = self.get_handler()
            if handler:
                try:
                    cmd = "{}{}".format(cmd, self.write_terminator)
                    handler.send_packet(cmd)
                    if verbose or self.verbose and not quiet:
                        self.log_tell(cmd, info)
                except socket.error as e:
                    self.warning("tell. send packet. error: {}".format(e))
                    self.error_mode = True

    # private
    def _reset_connection(self):
        self.handler = None
        self.error_mode = False

    def _ask(
        self, cmd, timeout=None, message_frame=None, delay=None, use_error_mode=True
    ):
        if self.error_mode:
            self.handler = None
            if use_error_mode:
                timeout = 0.25

        if timeout is None:
            timeout = self.default_timeout

        self.error_mode = False

        handler = self.get_handler(timeout=timeout)
        if not handler:
            return

        try:
            handler.send_packet(cmd)

            if delay:
                time.sleep(delay)

            handler = self.get_read_handler(handler, timeout=timeout)
            try:
                return handler.get_packet(message_frame=message_frame)
            except socket.error as e:
                self.debug_exception()
                self.warning(
                    "ask. get packet. error: {} address: {}".format(e, handler.address)
                )
                self.error_mode = True
        except socket.error as e:
            self.warning(
                "ask. send packet. error: {} address: {}".format(e, handler.address)
            )
            self.error_mode = True


# ============= EOF ====================================
