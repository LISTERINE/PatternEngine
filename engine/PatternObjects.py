#!/usr/bin/python
from collections import defaultdict
from functools import wraps
from time import sleep
from copy import deepcopy


class BasePattern(object):
    # Keys are function names, values are a list of patternss
    registration = defaultdict(lambda : defaultdict(list))

    @staticmethod
    def register(pattern_obj=None,ttl=None):
        def wrap(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            if not BasePattern.registration[wrapper.__name__].has_key("callback"):
                BasePattern.registration[wrapper.__name__]["callback"] = wrapper
            if pattern_obj is not None:
                # Apply in reverse order
                BasePattern.registration[wrapper.__name__]["pattern"].insert(0,pattern_obj)
            if ttl is not None:
                BasePattern.registration[wrapper.__name__]["ttl"][:] = [ttl]
            return wrapper
        return wrap

    def __init__(self):
        self.pattern_list_restore = []
        self.pattern_list = []

    def build_patterns(self):
        self.pattern_list = []
        for k,v in BasePattern.registration.iteritems():
            # make new pattern with ttl
            g = ComplexPattern(*v["ttl"])
            # Push list of patterns to complexpattern
            g.patterns = v["pattern"]
            # Assign callback
            g.callback = v["callback"]
            # BasePatterns is now a list of patterns that will call callbacks on
            # completion
            self.pattern_list.append(g)
        self.pattern_list_restore = deepcopy(self.pattern_list)

    def reset(self):
        self.pattern_list = deepcopy(self.pattern_list_restore)


class AccelPattern(object):
    def __init__(self, t1, t2, ttl):
        """ Set an acceleration based pattern

        Low and high are tuples containing two values.
        When input data falls within the threshold specified
        by one of these values, the threshold is satisfied.
        ex.
        low = (20,40)
        # values that would satisfy low
        input = 25 # True
        input = 19 # False
        input = 20 # True
        input = 40 # True
        input = 41 # False

        When a value seen satisfies the low threshold,
        the pattern becomes actived.
        When checking completion progress once active,
        if new input does not match trend decrease ttl.
        Once ttl reaches 0, pattern is deactivated.
        Once active, if the high value is satisfied this
        pattern is evaluated as True.
        """
        self.type = "Accel"
        self.active = False
        self.low, self.high = sorted([t1,t2], key=lambda n:min(n))
        self.max_ttl = ttl
        self.ttl = ttl
        self.thresh1 = None
        self.thresh2 = None
        self.point = None

    def in_threshold(self, val, thresh):
        if val is None:
            return False
        if thresh[0] <= val <= thresh[1]:
            return True
        return False

    def process(self, input_data):
        """
        This method is used to determine the state of this pattern.
        pass new data points as input, evaluate them to determine
        pattern state.
        """
        if self.in_threshold(input_data.get(self.point,None), self.thresh1):
            self.active = True
            print "accel activating"
        if self.active:
            if self.ttl > 0:
                if self.in_threshold(input_data.get(self.point,None), self.thresh2):
                    print "got it!!"
                    self.reset()
                    return True
                else:
                    # If active and not finished
                    self.ttl -= 1
            else:
                # If active and no ttl
                self.reset()
        return False

    def reset(self):
        self.active = False
        self.ttl = self.max_ttl


class ComplexPattern(object):
    def __init__(self, ttl):
        self.ttl = ttl
        self.max_ttl = ttl
        self.patterns = []
        self.active = False
        self.current_pattern = 0
        self.live_patterns = False
        self.callback = lambda :None

    def process(self, input_data):
        if self.patterns[self.current_pattern].process(input_data):
            self.current_pattern += 1
            if not self.active:
                self.active = True
            if self.current_pattern >= len(self.patterns):
                self.reset()
                self.callback()
                return True
        self.live_patterns = any([g.active for g in self.patterns])
        if not self.live_patterns:
            self.ttl -= 1
            if self.ttl < 0:
                self.reset()
                return False
        return False

    def reset(self):
        self.current_pattern = 0
        self.active = False
        self.ttl = self.max_ttl
        self.live_patterns = False


class FingerPattern(object):
    def __init__(self, thumb=0, index=0, middle=0, ring=0, ttl=0):
        # A pattern is a dict which sets the values of
        # the fingers to 1 (closed) or 0 (open)
        self.type = "Finger"
        self.ttl = ttl
        self.max_ttl = ttl
        self.active = False
        self.pattern = {"thumb": thumb, "index": index,
                        "middle": middle, "ring": ring}

    def process(self, input_data):
        if input_data["type"] == "finger":
            if not self.active:
                self.active = True
            if all([input_data[k] == v for k,v in self.pattern.iteritems()]):
                self.reset()
                return True
            # If active and not finshed
            self.ttl -= 1
            if self.ttl <= 0:
                self.reset()
        return False

    def reset(self):
        self.active = False
        self.ttl = self.max_ttl

class XIncrease(AccelPattern):

    def __init__(self, *args, **kwargs):
        super(XIncrease,self).__init__(*args, **kwargs)
        self.thresh1 = self.low
        self.thresh2 = self.high
        self.point = "x"

class XDecrease(AccelPattern):

    def __init__(self, *args, **kwargs):
        super(XDecrease,self).__init__(*args, **kwargs)
        self.thresh1 = self.high
        self.thresh2 = self.low
        self.point = "x"

class YIncrease(AccelPattern):

    def __init__(self, *args, **kwargs):
        super(YIncrease,self).__init__(*args, **kwargs)
        self.thresh1 = self.low
        self.thresh2 = self.high
        self.point = "y"

class YDecrease(AccelPattern):

    def __init__(self, *args, **kwargs):
        super(YDecrease,self).__init__(*args, **kwargs)
        self.thresh1 = self.high
        self.thresh2 = self.low
        self.point = "y"
