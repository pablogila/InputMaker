'''
# Description
Common functions to search and analyze data contained in text files.

# Index
- TO-DO

---
'''


from .file import *
import mmap
import re


def line(keyword:str, file:str, stop_at:int=0, lines_below:int=0):
    '''
    Finds the line(s) containing the `keyword` string in the given `file`.\n
    The value `stop_at` specifies the max number of matches to be returned.
    Defaults to 0 to return all possible matches. Set it to 1 to return only one match,
    or to negative numbers to start the search from the end of the file upwards.\n
    The value `lines_below` specifies the additional lines below the target line that are also returned;
    2 to return the found line plus two lines below, etc.
    Negative values return the specified number of lines before the target line,
    yet preserving the original ordering from the file.
    Defaults to `lines_below=0`, only returning the target line.
    
    TO-IMPLEMENT: lines_below working
    '''
    file_path = get(file)
    matches = []
    with open(file_path, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)
        # Determine search direction and starting index
        if stop_at < 0:
            start_index = len(mm) - 1
            step = -1
        else:
            start_index = 0
            step = 1
        found_count = 0
        while 0 <= start_index < len(mm) and found_count < abs(stop_at):
            # Find the next match based on the search direction
            match_start = mm.rfind(keyword.encode(), 0, start_index) if step < 0 else mm.find(keyword.encode(), start_index)
            if match_start == -1:
                break
            # Extract the matched line and append it to the results
            match_end = mm.find(b'\n', match_start)
            print(match_start, match_end)
            match_line = mm[match_start:match_end].decode()
            matches.append(match_line)
            # Update the search index to avoid repeated matches
            start_index = match_start - 1 if step < 0 else match_end + 1
            found_count += 1
    return matches