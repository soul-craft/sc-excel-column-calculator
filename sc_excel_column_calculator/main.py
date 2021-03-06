# The MIT License (MIT)
#
# Copyright (c) 2022 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from sc_utilities import Singleton
from sc_utilities import log_init, calculate_column_index, calculate_column_name_from_index

log_init()

from sc_excel_column_calculator import PROJECT_NAME, __version__
import argparse
import re
import json


class Runner(metaclass=Singleton):

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        columns = args.columns
        column_pairs = dict()
        if args.reverse:
            for column in columns:
                if re.match(r'^[0-9]|[1-9][0-9]+$', column) is None:
                    logging.getLogger(__name__).exception('bad input {}, numeric characters only'.format(column))
                    continue
                value = int(column)
                column_name = calculate_column_name_from_index(value)
                column_pairs[value] = column_name
        else:
            for column in columns:
                if re.match(r'^[a-zA-Z]+$', column) is None:
                    logging.getLogger(__name__).exception('bad input {}, alpha characters only'.format(column))
                    continue
                column_index = calculate_column_index(column)
                column_pairs[column] = column_index
        json_str = json.dumps(column_pairs, indent=2)
        logging.getLogger(__name__).info("column pairs {}".format(json_str))
        return 0


def main():
    try:
        parser = argparse.ArgumentParser(description='Python project')
        parser.add_argument('columns', metavar='N', nargs='+',
                            help='Columns: a list of column letters or column indexes')
        parser.add_argument("--reverse", action='store_true', default=False,
                            help="if calculate column name from column index")
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
