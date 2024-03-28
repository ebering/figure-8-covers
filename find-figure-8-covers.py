from low_index import *

relators = ['AdaC', 'BabC', 'CdcB']

covers = permutation_reps(4, relators, [], 10)

# Data types:

# permutation on k symbols: list of ( 0 ≤ i < k integer) of length k
# entries define permutation output f(i) = v[i]

# permutation-representation: [ permutation, permutation, permutation, permutation]
# permutations on the generators a, b, c, d


def kev_inverse(permutation):
    out = [0] * len(permutation)
    for i in range(len(permutation)):
        out[permutation[i]] = i
    return out


def ivy_inverse(permutation):
    return


# is_special_cover: permutation-representation -> 
#   false or "A-special" or "C-special" or "both"
def is_special_cover(perm_rep):
    C = generate_squares(perm_rep)
    H = search_hyperplanes(C)
    one_sided = False
    indirect_osculation = False
    for h in H:
        if is_one_sided(h):
            one_sided = True
            if self_osculates(h):
                return True
        else:
            if direct_osculates(h):
                return False
            elif self_osculates(h):
                indirect_osculation = True

    # if we get here we're some kind of special
    if one_sided:
        return "C-special"
    elif indirect_osculation:
        return "A-special"
    else:
        return "both"


# generate_squares: permutation-representation ->
#  labeled-square-complex
def generate_squares(perm_rep):
    return []


# search_hyperplanes: labeled-square-complex ->
#   list of hyperplane
def search_hyperplanes(square_cx):
    return []


# is_one_sided: hyperplane -> bool
def is_one_sided(hyp):
    return False


# self_osculates: hyperplane -> bool
def self_osculates(hyp):
    return False


# direct_osculates: hyperplane -> bool
def direct_osculates(hyp):
    return False


permutation_1 = [1, 3, 4, 0, 2]
print(permutation_1)
print(kev_inverse(permutation_1))
print(kev_inverse(kev_inverse(permutation_1)))


for c in covers:
    kind = is_special_cover(c)
    if kind:
        print(kind, c)
