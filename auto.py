from equivalence import EquivalenceClass
from branching import main_automorphisms
from tree import aut_counter
from our_lib import factorial



def automorphism_main(equivalence_classes: "list[EquivalenceClass]") -> None:
    """
        Function that calculates #aut according to the most efficient algorithm for the given equivalence classes
        :param equivalence_classes:
    """

    for equivalence_class in equivalence_classes:

        if equivalence_class.hypercube:
            n = equivalence_class.hypercube_n
            equivalence_class.automorphisms = factorial(n) * 2**n
        elif equivalence_class.tree:
            equivalence_class.automorphisms = aut_counter(equivalence_class.tree_tree)
        else:
            main_automorphisms(equivalence_class)

        if equivalence_class.twins:
            equivalence_class.automorphisms *= equivalence_class.twins_factor
