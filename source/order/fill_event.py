#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import Timestamp
from ..event.event import *
from ..position.position import Position
from ..util.util_func import retrieve_multiplier_from_full_symbol

class FillEvent(Event):
    """
    Fill event, with filled quantity/size and price
    """
    def __init__(self):
        """
        Initialises fill
        """
        self.event_type = EventType.FILL
        self.internal_fill_id = -1
        self.internal_order_id = -1
        self.broker_order_id = -1
        self.timestamp = Timestamp('1900-01-01', tz='UTC')
        self.full_symbol = ''
        self.fill_price = 0.0
        self.fill_size = 0     # size < 0 means short order is filled
        self.exchange = ''
        self.commission = 0.0
        self.account = ''
        self.source = -1

    def to_position(self):
        """
        if there is no existing position for this symbol, this fill will create a new position
        (otherwise it will be adjusted to exisitng position)
        """
        if self.fill_size > 0:
            average_price_including_commission = self.fill_price + self.commission \
                                                                     / retrieve_multiplier_from_full_symbol(self.full_symbol)
        else:
            average_price_including_commission = self.fill_price - self.commission \
                                                                     / retrieve_multiplier_from_full_symbol(self.full_symbol)

        new_position = Position(self.full_symbol, average_price_including_commission, self.fill_size)
        return new_position