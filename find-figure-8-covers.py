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


# A 10-tuple of permutation symbols represents a single copy of the
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


def composition(sigma_1, sigma_2):
    # should return sigma_1(sigma_2([i]))
    comp = list(range(len(sigma_1)))
    for index in range(len(sigma_1)):
        comp[index] = sigma_1[sigma_2[index]]
    return comp


# is_special_cover: permutation-representation -> 
#   false or "A-special" or "C-special" or "both"
def is_special_cover(perm_rep, dictionary):
    C = generate_squares(perm_rep)
    H = search_hyperplanes(C)
    print(len(H))
    one_sided = False
    indirect_osculation = False
    for h in H:
        if is_one_sided(h):
            one_sided = True
            if self_osculates(h, dictionary):
                return "one-sided + osculation"
        else:
            if direct_osculates(h, dictionary):
                return "orientable + direct osculation"
            elif self_osculates(h, dictionary):
                indirect_osculation = True

    # if we get here we're some kind of special
    if one_sided:
        return "C-special"
    elif indirect_osculation:
        return "A-special"
    else:
        return "both"


# generate labels takes the sigma representations of a,b,c and returns dictionary mapping p,q,r,x,y,z to sigma
def generate_labels(perm_rep):
    labels_ = {}
    a = perm_rep[0]
    b = perm_rep[1]
    # c = perm_rep[2]
    d = perm_rep[3]

    labels_["p"] = a
    labels_["q"] = b
    labels_["r"] = inverse(d)

    sigma_x = list(range(len(perm_rep[0])))
    for i_ in range(len(sigma_x)):
        sigma_x[i_] = i_

    labels_["x"] = sigma_x
    labels_["y"] = composition(inverse(d), b)
    labels_["z"] = composition(b, a)

    return labels_


# Implement
# generate_squares: permutation-representation ->
#  labeled-square-complex
def generate_squares(perm_rep):
    a = perm_rep[0]
    b = perm_rep[1]
    # c = perm_rep[2]
    d = perm_rep[3]
    A = inverse(a)
    D = inverse(d)

    degree = len(a)
    complexes = [tuple()] * degree
    for s in range(degree):
        complexes[s] = (
            s,  # 0
            D[s],  # 1: i.r
            a[D[s]],  # 2: i.y
            D[s],  # 3: i.rx
            b[D[s]],  # 4: i.rxq
            a[D[s]],  # 5: i.yx
            b[a[D[s]]],  # 6: i.yxq = i.rxz
            A[b[a[D[s]]]],  # 7: i.yxqP
            a[D[a[D[s]]]],  # 8: i.yxy
            d[a[D[a[D[s]]]]]  # 9: i.yxyR
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
    return list(map(lambda e: (e[0], e[1], -1*oedge[2]), find_neighbors(oedge, square_cx)))


def generate_hyperplane(edge, square_cx):
    hyp = set()
    hyp.add(edge)

    neighbors = set(find_neighbors(edge, square_cx))

    while len(neighbors - hyp) > 0:
        new = neighbors - hyp
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
        hyp = hyp | neighbors
        neighbors = set()
        for n in new:
            neighbors |= set(find_neighbors_oriented(n, square_cx))

    return hyp


# search_hyperplanes: labeled-square-complex ->
#   list of hyperplane
# Goal: implement!
def search_hyperplanes(square_cx):
    # each hyperplane is a set of oriented edges
    # planes is a list of hyperplanes. (planes is a list of sets of oedges)
    planes = []

    # make set of all oriented edges
    oedges = set()
    for label_ in {"x", "y", "z", "p", "q", "r"}:
        for start_ in range(len(square_cx)):
            oedges.add((start_, label_, 1))
            oedges.add((start_, label_, -1))

    # take an edge, generate its hyperplane, add to output
    # delete the result from all edges
    # if you have edges left, do it again
    while len(oedges) > 0:
        new = generate_hyperplane_oriented(oedges.pop(), square_cx)  # pop removes arbitrary item, and returns it
        oedges -= new
        planes.append(new)

    return planes


# is_one_sided: oriented_hyperplane -> bool
# Goal: implement!
def is_one_sided(hyp):
    # hyp is a set of oriented edges
    # If a hyperplane is one-sided, every edge will appear in both orientations
    # The for loop will run exactly one time
    edge_ = list(hyp)[0]
    inverse_edge_ = (edge_[0], edge_[1], -1*edge_[2])
    return inverse_edge_ in hyp


# self_osculates: hyperplane -> bool
# Stretch goal
def self_osculates(hyp, dictionary):
    for edge_1 in hyp:
        for edge_2 in hyp:  # for each pair of edges
            if edge_1[0] == edge_2[0] and edge_1[1] != edge_2[1]:
                return True  # two edges with same origin, different labels
            if edge_2[1] != edge_2[1] and dictionary[edge_1[1]] == dictionary[edge_2[1]]:
                return True  # two edges with different labels, same "endpoint"
    return False


# direct_osculates: hyperplane -> bool
# Stretch goal
def direct_osculates(hyp, dictionary):
    for edge_1 in hyp:
        for edge_2 in hyp:  # for each pair of edges
            if edge_1[0] == edge_2[0] and edge_1[1] != edge_2[1] and edge_1[2] == edge_2[2]:
                return True  # two edges with same origin, different labels, AND orientations match
            if edge_2[1] != edge_2[1] and dictionary[edge_1[1]] == dictionary[edge_2[1]] and edge_1[2] == edge_2[2]:
                return True  # two edges with different labels, same "endpoint" AND orientations match
    return False


for c in covers:
    d = generate_labels
    kind = is_special_cover(c, d)
    if kind:
        print(kind, c)

# covers_test = covers[6]
# labels = generate_labels(covers_test)
# for l1 in labels:
#     print(l1)
#     print(labels[l1])
