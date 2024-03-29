#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010-2016 Eurotechnia (support@webcampak.com)
# This file is part of the Webcampak project.
# Webcampak is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# Webcampak is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Webcampak.
# If not, see http://www.gnu.org/licenses/

from __future__ import absolute_import
from builtins import object
import os, uuid
import shutil

from .wpakConfigObj import Config
from .wpakFileUtils import fileUtils
from .wpakXferUtils import xferUtils
from .wpakFTPTransfer import FTPTransfer


# This class is used to remove all xfer jobs in queue


class xferClear(object):
    def __init__(self, log, appConfig, config_dir, threadUUID):
        self.log = log
        self.appConfig = appConfig
        self.config_dir = config_dir
        self.configPaths = Config(self.log, self.config_dir + "param_paths.yml")
        self.xferUtils = xferUtils(self.log, self.config_dir)
        self.argThreadUUID = threadUUID

        self.dirXferThreads = fileUtils.CheckDir(
            self.configPaths.getConfig("parameters")["dir_xfer"] + "threads/"
        )
        self.dirXferQueue = fileUtils.CheckDir(
            self.configPaths.getConfig("parameters")["dir_xfer"] + "queued/"
        )
        self.dirXferFailed = fileUtils.CheckDir(
            self.configPaths.getConfig("parameters")["dir_xfer"] + "failed/"
        )
        self.dirEtc = self.configPaths.getConfig("parameters")["dir_etc"]
        self.dirConfig = self.configPaths.getConfig("parameters")["dir_config"]
        self.dirSources = self.configPaths.getConfig("parameters")["dir_sources"]
        self.dirLocale = self.configPaths.getConfig("parameters")["dir_locale"]
        self.dirLogs = self.configPaths.getConfig("parameters")["dir_logs"]
        self.dirLocale = self.configPaths.getConfig("parameters")["dir_locale"]
        self.dirLocaleMessage = self.configPaths.getConfig("parameters")[
            "dir_locale_message"
        ]

        self.setupLog()

        self.configGeneral = Config(self.log, self.dirConfig + "config-general.cfg")

        self.maxFilesPerThread = 10

    def setupLog(self):
        """Setup logging to file"""
        xferLogs = self.dirLogs + "xfer/"
        if not os.path.exists(xferLogs):
            os.makedirs(xferLogs)
        logFilename = xferLogs + "clear.log"
        self.appConfig.set(self.log._meta.config_section, "file", logFilename)
        self.appConfig.set(self.log._meta.config_section, "rotate", True)
        self.appConfig.set(self.log._meta.config_section, "max_bytes", 512000)
        self.appConfig.set(self.log._meta.config_section, "max_files", 10)
        self.log._setup_file_log()

    # Clear all files from the transfer queue
    # Function: run
    # Description: Remove all files from the transfer queue
    # Return: Nothing
    def run(self):
        # Load the config containing all paths and the general config file
        self.log.info("xferClear.run(): Job Running XFer Clear")
        self.log.info(
            "xferClear.run(): Removing queued jobs: %(dirXferQueue)s"
            % {"dirXferQueue": self.dirXferQueue}
        )
        shutil.rmtree(self.dirXferQueue)
        self.log.info(
            "xferClear.run(): Removing threads and jobs: %(dirXferThreads)s"
            % {"dirXferThreads": self.dirXferThreads}
        )
        shutil.rmtree(self.dirXferThreads)
        self.log.info(
            "xferClear.run(): Removing failed jobs: %(dirXferFailed)s"
            % {"dirXferFailed": self.dirXferFailed}
        )
        shutil.rmtree(self.dirXferFailed)
        os.makedirs(self.dirXferQueue)
        os.makedirs(self.dirXferThreads)
        os.makedirs(self.dirXferFailed)
