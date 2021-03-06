# Host class
# Copyright (c) 2016, Qualcomm Atheros, Inc.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import logging
import subprocess
import threading

logger = logging.getLogger()

def execute_thread(command, reply):
    try:
        status = 0;
        buf = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        status = e.returncode
        buf = e.output

    cmd = ""
    for c in command:
        cmd = cmd + " " + c
    logger.debug("thread cmd: " + cmd)
    logger.debug("thread exit status: " + str(status))
    logger.debug("thread exit buf: " + str(buf))
    reply.append(status)
    reply.append(buf)

class Host():
    def __init__(self, host=None, ifname=None, port=None, name="", user="root"):
        self.host = host
        self.name = name
        self.user = user
        self.ifname = ifname
        self.port = port
        if self.name == "" and host != None:
            self.name = host

    def local_execute(self, command):
        logger.debug("execute: " + command)
        words = command.split()
        cmd = []
        for word in words:
            cmd.append(word)
        try:
            status = 0;
            buf = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            status = e.returncode
            buf = e.output

        logger.debug("status: " + str(status))
        logger.debug("buf: " + str(buf))
        return status, buf

    def execute(self, command):
        if self.host is None:
            return self.local_execute(command)

        cmd = ["ssh", self.user + "@" + self.host, command]
        _cmd = self.name + " execute: "
        for c in cmd:
            _cmd = _cmd + " " + c
        logger.debug(_cmd)
        try:
            status = 0
            buf = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            status = e.returncode
            buf = e.output

        logger.debug(self.name + " status: " + str(status))
        logger.debug(self.name + " buf: " + str(buf))
        return status, buf

    # async execute
    def execute_run(self, command, res):
        if self.host is None:
            cmd = [command]
        else:
            cmd = ["ssh",  self.user + "@" + self.host, command]
        _cmd = self.name + " execute_run: "
        for c in cmd:
            _cmd = _cmd + " " + c
        logger.debug(_cmd)
        t = threading.Thread(target = execute_thread, args=(cmd, res))
        t.start()
        return t

    def wait_execute_complete(self, t, wait=None):
        if wait == None:
            wait_str = "infinite"
        else:
            wait_str = str(wait) + "s"

        logger.debug(self.name + " wait_execute_complete(" + wait_str + "): ")
        if t.isAlive():
            t.join(wait)
