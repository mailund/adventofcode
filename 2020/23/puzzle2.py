
class Link(object):
    def __init__(self, val, prev = None, next = None):
        self.val = val
        self.prev = prev
        self.next = next

        if self.prev is not None:
            self.prev.next = self
        else:
            self.prev = self # circular list
        if self.next is not None:
            self.next.prev = self
        else:
            self.next = self # circular list

    def __contains__(self, val):
        link = self
        while True:
            if link.val == val: return True
            link = link.next
            if link is self: return False

    def __str__(self):
        links = [f"{self.val}"]
        link = self.next
        while link != self:
            links.append(f"{link.val}")
            link = link.next
        return " -> ".join(links)

def make_linked_list(x):
    link = Link(x[0])
    link.next = link.prev = link
    for y in x[1:]:
        Link(y, link.prev, link) # appending
    return link

def take_three(link):
    start = link.next
    end = start.next.next
    start.prev.next = end.next
    end.next.prev = start.prev
    # make circular
    start.prev = end
    end.next = start
    return start

def insert_after(link, lst):
    lst.prev.next = link.next
    lst.prev.next.prev = lst.prev
    link.next = lst ; lst.prev = link


# These are given from the puzzle by now...
min_cup = 1
max_cup = 1_000_000

def dec(i):
    return (i - 1) if (i - 1) >= min_cup else max_cup

def play(starting_cups):
    
    # Fill the cups to the max
    for i in range(10, max_cup + 1):
        Link(i, starting_cups.prev, starting_cups)

    # starting cup
    cup = starting_cups

    # Build dict to map from index to link
    LINK_MAP = {}
    LINK_MAP[cup.val] = cup
    link = cup.next
    while link != cup:
        LINK_MAP[link.val] = link
        link = link.next

    # Now play the game...
    for i in range(10):#_000_000):
        if i % 1_000_000 == 0:
            print(i)
        
        removed = take_three(cup)
        print(removed)

        dest = dec(cup.val)
        while dest in removed:
            dest = dec(dest)

        insert_after(LINK_MAP[dest], removed)
        
        cup = cup.next

    return LINK_MAP[1].next.val * LINK_MAP[1].next.next.val

inp = "137826495" # puzzle input
inp = "389125467" # test data
cups = make_linked_list(list(map(int, inp)))
print(f"Puzzle #2: {play(cups)}")

