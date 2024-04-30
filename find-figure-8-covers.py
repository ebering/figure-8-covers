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
#    T[x] = lab(x)


# labeled-square-complex: list of (10-tuple of permutation symbols) of length k

# For example the cover corresponding to the irregular degree 4 cover is represented by
# 
# [ (0,1,3,1,2,3,3,1,0,3),
#   (1,3,2,3,3,2,0,0,1,0),
#   (2,2,1,2,0,1,2,3,2,2),
#   (3,0,0,0,1,0,1,2,3,1) ]
#
# See picture in discord for schematic correspondence.

# edge: (symbol, edge-label)
# edge-label: "p" or "q" or "r" or "x" or "y" or "z"
# orientation: 1 or -1
# oriented-edge: (symbol, edge-label, orientation)
# hyperplane: set(edge)
# oriented-hyperplane: set(oriented-edges)


def inverse(permutation):
    out = list(range(len(permutation)))
    for index in range(len(permutation)):
        out[permutation[index]] = index
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
        complexes[i] = (
            i,  # 0
            D[i],  # 1: i.r
            a[D[i]],  # 2: i.y
            D[i],  # 3: i.rx
            b[D[i]],  # 4: i.rxq
            a[D[i]],  # 5: i.yx
            b[a[D[i]]],  # 6: i.yxq = i.rxz
            A[b[a[D[i]]]],  # 7: i.yxqP
            a[D[a[D[i]]]],  # 8: i.yxy
            d[a[D[a[D[i]]]]]  # 9: i.yxyR
        )

    return complexes


# Implement
# find_neighbors: edge labeled-square-complex -> list of edge
def find_neighbors(edge, square_cx):
    # Cases, one for each label (use a python match statement)
    output = []
    match edge[1]:  # label of edge
        case "x":
            for cx in square_cx:
                if edge[0] == cx[3]:
                    output.append((cx[0], "y"))
                if edge[0] == cx[5]:
                    output.append((cx[3], "z"))
                if edge[0] == cx[9]:
                    output.append((cx[5], "y"))
            return output
        case "y":
            for cx in square_cx:
                if edge[0] == cx[0]:
                    output.append((cx[3], "x"))
                if edge[0] == cx[5]:
                    output.append((cx[9], "x"))
                if edge[0] == cx[7]:
                    output.append((cx[3], "z"))
            return output
        case "z":
            for cx in square_cx:
                if edge[0] == cx[3]:
                    output.append((cx[5], "x"))
                    output.append((cx[7], "y"))
            return output
        case "p":
            for cx in square_cx:
                if edge[0] == cx[3]:
                    output.append((cx[0], "r"))
                    output.append((cx[5], "q"))
                if edge[0] == cx[7]:
                    output.append((cx[3], "q"))
            return output
        case "q":
            for cx in square_cx:
                if edge[0] == cx[3]:
                    output.append((cx[7], "p"))
                if edge[0] == cx[5]:
                    output.append((cx[3], "p"))
                    output.append((cx[9], "r"))
            return output
        case "r":
            for cx in square_cx:
                if edge[0] == cx[0]:
                    output.append((cx[3], "p"))
                if edge[0] == cx[9]:
                    output.append((cx[5], "q"))
            return output


def find_neighbors_oriented(oedge, square_cx):
    return list(map(lambda e: (e[0],e[1], -1*oedge[2]), find_neighbors(oedge, square_cx)))


def generate_hyperplane(edge, square_cx):
    hyp = set()
    hyp.add(edge)

    neighbors = set(find_neighbors(edge, square_cx))

    while len(neighbors - hyp) > 0:
        new = neighbors - hyp
        print(new)
        hyp = hyp | neighbors
        neighbors = set()
        for n in new:
            neighbors |= set(find_neighbors(n, square_cx))

    return hyp


def generate_hyperplane_oriented(oedge, square_cx):
    hyp = set()
    hyp.add(oedge)

    neighbors = set(find_neighbors_oriented(oedge, square_cx))

    while len(neighbors - hyp) > 0:
        new = neighbors - hyp
        print(new)
        hyp = hyp | neighbors
        neighbors = set()
        for n in new:
            neighbors |= set(find_neighbors_oriented(n, square_cx))

    return hyp


# search_hyperplanes: labeled-square-complex ->
#   list of hyperplane
#Goal: implement!
def search_hyperplanes(square_cx):
    # make all oriented edges

    # take an edge, generate its hyperplane, add to output
    # delete the result from all edges
    # if you have edges left, do it again

    return []


# is_one_sided: oriented_hyperplane -> bool
# Goal: implement!
def is_one_sided(hyp):
    # one way: add square_cx as an argument
    # and check if the oriented and unoriented have different
    # sizes

    # Another way: take the first edge e and check if opp(e)\in hyp
    return False


# self_osculates: hyperplane -> bool
# Stretch goal
def self_osculates(hyp):
    return False


# direct_osculates: hyperplane -> bool
# Stretch goal
def direct_osculates(hyp):
    return False


# for c in covers:
#     kind = is_special_cover(c)
#     if kind:
#         print(kind, c)

covers_test = covers[6]
squares_test = generate_squares(covers_test)
hypertestvert = generate_hyperplane((0,"r"),squares_test)
hypertesthoriz = generate_hyperplane((0,"y"),squares_test)
hyperorient = generate_hyperplane_oriented((0,"r",1),squares_test)
print(hyperorient)
print(len(hyperorient))

for i in squares_test:
   print(i)
