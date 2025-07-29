from fd_solver import *
import numpy as np

###############
### Testing ###      
###############
A = Symbol("A")
B = Symbol("B")
C = Symbol("C")
D = Symbol("D")
E = Symbol("E")

def check_basic():
    A = Symbol("A")
    B = Symbol("B")
    A2 = Symbol("A")
    print(A == A2)

    one = FunctionalDependency({A, B}, {B})
    one2 = FunctionalDependency({A2, B}, {B})

    print(one == one2)
    print(sorted({A, B, A2}))

def check_reflex():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")

    attrs = {A, B, C}
    print(attrs)
    print()
    for fd in get_reflexive(attrs):
        print(fd)

def check_augment():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")
    fd1 = FunctionalDependency(A, B)
    res = get_augmented(fd1, {C, D})
    print(fd1, "\n")
    for i in res:
        print(i)

def check_transitive():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")
    fd1 = FunctionalDependency(A, B)
    fd2 = FunctionalDependency(B, C)
    fd3 = FunctionalDependency(C, D)
    print(fd1, fd2, fd3, "\n")
    res = get_transitive({fd1, fd2, fd3})
    for i in res:
        print(i)

def check_decompose():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")
    fds = {
        FunctionalDependency(A, {B, C, D}),
        FunctionalDependency({C, D}, {A, B}),
        FunctionalDependency(D, A)
    }
    print(fds, "\n")
    res = make_decomposed(fds)
    for i in res:
        print(i)

def check_union():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")
    fds = {
        FunctionalDependency(A, B),
        FunctionalDependency(A, C),
        FunctionalDependency(B, C),
        FunctionalDependency(A, D)
    }
    print("Initial FDs:", fds, "\n")
    res = make_union(fds)
    for i in res:
        print(i)

def check_closure():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")

    fds = {
        FunctionalDependency(B, D),
        FunctionalDependency({B, D}, A),
        FunctionalDependency({A, D}, C)
    }
    print(fds, "\n")

    print("{B}+ =", compute_closure({B}, fds))
    print("{A}+ =", compute_closure({A}, fds))

def check_superkeys():
    fds = {
        FunctionalDependency({A, B}, C),
        FunctionalDependency({A, D}, B),
        FunctionalDependency(B, D)
    }

    print(fds, "\n")
    res = find_superkeys({A, B, C, D}, fds)
    print(res)
    # for i in res:
    #     print(set(i))

def check_keys():
    fds = {
        FunctionalDependency({A, B}, C),
        FunctionalDependency({A, D}, B),
        FunctionalDependency(B, D)
    }
    print(fds, "\n")
    res = find_keys(attrs={A, B, C, D}, fds=fds)
    print(res)

def check_cover():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")

    fds = {
        FunctionalDependency(A, {C, D}),
        FunctionalDependency({A, C}, D),
        FunctionalDependency({A, D}, B),
        FunctionalDependency(C, D)
    }
    print(fds, "\n")

    minco = minimal_cover(fds)
    canco = canonical_cover(fds)
    print("Minimal cover: ", minco)
    print("Canonical cover: ", canco)

def check_cover2():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")

    fds = {
        FunctionalDependency(A, {B, D}),
        FunctionalDependency({A, B}, C),
        FunctionalDependency(C, D),
        FunctionalDependency({B, C}, D)
    }
    print(fds, "\n")
    print(minimal_cover(fds))

def tut_q_3b():
    A = Symbol("A", "name")
    B = Symbol("B", "cultivar")
    C = Symbol("C", "region")
    D = Symbol("D", "dname")
    E = Symbol("E", "price")
    F = Symbol("F", "qty")
    G = Symbol("G", "bname")
    H = Symbol("H", "address")

    fds = {
        FunctionalDependency(A, {B, C}),
        FunctionalDependency({B, C}, A),
        FunctionalDependency({A, D}, E),
        FunctionalDependency({B, C, D}, E),
        FunctionalDependency(G, H),
        FunctionalDependency({A, D, G}, F),
        FunctionalDependency({B, C, D, G}, F)
    }

    print("Initial fds:")
    for fd in fds:
        print(fd.otherrep())
    print()

    print("Minimal cover:")
    minco = canonical_cover(fds)
    for i in minco:
        print(i.otherrep())

def check_subset_clsr():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")

    fds = {
        FunctionalDependency({A, B}, C),
        FunctionalDependency(C, D),
        FunctionalDependency(D, A)
    }

    res = all_subset_closures({A, B, C, D}, fds)
    for i in res.keys():
        print(f"{str(i).replace('frozenset(', '').replace(')', '')}+ = {res[i]}")

def tut_q_2():
    A = Symbol("A")
    B = Symbol("B")
    C = Symbol("C")
    D = Symbol("D")
    E = Symbol("E")

    fds = {
        FunctionalDependency(A, E),
        FunctionalDependency({A, B}, D),
        FunctionalDependency({C, D}, {A, E}),
        FunctionalDependency(E, B),
        FunctionalDependency(E, D)
    }

    res = check_bcnf_quick({A, B, C, D, E}, fds)
    print(res)

check_keys()
