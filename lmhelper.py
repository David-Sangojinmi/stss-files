"""
Helper functions for implementing the Little Man Computer.

Copyright (c) 2017, 2018 University of Cambridge
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the University of Cambridge nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Author: Timothy M. Jones
"""

import argparse
import math
import sys
import time


FREQ = 100000
MEMLAT = 0.002
OPCODES = {}
def add_opcode(mnemonic, code, maxop):
    OPCODES[mnemonic] = {'code':code, 'maxop':maxop}
add_opcode('HLT', 0, None)
add_opcode('ADD', 1, 99)
add_opcode('SUB', 2, 99)
add_opcode('STA', 3, 99)
add_opcode('LDA', 5, 99)
add_opcode('BRA', 6, 99)
add_opcode('BRZ', 7, 99)
add_opcode('BRP', 8, 99)
add_opcode('INP', 901, None)
add_opcode('OUT', 902, None)
add_opcode('OTC', 903, None)
add_opcode('DAT', None, 999)


def error(msg, num=1):
    """Exit with a message and error value."""
    print(msg, file=sys.stderr)
    sys.exit(num)


def read_numeric_file(filename):
    """Read an LMC program in numeric format, return as a list of numbers.

    Assumes that there is one number per line, in text.  Exits with an error if
    it cannot parse the file for any reason.
    """
    values = []
    with open(filename) as f:
        lnum = 0
        for line in f:
            try:
                values.append(int(line))
            except:
                error("Error: couldn't parse line " + str(lnum))
            lnum += 1
    return values


def read_mnemonic_file(filename):
    """Read an LMC program in mnemonic format.

    Returns a list of lines broken into tokens along with their line number, so
    each entry is a tuple (list of tokens, line number)."""
    program = []
    with open(filename) as f:
        lnum = 1
        for line in f:
            program.append((line.split(), lnum))
            lnum += 1
    return program


def filter_program(program):
    """Remove blank lines and comments from the program."""
    filtered = []
    for line in program:
        try:
            fline = []
            for token in line[0]:
                if not token.startswith('//'):
                    fline.append(token)
                else:
                    break
            if len(fline) > 0:
                filtered.append((fline, line[1]))
        except IndexError:
            # Empty line.
            pass
    return filtered


def identify_labels(program):
    """Get a dictionary of label definitions and their box number."""
    labels = dict()
    mbox = 0
    for line in program:
        ctoken = line[0][0]
        if ctoken.upper() not in OPCODES:
            labels[ctoken] = mbox
        mbox += 1
    return labels


def compile_opcode(opcode, lnum):
    """Compile an opcode from an LMC program."""
    try:
        if OPCODES[opcode]['maxop'] is not None:
            try:
                return OPCODES[opcode]['code'] * 100
            except TypeError:
                # DAT
                pass
        else:
            return OPCODES[opcode]['code']
    except KeyError:
        error("Unrecognised operation '" + str(opcode) + "' on line " + str(lnum))
    return 0


def compile_operand(opcode, operand, lnum, labels):
    """Compile an operand from an LMC program."""
    maxop = OPCODES[opcode]['maxop']
    if maxop is not None:
        try:
            value = int(operand)
            if value < 0 or value > maxop:
                error("Operand must be between 0 and " + str(maxop) + " on line " + str(lnum))
            return value
        except ValueError:
            try:
                return labels[operand]
            except KeyError:
                error("Unrecognised label '" + str(operand) + "' on line" + str(lnum))
        except TypeError:
            if opcode != 'DAT':
                error("Missing operand on line " + str(lnum))

    return 0


def compile_line(line, lnum, labels):
    """Compile a single line in an LMC assembly program."""

    # Skip labels.
    if line[0] in labels:
        line = line[1:]

    try:
        opcode = line[0].upper()
    except IndexError:
        error("Label only on line " + str(lnum))

    # Get the opcode number.
    value = compile_opcode(opcode, lnum)

    # Get any operand number.
    try:
        operand = line[1]
    except IndexError:
        operand = None
    value += compile_operand(opcode, operand, lnum, labels)

    return value


def compile(program):
    """Compile an LMC program in assembly form."""

    # First pass, recognise labels.
    labels = identify_labels(program)
#     print labels

    # Second pass, convert to a list of values.
    values = []
    for line in program:
#         print line[1], line[0]
        values.append(compile_line(line[0], line[1], labels))

    return values


def get_args(parser=None, have_filename=False):
    """Set simulator arguments."""
    if parser is None:
        parser = argparse.ArgumentParser()
    if not have_filename:
        parser.add_argument("program", help="file name of program to run")
    parser.add_argument("-n", "--numeric", action="store_true",
                        help="program is pre-compiled numeric format")
    parser.add_argument("-d", "--dump-numeric",
                        help="dump a pre-compiled program in numeric format")
    args = parser.parse_args()
    return args


def get_mnemonic_program(filename):
    """Get an LMC program in assembly form and compile it."""
    program = read_mnemonic_file(filename)
    program = filter_program(program)
    return compile(program)


def get_numeric_program(filename):
    """Get an LMC program in numeric (compiled) form."""
    return read_numeric_file(filename)


def dump_numeric_program(filename, values):
    """Dump a program as a set of numeric values to a file."""
    with open(filename, "w") as f:
        for val in values:
            print(val, file=f)


def startup(filename=None, parser=None):
    """Read simulator arguments and return an LMC program."""
    args = get_args(parser=parser, have_filename=(filename is not None))
    if filename is None:
        filename = args.program
    if args.numeric or filename.endswith('.lmv'):
        values = get_numeric_program(filename)
    else:
        values = get_mnemonic_program(filename)
    if args.dump_numeric is not None:
        dump_numeric_program(args.dump_numeric, values)
    return values


def get_frequency():
    """Return the frequency."""
    return FREQ


def set_frequency(freq):
    """Set the frequency."""
    global FREQ
    FREQ = freq


def access_memory():
    """Add the latency of a memory access."""
    time.sleep(MEMLAT)
    return int(math.ceil(MEMLAT * FREQ))


def access_cache(size=10):
    """Add the latency of a cache access."""
    if size < 100:
        lat = (size**2) / 5000000.
    else:
        error("Cache size " + str(size) + " is bigger than the number of mailboxes")
    time.sleep(lat)
    return int(math.ceil(lat * FREQ))