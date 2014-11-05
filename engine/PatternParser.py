#/usr/bin/python
from collections import namedtuple
from time import sleep
from PatternObjects import BasePattern
from my_patterns import *
from sys import exit


class Parser():
    def __init__(self, queue, pipes):
        # Data queue
        self.queue = queue
        self.patterns = BasePattern()
        self.patterns.build_patterns()
        self.pipes = pipes
        self.active_patterns = []
        self.zombie_patterns = []

    def check_for_active(self, data):
        """ Try to activate a pattern.

        Checks if putting new data into any of the patterns makes them active
        If the pattern only needs one data point and completes, reset
        """

        for pattern in self.patterns.pattern_list:
            if pattern.process(data):
                self.reset()
                return
            elif pattern.active:
                self.active_patterns.append(pattern)

    def feed_active(self, data):
        """ Push data into active patterns to try to complete them.

        If an inactive pattern is found push it to the zombie list
        """
        for pattern in self.active_patterns:
            # If the pattern passes, reset
            if pattern.process(data):
                self.reset()
            if not pattern.active:
                self.zombie_patterns.append(pattern)

    def kill_zombies(self):
        """ Prune the zombie patterns """

        for pattern in self.zombie_patterns:
            if pattern in self.active_patterns:
                self.active_patterns.remove(pattern)
        self.zombie_patterns = []

    def push_to_pipes(self, data):
        """ Sends the data out to all the data pipes """
        for pipe in self.pipes.Pipes.iteritems():
            pipe.push(data)

    def print_pattens(self):
        """ Prints out all the active patterns """
        for pattern in self.active_patterns:
            print pattern
        print "________________________"

    def reset(self):
        self.patterns.reset()
        self.active_patterns = []
        self.zombie_patterns = []

    def parse(self):
        while True:
            data = self.queue.get()
            if not self.active_patterns:
                self.check_for_active(data)
            else:
                self.print_patterns()
                self.feed_active(data)
                self.kill_zombies()
                if len(self.active_patterns) == 0:# If we've run out of pattern, reset
                    self.reset()

if __name__ == "__main__":
    from Queue import Queue
    Parser(Queue(10))
