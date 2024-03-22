from low_index import *

relators = ['AdaC', 'BabC', 'CdcB']

covers = permutation_reps(4, relators, [], 10)

for c in covers:
    kind = is_special_cover(c)
    if kind:
        print (kind, c)

# Data types:

# permutation on k symbols: list of ( 0 ≤ i < k integer) of length k
# entries define permutation output f(i) = v[i]

# permutation-representation: [ permutation, permutation, permutation, permutation]
# permutations on the generators a, b, c, d


def kev_inverse(permutation):
    return

def ivy_inverse(permutation):
    return

# is_special_cover: permutation-representation -> 
#   false or "A-special" or "C-special" or "both"
def is_special_cover(perm-rep):
    C = generate_squares(perm-rep)
    H = search_hyperplanes(C)
    one_sided = false
    indirect_osculation = false
    for h in H:
        if is_one_sided(h):
            one_sided = true
            if self_osculates(h):
                return false
        else:
            if direct_osculates(h):
                return false
            else if self_osculates(h):
                indirect_osculation = true

    # if we get here we're some kind of special
    if one_sided:
        return "C-special"
    else if indirect_osculation:
        return "A-special"
    else
        return "both"

# generate_squares: permutation-representation ->
#  labeled-square-complex
def generate_squares(perm-rep):
    return [];

# search_hyperplanes: labeled-square-complex ->
#   list of hyperplane
def search_hyperplanes(square-cx):
    return [];

# is_one_sided: hyperplane -> bool
def is_one_sided(hyp):
    return false

# self_osculates: hyperplane -> bool
def self_osculates(hyp):
    return false

# direct_osculates: hyperplane -> bool
def direct_osculates(hyp):
    return false
