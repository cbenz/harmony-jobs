# -*- coding: utf-8 -*-


from datetime import datetime

from biryani1.baseconv import (cleanup_line, function, guess_bool, input_to_int, noop, not_none, pipe, struct, test,
                               test_in, uniform_sequence)
from biryani1.bsonconv import object_id_to_str
from biryani1.datetimeconv import date_to_iso8601_str
import biryani1.states

from . import model


french_date_format = '%d/%m/%Y'
N_ = lambda message: message


# Level 1 converters


# Level 2 converters
