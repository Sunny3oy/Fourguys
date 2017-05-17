import datetime as dt

# Should return a time.
def time_difference(time1, time2):
    return dt.datetime.timedelta()

# Should return a time.
def time_add(time1, time2):
    return dt.datetime.timedelta()

class _FakeTime:

    NORMAL_STATE = 'NORMAL'
    FROZEN_STATE = 'FROZEN'
    FAST_FORWARD_STATE = 'FF'

    def __init__(self):
        # A delta to add to the current time.
        self.offset = dt.timedelta()
        # A reference time to base things off of when the flow of time
        # changes. Either frozen, slower, or faster.
        self.timeSnapshot = None
        self.state = _FakeTime.NORMAL_STATE

    # TODO: Put some validation here.
    # - offset: ATM, another time delta object.
    def set_offset(self, offset):
        self.offset = offset

    def get_now(self):
        if self.state == _FakeTime.NORMAL_STATE:
            return self.offset + dt.datetime.now()
        #elif self.state == _FakeTime.FROZEN_STATE:
            #return self.timeSnapshot
        #elif self.state == _FakeTime.FAST_FORWARD_STATE:
            #return self.timeSnapshot

    #def freeze_time(self):
        #self.timeSnapshot = self.get_now()
        #self.state = _FakeTime.FROZEN_STATE

    #def start_time(self):
        ## Set offset such that current time + offset equals last
        ## recorded fake time.
        #self.offset = time_difference(dt.datetime.now(), self.get_now())
        #self.state = _FakeTime.NORMAL_STATE

FakeTime = _FakeTime()

# - toordinal: Seems to convert everything to seconds, or something like
#   it. Though it seems that ordinals do not return seconds. Their
#   resolution is minutes.
# - Timestamps seem to be a good option for taking differences when
#   dealing with non-delta times.

# Guiding principle of design:
# - The time curve should pretty much be smooth, except for the changing
#   of the offset. When starting to fastforward, increase the multiplier
