'''
'''

def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    return max(hands, key=hand_rank);


# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens 
#                  this function would return 7.
# two_pair(ranks): if there is a two pair, this function 
#                  returns their corresponding ranks as a 
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
# card_ranks(hand) returns an ORDERED tuple of the ranks 
#                  in a hand (where the order goes from
#                  highest to lowest rank). 
def hand_rank():
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks));# your code here
    elif flush(hand):                              # flush
        return (5, ranks);# your code here
    elif straight(ranks):                          # straight
        return (4, max(ranks))# your code here
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks);# your code here
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks);# your code here
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks);# your code here
    else:                                          # high card
        return (0, ranks);# your code here

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ["--23456789TJQKA".index(r) for r,s in cards];
    ranks.sort(reverse=True);
    return ranks;

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    # Your code here.
#    i = ranks[0] - 1; 
#    stra = True;
#    for r in ranks[1:]:
#        if r == i:
#            i = i - 1;
#        else:
#            stra = False;
#            break;
#    return stra;
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5;
            
def flush(hand):
    "Return True if all the cards have the same suit."
    # Your code here.
    ranks = [s for r,s in hand];
#    suit = True;
#    t = ranks[0];
#    for r in ranks[1:]:
#        if t != r:
#            suit = False;
#            break;
#    return suit;
    return len(set(ranks)) == 1;

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    # Your code here.

def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split(); # => ['6C', '7C', '8C', '9C', 'TC']
    fk = "9D 9H 9S 9C 7D".split();
    fh = "TD TC TH 7C 7D".split();
    assert poker([sf, fk, fh]) == sf;
    
    # Add 2 new assert statements here. The first 
    # should check that when fk plays fh, fk 
    # is the winner. The second should confirm that
    # fh playing against fh returns fh.
    
    assert poker([fk, fh]) == fk;
    assert poker([fh, fh]) == fh;
    
    # Add 2 new assert statements here. The first 
    # should assert that when poker is called with a
    # single hand, it returns that hand. The second 
    # should check for the case of 100 hands.
    
    assert poker([sf]) == sf;
    assert poker([sf] + 99*[fk]) == sf;
    
    #
    # add 3 new assert statements here.
    #
    
    assert hand_rank(sf) == (8, 10);
    assert hand_rank(fk) == (7, 9, 7);
    assert hand_rank(fh) == (6, 10, 7);
    
    # Modify the test() function to include three new test cases.
    # These should assert that card_ranks gives the appropriate
    # output for the given straight flush, four of a kind, and
    # full house.    
    
    assert card_ranks(sf) == [10, 9, 8, 7, 6];
    assert card_ranks(fk) == [9, 9, 9, 9, 7];
    assert card_ranks(fh) == [10, 10, 10, 7, 7];
    
    return "test pass";
    
print (test());
