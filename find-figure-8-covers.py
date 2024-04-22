from low_index import *

relators = ['AdaC', 'BabC', 'CdcB']

covers = permutation_reps(4, relators, [], 10)

# Data types:

# permutation on k symbols: list of ( 0 ≤ i < k integer) of length k
# entries define permutation output f(i) = v[i]

# permutation-representation: [ permutation, permutation, permutation, permutation]
# permutations on the generators a, b, c, d

# Going from the generators to edge labels
# 
# x = ()
# p = a
# q = b
# r = D
# y = qr = aD
# z = pq = ab


# A 10-tuple of perumtation symbols represents a single copy of the
# fundamental unit of the Dehn complex, with the following index condition
#
#
# 0 - r - 1
# |       |
# y   I   x
# |       |
# 2 - p - 3 - q - 4
# |       |       |
# x  II   z  III  y
# |       |       |
# 5 - q - 6 - p - 7
# |       |
# y   IV  x
# |       |
# 8 - r - 9
#
# lab(x) = permutation label on vertex number x
#
# one copy of the fundamental unit is a python tuple T with the property
#    T(x) = lab(x)


# labeled-square-complex: list of (10-tuple of permutation symbols) of length k

# For example the cover corresponding to the irregular degree 4 cover is represented by
# 
# [ (0,1,3,1,2,3,3,1,0,3),
#   (1,3,2,3,3,2,0,0,1,0),
#   (2,2,1,2,0,1,2,3,2,2),
#   (3,0,0,0,1,0,1,2,3,1) ]
#
# See picture in discord for schematic correspondence.

def inverse(permutation):
    out = list(range(len(permutation)))
    for i in range(len(permutation)):
        out[permutation[i]] = i
    return out


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


# Implement
# generate_squares: permutation-representation ->
#  labeled-square-complex
def generate_squares(perm_rep):
    a = perm_rep[0]
    b = perm_rep[1]
    c = perm_rep[2]
    d = perm_rep[3]
    A = inverse(a)
    D = inverse(d)

    degree = len(a)
    complexes = [tuple()] * degree
    for i in range(degree):
        complexes[i] =(
            i,  # 0
            D[i],  # 1
            a[D[i]],  # 2
            D[i],  # 3
            b[D[i]],  # 4
            a[D[i]],  # 5
            b[a[D[i]]],  # 6
            A[b[a[D[i]]]],  # 7
            a[D[a[D[i]]]],  # 8
            d[a[D[a[D[i]]]]]  # 9
        )

    return complexes


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


# for c in covers:
#     kind = is_special_cover(c)
#     if kind:
#         print(kind, c)


covers_test = [[0, 3, 1, 2], [1, 2, 0, 3], [2, 1, 3, 0], [3, 0, 2, 1]]
squares_test = generate_squares(covers_test)
for i in squares_test:
    print(i)
