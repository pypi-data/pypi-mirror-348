from itertools import combinations

#########################
### Class Definitions ###
#########################
class Symbol:
    """
    A class for the smallest element of Functional Dependency logic. Use this to represent relation attributes.
    Name should be unique: Two Symbols with the same `name` will return `True` when checked with equality `==`.
    Other comparisons are also done by `name`.

    Attributes:
        name (str): Name of the attribute/symbol. This is the main representation.
        desc (str, optional): Alternative descriptor, used with `Symbol::otherrep`
    """

    def __init__(self, name: str, desc: str = "") -> None:
        """
        Creates a new `Symbol` with a name and description.

        Args:
            name (str): Attribute name. Should be unique for the `Symbol`.
            desc (str, optional): Attribute description.
        """

        self.name: str = name
        self.description: str = desc if len(desc) != 0 else name
    
    def __eq__(self, value: object) -> bool:
        if self is value:
            return True
        if isinstance(value, Symbol) and value.name == self.name:
            return True
        return False

    def __ne__(self, value: object) -> bool:
        if self is value:
            return False
        if isinstance(value, Symbol) and value.name == self.name:
            return False
        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Symbol):
            raise TypeError("'<' not supported between instances of 'Symbol' and " + str(type(other)))
        return self.name < other.name

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Symbol):
            raise TypeError("'<=' not supported between instances of 'Symbol' and " + str(type(other)))
        return self.name <= other.name
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Symbol):
            raise TypeError("'>' not supported between instances of 'Symbol' and " + str(type(other)))
        return self.name > other.name
    
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Symbol):
            raise TypeError("'>=' not supported between instances of 'Symbol' and " + str(type(other)))
        return self.name >= other.name
    
    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def otherrep(self) -> str:
        """Alternative representation of the `Symbol` using its description."""

        return self.description

class FunctionalDependency:
    """
    A class to represent a functional dependency (FD) between two sets of attributes.
    Two FDs are equal if their LHS (`fro`) are equal and their RHS (`to`) are equal.

    Attributes:
        fro (set[Symbol]): Set of attributes that determine another set of attributes.
        to (set[Symbol]): Set of attributes that is determined by `fro`.
        lhs (set[Symbol]): Alias for `fro`.
        rhs (set[Symbol]): Alias for `to`.
    """

    def __init__(self, fro: Symbol | set[Symbol], to: Symbol | set[Symbol]) -> None:
        """
        Creates a new `FunctionalDependency` from and to the given `Symbol(s)`.

        Args:
            fro (Symbol or set[Symbol]): Left-Hand Side of the dependency.
            to (Symbol or set[Symbol]): Right-Hand Side of the dependency.
        
        Examples:
            Assuming `Symbol`s A and B are created:
            >>> A = Symbol("A")
            >>> B = Symbol("B")

            >>> fd1 = FunctionalDependency(A, B)
            A --> B

            >>> fd2 = FunctionalDependency({A, B}, B)
            AB --> B

            >>> fd2 = FunctionalDependency(B, {A, B})
            B --> AB

            >>> fd3 = FunctionalDependency({A}, {B})
            A --> B
        """

        if not isinstance(fro, set):
            self.fro: set[Symbol] = {fro}
        else:
            self.fro: set[Symbol] = fro
        if not isinstance(to, set):
            self.to: set[Symbol] = {to}
        else:
            self.to: set[Symbol] = to
    
    @property
    def lhs(self):
        return self.fro
    
    @property
    def rhs(self):
        return self.to
    
    def __eq__(self, value: object) -> bool:
        if self is value:
            return True
        if isinstance(value, FunctionalDependency) and value.fro == self.fro and value.to == self.to:
            return True
        return False

    def __hash__(self) -> int:
        out = 0
        for fro_attr in self.fro:
            out += fro_attr.__hash__()
        for to_attr in self.to:
            out += to_attr.__hash__()
        return out

    def __str__(self) -> str:
        out = ""
        for i in sorted(self.fro):
            out += str(i)
        out += " --> "
        for i in sorted(self.to):
            out += str(i)
        return out
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def otherrep(self) -> str:
        """Alternative representation of the FD using `Symbol::otherrep`."""

        out = "{"
        out += ", ".join(i.otherrep() for i in self.fro)
        out += "} --> {"
        out += ", ".join(i.otherrep() for i in self.to)
        out += "}"
        return out


##########################
### Armstrong's Axioms ###
##########################
def get_reflexive(lhs_attrs: Symbol | set[Symbol]) -> set[FunctionalDependency]:
    """
    Gets all FDs derived from Armstrong's Axiom of Reflexivity.

    Args:
        lhs_attrs (Symbol or set[Symbol]): Attribute(s) to get reflexive FDs from. This set will appear on the LHS of all returned FDs.
    
    Returns:
        set[FunctionalDependency]: All derived Functional Dependencies.
    
    Raises:
        TypeError: If the function encounters anything in `lhs_attrs` that is not a `Symbol`.
    
    Examples:
        Given attributes `ABC`, it can determine any subset of `ABC`.
        >>> get_reflexive({A, B})
        {AB --> A, AB --> B, AB --> AB}
    """

    if isinstance(lhs_attrs, set):
        for i in lhs_attrs:
            if not isinstance(i, Symbol): # type: ignore
                raise TypeError("Only Symbols allowed as input.")
        lhs_attrs = lhs_attrs.copy()
    elif isinstance(lhs_attrs, Symbol): # type: ignore
        lhs_attrs = {lhs_attrs}
    else:
        raise TypeError("Only Symbols allowed as input.")
    output: set[FunctionalDependency] = set()
    for L in range(1, len(lhs_attrs) + 1):
        for rhs in combinations(lhs_attrs, L):
            output.add(FunctionalDependency(lhs_attrs, set(rhs)))
    
    return output

def get_augmented(fds: FunctionalDependency | set[FunctionalDependency], others: Symbol | set[Symbol]) -> set[FunctionalDependency]:
    """
    Gets all FDs derived from Armstrong's Axiom of Augmentation.

    Args:
        fds (FunctionalDependency or set[FunctionalDependency]): Set of dependencies to augment.
        others (Symbol or set[Symbol]): `Symbol`s to augment `fds` with.
    
    Returns:
        set[FunctionalDependency]: Derived Functional Dependencies, excluding the original(s).
    
    Raises:
        TypeError: If the function encounters invalid types.
    
    Example:
        Given FD `A --> B` returns `Ax --> Bx` for all `x` combinations in `others`.
    """

    if isinstance(fds, set):
        fds = fds.copy()
    elif isinstance(fds, FunctionalDependency): # type: ignore
        fds = {fds}
    else:
        raise TypeError("`fds` is of an invalid type.")
    
    if isinstance(others, set):
        for o in others:
            if not isinstance(o, Symbol): # type: ignore
                raise TypeError("`others` contains type other than Symbol: " + str(o) + " of type " + str(type(o)))
        others = others.copy()
    elif isinstance(others, Symbol): # type: ignore
        others = {others}
    else:
        raise TypeError("`others` is on an invalid type.")
    
    output: set[FunctionalDependency] = set()
    for fd in fds:
        if not isinstance(fd, FunctionalDependency): # type: ignore
            raise TypeError("`fds` contains type other than FunctionalDependency: " + str(fd) + " of type " + str(type(fd)))
        for L in range(1, len(others) + 1):
            for comb in combinations(others, L):
                frocpy = fd.fro.copy()
                tocpy = fd.to.copy()
                for item in comb:
                    frocpy.add(item)
                    tocpy.add(item)
                output.add(FunctionalDependency(frocpy, tocpy))
    return output

def get_transitive(fds: set[FunctionalDependency]) -> set[FunctionalDependency]:
    """
    Gets all FDs derived from Armstrong's Axiom of Transitivity.

    Args:
        fds (set[FunctionalDependency]): Set of dependencies to check.
    
    Returns:
        set[FunctionalDependency]: Derived dependencies, not including the inputs.
    
    Raises:
        TypeError: If any type other than `FunctionalDependency` encountered in the input.
    
    Example:
        Given FDs `A --> B` and `B --> C`, returns `A --> C`.
    """

    for i in fds:
        if not isinstance(i, FunctionalDependency): # type: ignore
            raise TypeError("`fds` contains type other than FunctionalDependency: " + str(i) + " of type " + str(type(i)))
    if len(fds) <= 1:
        return set()
    output: set[FunctionalDependency] = set()
    checklist = list(fds)
    seen = set(fds)
    while checklist:
        fromfd = checklist.pop()
        for tofd in list(seen):
            if fromfd == tofd:
                continue
            if fromfd.to & tofd.fro:
                newfd = FunctionalDependency(fromfd.fro, tofd.to)
                if newfd not in seen:
                    output.add(newfd)
                    checklist.append(newfd)
                    seen.add(newfd)
    return output

def make_decomposed(fds: FunctionalDependency | set[FunctionalDependency]) -> set[FunctionalDependency]:
    """
    Returns a decomposed set of FDs from the input.

    Args:
        fds (FunctionalDependency or set[FunctionalDependency]): Set of FDs to decompose.
    
    Returns:
        set[FunctionalDependency]: Decomposed FDs, as well as any from the input that were already in a decomposed form.
            Does not include FDs that were identified as non-decomposed.
    
    Raises:
        TypeError: If any type other than `FunctionalDependency` encountered in the input.
    
    Examples:
        >>> make_decomposed({A --> B, B --> CD})
        {A --> B, B --> C, B --> D}
    """

    output: set[FunctionalDependency] = set()
    if isinstance(fds, FunctionalDependency):
        fds = {fds}
    elif not isinstance(fds, set): # type: ignore
        raise TypeError("`fds` is of invalid type.")
    
    for fd in fds:
        if not isinstance(fd, FunctionalDependency): # type: ignore
            raise TypeError("`fds` contains type other than FunctionalDependency: " + str(fd) + " of type " + str(type(fd)))
        if len(fd.to) == 1:
            output.add(fd)
        else:
            for attr in fd.to:
                output.add(FunctionalDependency(fd.fro, attr))
    return output

def make_union(fds: set[FunctionalDependency]) -> set[FunctionalDependency]:
    """
    Returns a set of FDs with the Rule of Union applied.

    Args:
        fds (FunctionalDependency or set[FunctionalDependency]): Set of FDs to apply union to.
    
    Returns:
        set[FunctionalDependency]: All FDs that were either\n
            a) Were not used in any union (already in most combined form).\n
            b) Result of a union.\n
            Does not include FDs that produced a new FD by union.
    
    Raises:
        TypeError: If `fds` contains a type other than FunctionalDependency.
    
    Examples:
        >>> make_union({A --> B, A --> C, B --> D})
        {B --> D, A --> BC}
    """

    if len(fds) <= 1:
        return fds
    unique_lhs: set[frozenset[Symbol]] = set()
    output: set[FunctionalDependency] = set()
    for fd in fds:
        unique_lhs.add(frozenset(fd.lhs))
    for lhs in unique_lhs:
        new_fd: FunctionalDependency = FunctionalDependency(set(lhs), set())
        for fd in fds:
            if frozenset(fd.lhs) != lhs: continue
            for att in fd.rhs:
                new_fd.rhs.add(att)
        output.add(new_fd)

    return output


###############
### Closure ###
###############
def compute_closure(attrs: set[Symbol], fds: set[FunctionalDependency]) -> set[Symbol]:
    """
    Calculates the closure of a set of attributes with respect to the given FDs.
    The closure is defined as the set of attributes that can be determined from the input attributes using the FDs.

    Args:
        attrs (set[Symbol]): The set of :class:`~fdfuncs.Symbol`\s to compute closure for.
        fds (set[FunctionalDependency]): FDs to use for closure.
    Returns:
        set[Symbol] The closure.
    Raises:
        TypeError: If input sets contain unexpected types.
    """

    for att in attrs:
        if not isinstance(att, Symbol): # type: ignore
            raise TypeError("`attrs` contains type other than Symbol: " + str(att) + " of type " + str(type(att)))
    for fd in fds:
        if not isinstance(fd, FunctionalDependency): # type: ignore
            raise TypeError("`fds` contains type other than FunctionalDependency: " + str(fd) + " of type " + str(type(fd)))

    activated = set(attrs.copy())
    remaining_fds = fds.copy()
    while True:
        num_activated = 0
        to_remove: set[FunctionalDependency] = set()
        for fd in remaining_fds:
            if fd.fro <= activated:
                for attr in fd.to:
                    activated.add(attr)
                    num_activated += 1
                to_remove.add(fd)
        for fd in to_remove:
            remaining_fds.remove(fd)
        if (num_activated == 0 or len(remaining_fds) == 0):
            break
    return activated


def minimal_cover(fds: set[FunctionalDependency]) -> set[FunctionalDependency]:
    """
    Calculates the minimal cover / basis of a set of FDs.

    Args:
        fds (set[FunctionalDependency]): Initial set of FDs.
    Returns:
        set[FunctionalDependency]: Minimal basis of input FDs.
    Raises:
        TypeError: Via `make_decomposed`
    """

    # 1. Decompose
    working_fds: set[FunctionalDependency] = make_decomposed(fds)
    # print(working_fds)

    # 2. Clean LHS for redundant
    fds_to_replace: set[FunctionalDependency] = set()
    replacement_fds: set[FunctionalDependency] = set()
    for fd in working_fds:
        if len(fd.fro) == 1: continue
        redundant_atts: set[Symbol] = set()
        for att in fd.fro:
            other_atts = fd.fro.copy()
            other_atts.remove(att)
            other_fds = working_fds.copy()
            other_fds.remove(fd)
            other_att_closure = compute_closure(other_atts, other_fds)
            if att in other_att_closure:
                redundant_atts.add(att)
        
        # Mark reduns
        new_fd: FunctionalDependency = FunctionalDependency(fd.fro.copy(), fd.to.copy())
        for att in redundant_atts:
            new_fd.fro.remove(att)
        if fd != new_fd:
            fds_to_replace.add(fd)
            replacement_fds.add(new_fd)
    
    # Replace marked LHS attrs
    for fd in fds_to_replace:
        working_fds.remove(fd)
    for fd in replacement_fds:
        working_fds.add(fd)
    # print(working_fds)

    # 3. Remove redun FDs
    final_fds: set[FunctionalDependency] = working_fds.copy()
    for fd in working_fds:
        final_fds.remove(fd)
        non_fd_closure = compute_closure(fd.fro, final_fds)
        if not((fd.to & non_fd_closure) == fd.to): # ==> Not redundant, add back
            final_fds.add(fd)

    return final_fds

def canonical_cover(fds: set[FunctionalDependency], minimum_cover: set[FunctionalDependency] = None) -> set[FunctionalDependency]: # type: ignore
    """
    Calculates the canonical cover / basis of a set of FDs.
    Note: Canonical cover is equivalent to the minimal cover with the Union Rule applied.

    Args:
        fds (set[FunctionalDependency]): Initial set of FDs.
    Returns:
        set[FunctionalDependency]: Canonical basis of input FDs.
    Raises:
        TypeError: Via `minimal_cover`
    """

    if minimum_cover is None: # type: ignore
        minimum_cover = minimal_cover(fds)
    return make_union(minimum_cover)

####################
### Normal Forms ###
####################

def all_subset_closures(attrs: set[Symbol], fds: set[FunctionalDependency]) -> dict[frozenset[Symbol], set[Symbol]]:
    """
    Calculates the closure for all attribute subsets.

    Args:
        attrs (set[Symbol]): Full set of attributes to compute on.
        fds (set[FunctionalDependency]): Set of FDs to calculate closure using.
    Returns:
        dict[frozenset[Symbol], set[Symbol]]: Dictionary containing closure of every attribute subset combination.\n
            Note that the key is a frozenset due to hashing limitations.
    Raises:
        TypeError: If input sets contain unexpected types.
    """

    for att in attrs:
        if not isinstance(att, Symbol): # type: ignore
            raise TypeError("`attrs` contains type other than Symbol: " + str(att) + " of type " + str(type(att)))
    for fd in fds:
        if not isinstance(fd, FunctionalDependency): # type: ignore
            raise TypeError("`fds` contains type other than FunctionalDependency: " + str(fd) + " of type " + str(type(fd)))

    out: dict[frozenset[Symbol], set[Symbol]] = dict()
    for L in range(1, len(attrs) + 1):
        for comb in combinations(attrs, L):
            comb = frozenset(comb)
            if out.get(comb) != None:
                continue
            out[comb] = compute_closure(comb, fds) # type: ignore
    
    return out

def find_superkeys(attrs: set[Symbol], fds: set[FunctionalDependency]) -> set[frozenset[Symbol]]:
    """
    Finds all superkeys of a relation.
    
    Args:
        attrs (set[Symbol]): Set of attributes in the relation.
        fds (set[FunctionalDependency]): Set of FDs of the relation.
    Returns:
        set[frozenset[Symbol]]: Set containing a list of all attribute combinations that act as superkeys for the relation.\n
            Note that it must be a set of frozensets due to hashing limitations.
    Raises:
        TypeError: If input sets contain unexpected types.
    """

    for att in attrs:
        if not isinstance(att, Symbol): # type: ignore
            raise TypeError("`attrs` contains type other than Symbol: " + str(att) + " of type " + str(type(att)))
    for fd in fds:
        if not isinstance(fd, FunctionalDependency): # type: ignore
            raise TypeError("`fds` contains type other than FunctionalDependency: " + str(fd) + " of type " + str(type(fd)))

    all_closures: dict[frozenset[Symbol], set[Symbol]] = all_subset_closures(attrs, fds)
    keys_found: set[frozenset[Symbol]] = set()
    for comb in all_closures.keys():
        if all_closures[comb] & attrs == attrs:
            keys_found.add(comb)
    return keys_found

def find_keys(superkeys: set[frozenset[Symbol]] = None, attrs: set[Symbol] = None, fds: set[FunctionalDependency] = None) -> set[frozenset[Symbol]]: # type: ignore
    """
    Finds all candidate keys (or just keys) for a relation. 
    This is a set of minimal superkeys, i.e. removing an attribute from any subset in this list makes it no longer a key.\n
    **IMPORTANT**: Either `superkeys` or both of (`attrs`, `fds`) must be provided. If `superkeys` is provided, other arguments 
    will be ignored.

    Args:
        superkeys (set[frozenset[Symbol]], optional): A set of superkeys for the relation. If not provided, superkeys will first be computed from `attrs` and `fds`.
        attrs (set[Symbol], optional): Set of attributes in the relation.
        fds (set[FunctionalDependency]): Set of FDs of the relation.
    Returns:
        set[frozenset[Symbol]]: Set containing a list of all attribute combinations that act as candidate keys for the relation. Note that it must be a set of frozensets due to hashing limitations.
    Raises:
        TypeError: Via `find_superkeys`.
    """

    if superkeys is None and (attrs is None or fds is None): # type: ignore
        raise ValueError("At least on of (superkeys) or (attrs and fds) must be provided")
    if superkeys is None: # type: ignore
        superkeys = find_superkeys(attrs, fds)
    superkeys: list[frozenset[Symbol]] = sorted(superkeys, key=len)
    keys_found: list[frozenset[Symbol]] = superkeys.copy()
    i = 0
    while True:
        if i >= len(keys_found): break
        to_check: frozenset[Symbol] = keys_found[i]
        to_remove: set[frozenset[Symbol]] = set()
        for j in range(i + 1, len(keys_found)):
            if to_check & keys_found[j] == to_check:
                # keys_found[j] fully encompasses i and has extra: remove it
                to_remove.add(keys_found[j])
        
        for r in to_remove:
            keys_found.remove(r)
        i += 1
    return set(keys_found)
    
def non_trivial_n_decomposed(attrs: set[Symbol], fds: set[FunctionalDependency]) -> set[FunctionalDependency]:
    """
    Returns all 'non-trivial and decomposed' Functional Dependencies:\n
    * Non-Trivial: If a Symbol exists on the LHS of an FD, it will not appear on the RHS.
    * Decomposed: All RHS will only contain a single Symbol.

    Any FDs not in the initial arguments will be derived.
    
    Args:
        attrs (set[Symbol]): Set of attributes in the relation.
        fds (set[FunctionalDependency]): Set of FDs of the relation.
    Returns:
        set[FunctionalDependency]: Set of all non-trivial and decomposed FDs.
    Raises:
        TypeError: Via `all_subset_closures`.
    """

    subsets_clsrs = all_subset_closures(attrs, fds)
    out: set[FunctionalDependency] = set()
    for key in subsets_clsrs.keys():
        for right_attr in subsets_clsrs[key]:
            if right_attr in key:
                continue
            out.add(FunctionalDependency(set(key), right_attr))
    
    return out

# def check_bcnf_quick(attrs: set[Symbol], fds: set[FunctionalDependency]) -> tuple[bool, FunctionalDependency]:
#     subsets_clsrs = all_subset_closures(attrs, fds)
#     for key in subsets_clsrs.keys():
#         if subsets_clsrs[key] & key == subsets_clsrs[key]:
#             continue
#         elif subsets_clsrs[key] & attrs == attrs:
#             continue
#         else:
#             return False, FunctionalDependency(set(key), subsets_clsrs[key])
#     return True, None # type: ignore

if __name__ == "__main__":
    print("fd_solver: Nothing to do here!")
    exit()
