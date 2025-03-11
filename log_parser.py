from datetime import datetime
import re
from collections import defaultdict
from functools import reduce
from itertools import chain

# Read file from /etc/httpd/logs/access_log

'''
Declare a generator function which does not load the whole file at once,
but reads a line at a time from the file to reduce memory usage, nice and lazy.

This is functional, as the loop yeilds each value as soon as it is processed and does
not rely on or change any external state.
'''
def log_generator():
    with open('/etc/httpd/logs/access_log', 'r') as log_file:
        yield from (match.group()
                    for match in chain.from_iterable(
                    re.finditer(r'\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4}',
                                line) for line in log_file))

'''
Reformat the date to be easier to count and read;
Return nothing using 'pass' if it is not a valid datetime;
Only called within map, keeping the approach functional by mitigating potential side effects.
'''
def reformat_date_string(date_string):
    try:
        return datetime.strftime(
            datetime.strptime(date_string, '%d/%b/%Y:%H:%M:%S %z'),
            '%d/%b/%Y:%H')
    except ValueError:
        pass
    
'''
Reducer function to perform the count using a dict in the reducer call;
Side effects are contained within a reduce() call, keeping this functional;
Returning a new acc each time prevents mutation of the outside accumulator;
Unpacks the incoming acc to create a new one, checks for the key using .get();
If no key exists, start count from 0.
'''
def count_entries(acc, log):
    return {**acc, log: acc.get(log, 0) + 1}

'''
Perform the reduction action;
Returns a map (type: defaultdict(int)) and calls the reducer function;
Filter to remove invalid dates that are returned as 'None'.
'''
def get_counts():
    return reduce(
            count_entries, 
            map(lambda log: reformat_date_string(log), filter(None, log_generator())), 
            defaultdict(int))

'''
Kicks off the code with a call to sorted();
Outputs various stats.
'''
def output_stats():
    counted_logs = sorted(get_counts().items(), key=lambda kv: kv[1], reverse=True)
    
    print('The 5 most active hours on the server:\n')
    print('Date and hour ---  accesses made')
    list(map(lambda i: print(counted_logs[i]), range(0, 5)))
    
    print('The 5 least active hours:\n')
    print('Date and hour ---  accesses made')
    list(map(lambda i: print(counted_logs[i]), range(len(counted_logs)-5, len(counted_logs))))
    
    print('\nAverage accesses per hour: ' + str(
        round(sum(entry[1] for entry in counted_logs) / len(counted_logs), 2))+'\n')

output_stats()