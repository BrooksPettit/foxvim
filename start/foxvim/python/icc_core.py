
"""
File: ICCPY.py
Author: Brooks Pettit
Date: 01/24/2024
Description: Contains class interface from python to the integrated control configurator.
"""

import logging
import subprocess
import os
from enum import Enum
from functools import wraps
import dataclasses

API_PATH = r"D:\opt\fox\ciocfg\api"
ICCDRVR_TASK = "iccdrvr.tsk.exe"
ICCDRVR_EXE = os.path.join(API_PATH, ICCDRVR_TASK)

LOG_TOKENS = ("ECHO", "WARN", "FLSH", "FAIL", "DONE",)
SECURITY_LEVELS =("READ", "CHKPT", "UPLOAD", "MODIFY", "ALL",)

logging.getLogger("ICCPY").addHandler(logging.NullHandler())

class rtnCodes(Enum):
    """Enums representing manner of handling child process errors"""
    DONE = "DONE"
    FAIL = "FAIL"
    FLSH = 2


class SecurityLevels(Enum):
    """Enums representing ICC access levels
    
    READ -- Will only allow 'read-only' operations, e.g. LIST, GETDEF, etc
    CHECKPOINT -- Read, plus CHECKPOINT operation
    UPLOAD -- CHECKPOINT, plus UPLOAD operation
    MODITY -- UPLOAD, plus MODIFY operation
    ALL -- All operations allowed, including deleting compounds and blocks, and INITIALIZE a station
    """

    READ = "READ"
    CHECKPOINT = "CHKPT"
    UPLOAD = "UPLOAD"
    MODIFY = "MODIFY"
    ALL = "ALL"

@dataclasses.dataclass
class ICCResult:
    stdout: 'list[str]' = dataclasses.field(default_factory=list)
    stderr:'list[str]' = dataclasses.field(default_factory=list)
    returnMessage: str = ""
    returnCode: int = 1


class ICCDriverTask():
     
    __openSessions: int = 0

    def __init__(self, saveOutput = False):
        self.__session: subprocess.Popen = ICCDriverTask.__getSession()
        self.__currentStation: str = None
        self.__saveOutput = saveOutput
        self.saveFile: str = None
        #self.cps = self.listCPs()
        #self.hostedCPs = self.listHostedCPs()

    def __enter__(self):
        """Setup ICCDriverTask to be used as a context manager to prevent zombie processes"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close and Exit child iccdrvr.tsk."""
        self.close()
        self.exit()

    @staticmethod
    def __getSession() -> subprocess.Popen:
        """Run iccdrvr.tsk.exe in an interactive session.
        
        Setup pipe for STDIN for sending commands.
        Implementations must await terminal tokens in output: DONE, FAIL, FLSH when attempting to read from process.
        STDERR is redirected to STDOUT. Had issues reading from STDERR when lines were sitting on STDOUT.
        
        Warning: If read is attempted when there is nothing in STDOUT, the program will deadlock! Do not pass flags
        to supress messages.
        """
        ICCDriverTask.__openSessions += 1
        CREATE_NO_WINDOW = 0x8000000
        return  subprocess.Popen([ICCDRVR_EXE],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 creationflags=CREATE_NO_WINDOW)

    def getSessionPid(self):
        return self.__session.pid

    
    def __stdinSend(self, args: 'list[str]'):
        """Send single line command to iccdrvr.tsk STDIN and flush buffer.

        Private method to deal directly with iccdrvr.tsk at a low level.
        Arguments:
        args -- list of argument strings, e.g. ["OPEN", "CPNAME", "READ", "usrtxt"]
        """

        cmdStr = " ".join(args) + "\n"
        cmdBytes = cmdStr.encode("utf-8")
        self.__session.stdin.write(cmdBytes)
        self.__session.stdin.flush()

    def __stdoutRead(self):
        """Get lines from iccdrvr.tsk STDOUT/STDERR until terminal token found.

        Options:
        Terminal Tokens: ("DONE", "FAIL", "FLSH") are found at the beginning of a line.
        Make sure not to supress these messages with a flag when invoking the iccdrvr.tsk .



        Warning: This method will block waiting for STDOUT if terminal token is not found.
        """

        TERMINAL_TOKENS = (b"FLSH", b"FAIL", b"DONE",)

        stdoutLines = []
        while True:
            lineBytes = self.__session.stdout.readline()
            lineStr = lineBytes.decode("utf-8").strip()
            stdoutLines.append(lineStr)

            if lineBytes[:4] in TERMINAL_TOKENS:
                break
            elif lineBytes == b"":
                #empty bytestring means process is not running
                raise ChildProcessError("ICC Driver Task not running")

        if self.__saveOutput: #conditional write to file for building ICC simulator
            with open(self.saveFile, "a") as file:
                file.write("\n")
                output = "\n".join(stdoutLines)
                file.write(output)

        return stdoutLines

    def __writeReadCycle(self, cmdList: 'list[str]') -> ICCResult:
        """Send a command list to iccdrvr.tsk, return parsed result."""

        self.__stdinSend(cmdList) #communicate to ICCDRVR
        stdoutLines = self.__stdoutRead()
        stderrLines = []
        stdoutLinesNew = []
        for line in stdoutLines: #parse STDIO streams to lists
            if line[:4] in LOG_TOKENS:
                stderrLines.append(line)
            else:
                stdoutLinesNew.append(line)

        #check return state from iccdrvr
        rtnMessage: str = stderrLines[-1]
        rtnToken: str = rtnMessage[:4]
        rtnCode: int = 0
        if rtnToken in ("FAIL", "FLSH"):
            rtnCode = 1
        
        return ICCResult(stdoutLinesNew, stderrLines, rtnMessage, rtnCode)


    def open(self, station: str, sec_level: str = "READ", user_id_string: str = "iccpy") -> ICCResult:
        """Open interactive session with passed station.
        
        Arguments:
        station -- Must be a valid letterbug
        sec_level -- Security level to determine allowable actions.
        user_id_string -- Required by iccdrvr.tsk, which logs this session with System Manager.
        """

        cmd = ["OPEN", station, sec_level, user_id_string]
        res = self.__writeReadCycle(cmd)
        if res.returnCode == 0:
            self.__currentStation = station
        return res

    def override(self, cpName: str, user_id_string: str = "iccpy") -> ICCResult:
        """Unlocks the checkpoint file for the specified CP or volume
        
        cpName -- CP leterbug or library volume to unlock
        user_id_string -- For logging to system manager. Has a 256 char max length.
        """
        cmd = ["OVERRIDE", cpName, user_id_string]
        return self.__writeReadCycle(cmd)

    def initialize(self, cpName: str = "") -> ICCResult:
        """Initializes the CP or database.
        
        cpName -- Optional argument for CP letterbug or volume to initialize.
                  Required if no session is in progress, invalid if session is in progress.

        DANGER: This command *WILL* delete your database if called.
        """
        raise NotImplementedError("Don't initialize stff till authentifiaction added.")
        # if cpName:
        #     return ["INITIALIZE", cpName]
        # else:
        #     return ["INITIALIZE"]
    
    def get(self, cmpBlkStr: str, set: str, blktype: str = "", subsetList = []) -> ICCResult:
        """List parameters for an existing compound[:block]
        
        cmpBlockStr -- Name of compound and/or block for which parameters are desired.
                       Name format is like "COMPOUND:BLOCK"
                       "?" matches any char, and "*" matches any sequence of chars.
                       Examples:
                           "CPD:" - Compound params for "CPD"
                           "CPD:*" - Block params for all blocks in "CPD"
                           "CPD:BLK" - Block params for "CPD:BLK"
        set -- Specify which parameters are desired.
               {"all" | "std" | "subset"}
               "all" - Returns all parameters.
               "std" - Returns the standard set of parameters.
               "subset" - Returns a subset of parameters. Desired parameters must be passed in subsetList.
        """

        cmd = ["GET", cmpBlkStr, set]
        if set == "subset":
            cmd[-1] += "\n" #iccdrvr requires subset at new lines
            lines = []
            for param in subsetList:
                lines.append(param + "\n")
            lines.append("END")
            cmd.extend(lines)

        return self.__writeReadCycle(cmd)


    def getOrder(self, compound: str = "") -> ICCResult:
        """List compounds of a CP or blocks of a compound in their processing order. Must be in a session with a CP or volume.
        
        compound -- Optional argument to specify compound for which to list block. Otherwise list compounds.
        """

        cmd = []
        if compound:
            cmd = ["GETORDER", compound]
        else:
            cmd = ["GETORDER"]
        return self.__writeReadCycle(cmd)

    def getSeq(self, cmpBlkStr: str, basePathName: str) -> ICCResult:
        """List sequence code or return sequence code files for specified block.
        
        cmpBlkStr -- Name of CMP:BLK for which to obtain sequence code.
        basePathName -- Directory and base filename for returned files.

        Non-SFC sequence block will return .s, .i, and .r files.
        SFC blocks will return .a, .b, .f, .g, .h, .i, .k and .r files.

        Example: D:/path/filename => D:/path/filename.s , etc.
        """

        #TODO - set path environment variable or something for default basePathName
        #possibly that should be in the calling class?

        cmd = ["GETSEQ", cmpBlkStr, basePathName]
        return self.__writeReadCycle(cmd)

    def getDef(self, type: str) -> ICCResult:
        """List parameters, types, and default values for the specified block type.
        
        type -- Can be CMPND for compound, otherwise is a block type, e.g. PIDA.
        """

        cmd = ["GETDEF", type]
        return self.__writeReadCycle(cmd)




    def list(self, switch: str) -> ICCResult:
        cmd = ["LIST", switch]
        return self.__writeReadCycle(cmd)

    def upload(self, cmpBlkStr: str = "") -> ICCResult:
        """Uploads settable parameters from a potion of the database to the ICC workfile. Requires and open session with a station.
        
        cmpBlkStr -- Optional argument [CMP | CMP:* | CMP:BLK]
                     Without argument, all compounds and blocks in CP will be uploaded.
                     With argument, matched compound and block parameters will be uploaded
        """

        cmd = []
        if cmpBlkStr:
            cmd = ["UPLOAD", cmpBlkStr]
        else:
            cmd = ["UPLOAD"]
        return self.__writeReadCycle(cmd)

    def checkpoint(self, delay: int = None) -> ICCResult:
        """Performs checkpoint operation on CP open in session. Writes workfile contents to checkpoint file.
        
        delay -- specifies delay to wait for checkpoint return
                 0 - No delay, return immediately
                 >0 - delay for specified number of seconds
                 <0 - default delay: 240 seconds
        Note: I think delay doesn't work, and the call is actually synchronous anyway. See discussion here:
        https://www.freelists.org/post/foxboro/iccdrvrtskexe-CHECKPOINT-call
        """

        if not delay:
            return ["CHECKPOINT"]
        else:
            return ["CHECKPOINT", delay]

    def save(self, cmpStr: str, path: str, saveName: str) -> ICCResult:
        """Save specified compound and its blocks to the specified directory.
        
        cmpStr -- Name of CMP to save.
        path -- Location to hold compound subdirectory.
        saveName -- Name for compound subdirectory that will be created.
        """

        cmd = [cmpStr, path, saveName]
        return self.__writeReadCycle(cmd)
    
    def timeout(self, value: int) -> ICCResult:
        """Signal the iccdrvr.tsk to timout after waiting for input a specified number of seconds.
        
        value -- >0 - Seconds for the timeout.
                  0 - No timeout.
                 -1 - Timeout disabled. Driver never waits for input (e.g. IO from file instead.)

        """

        cmd = ["TIMEOUT", value]
        return self.__writeReadCycle(cmd)

    def close(self) -> ICCResult:
        """Close open station in iccdrvr session."""

        cmd = ["CLOSE"]
        res = self.__writeReadCycle(cmd)
        if res.returnCode == 0:
            self.__currentStation = None
        return res

    def exit(self) -> ICCResult:
        """Exit instance iccdrvr.tsk session"""

        cmd = ["EXIT"]
        return self.__writeReadCycle(cmd)
