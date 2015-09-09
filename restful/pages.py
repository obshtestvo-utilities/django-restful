from math import ceil, floor
from collections import Sequence

class RestfulPaging(Sequence):
    def __init__(self, count, start, limit):
        self.current_page = floor(start / limit) + 1  # account for exact matches, i.e. 20/20
        self.pages_count = self.current_page + ceil((count-(start+limit))/limit)
        if self.pages_count == 0:
            raise Exception("No pages")
        self.limit = limit
        self.current_start = start

    def __getitem__(self, index):
        page_num = index+1
        if page_num > self.pages_count:
            raise IndexError
        is_current = page_num == self.current_page
        if page_num < self.current_page:
            start = index * self.limit
        else:
            start = self.current_start + self.limit*(page_num - self.current_page)

        if page_num + 1 == self.current_page:
            limit = self.current_start-start
        else:
            limit = self.limit

        return {
            "number": page_num,
            "is_current": is_current,
            "start": start,
            "limit": limit
        }

    def __len__(self):
        return self.pages_count

    def has_next_page(self):
        return self.current_page < self.pages_count

    def previous_page(self):
        return self[self.current_page-2]  # python array is zero-based, paging is one-based

    def next_page(self):
        return self[self.current_page]  # python array is zero-based, paging is one-based

    def has_previous_page(self):
        return self.current_page != 1
