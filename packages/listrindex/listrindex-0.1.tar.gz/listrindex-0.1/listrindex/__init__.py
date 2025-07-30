from typing import List

class listrindex:
    def rindex(self, ln: List, obj) -> int:
        return len(ln)-ln[::-1].index(obj)-1 # returns the last index of the element