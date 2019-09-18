"""
Skeleton implementation of the Little Man Computer.

Copyright (c) 2018, University of Cambridge
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
import sys

import lmhelper as lmh

# Memory
mailboxes = dict([(i, None) for i in range(0, 100)])


def print_mailboxes():
    """Print out the values in the mailboxes."""
    print(mailboxes)


def set_mailbox(index, value):
    if value >= 1000:
        value = value - 1000
    if value < 0:
        value += 1000    
    mailboxes[index] = value


def load_program(values):
    """Place values into consecutive mailboxes."""
    mbox = 0
    for val in values:
        mailboxes[mbox] = val
        mbox += 1


pc = 0


def fetch():
    """Get the next instruction from the mailboxes."""
    global pc
    instruction = mailboxes[pc]
    pc = pc + 1
    return instruction


def decode(inst):
    """Split an instruction into the opcode and operands."""
    opcode = int(inst / 100)
    operand = inst - (opcode*100)
    return opcode, operand


accumulator = 0
outbox = 0
flag = False
branches = 0
overflows = 0
underflows = 0

def checkAcc(accumulator):
    if accumulator < 0:
        accumulator += 1000
        underflows += 1
        flag = True
    elif accumulator > 999:
        accumulator -= 1000
        overflows += 1
        flag = True
    else:
        flag = False

def evaluate():
    global branches
    print("No of inst: " + inst + "\n")
    print("No of branches: " + branches + "\n")
    print("No of overflows: " + overflows + "\n")
    print("No of underflows: " + underflows + "\n")

def execute(opcode, operand):
    """Execute a single instruction, return True if a HLT."""
    global accumulator
    global outbox
    global flag
    if opcode == 1:
        accumulator += mailboxes[operand]
        checkAcc(accumulator)
        return False
    if opcode == 2:
        accumulator -= mailboxes[operand]
        checkAcc(accumulator)
        return False
    if opcode == 3:
        mailboxes[operand] = accumulator
        ##print(mailboxes[operand])
        return False
    if opcode == 5:
        accumulator = operand
        checkAcc(accumulator)
        return False
    if opcode == 6:
        pc = operand
        branches += 1
        return False
    if opcode == 7:
        if accumulator == 0:
            pc = operand
        else:
            None
        brances += 1
        return False
    if opcode == 8:
        if flag == False:
            pc = operand
        brances += 1
        return False
    if opcode == 9:
        if operand == 1:
            inbox = int(input("Inbox: "))
            accumulator = inbox
        elif operand == 2:
            outbox = accumulator
            print(outbox)
        elif operand == 3:
            None
        else:
            return False
        return False
    if opcode == 0:
        return True
    
    evaluate()
    return False


def tick():
    """Fetch, decode and execute one instruction."""
    inst = fetch()
    opcode, operand = decode(inst)
    return execute(opcode, operand)


def run():
    """Run the program until it's done."""
    finished = False
    while not finished:
        finished = tick()


if __name__ == '__main__':
    # Read a program and parse it into a list of values
    # Remove the file name to choose one on the command line
    values = lmh.startup("progs/add.lmc")
    # Load the list of values into the mailboxes
    load_program(values)
    # Print the contents of the mailboxes
    print_mailboxes()
    # Run the program
    run()