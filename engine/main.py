#!/bin/python
from threading import Thread
from PatternParser import Parser
from Queue import Queue
from DataPipe.DataPipe import DataPipe

if __name__ == "__main__":
    queue = Queue(1000)
    parser = Parser(queue, DataPipe)
    thread = Thread(target=parser.parse).start()
