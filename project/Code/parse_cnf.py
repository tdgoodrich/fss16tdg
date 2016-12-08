import sys
import networkx as nx

"""
Script for converting CNF files into k- and 2-posiforms, and QUBOs.
"""

class ID_Generator:
    def __init__(self, variable):
        self.start = 0
        self.variable = variable

    def generate(self):
        self.start += 1
        return "%s%d" % (self.variable, self.start)

def negate_literals(literals):
    """
    Given a list of literals, negate them.
    """
    return ["~" + literal if "~" not in literal else literal.replace("~", "") for literal in literals]

def convert_cnf_posiform(cnf_clauses):
    """
    Accepts a list of CNF clauses and outputs a list of posiform terms.
    """
    posiform_terms = []
    for clause in cnf_clauses:
        clause = " * ".join(negate_literals(clause.split(" || ")))
        #parity = clause.count("~") % 2
        #clause = clause.replace("~", "")
        #if parity == 1:
        #    clause = "-1 * " + clause
        #posiform_terms.append(clause)

    return posiform_terms

def recursive_pairing(term, ids):
    """
    Given a list of the literals in a term, pair them up recursively and output
    the 2-posiform terms built.
    """

    if len(term) == 0:
        return []
    elif len(term) == 1:
        return "Foo"
    elif len(term) == 2:
        return ["%s * %s" % (term[0], term[1])]

    pairings = [(term[i], term[i+1]) for i in xrange(0, len(term)/2*2, 2)]
    recurse_list = []
    # If we had an odd number of variables, the last one will get carried
    # to the next computation
    if len(term)/2*2 != len(term):
        recurse_list.append(term[-1])

    output = []
    for pair in pairings:
        auxiliary = ids.generate()
        recurse_list.append(auxiliary)
        output.append("2 * %s * %s" % (pair[0], pair[1]))
        output.append("-4 * %s * %s" % (pair[0], auxiliary))
        output.append("-4 * %s * %s" % (pair[1], auxiliary))
        output.append("2 * %s" % pair[0])
        output.append("2 * %s" % pair[1])
        output.append("2 * %s" % auxiliary)
        #output.append("%s * %s - 2 * %s * %s - 2 * %s * %s + %s" % (pair[0], pair[1], pair[0], auxiliary, pair[1], auxiliary, auxiliary))
    output = recursive_pairing(recurse_list, ids) + output
    return output

def convert_posiform_two_posiform(posiform_terms):
    """
    Accepts a list of terms in posiform, then converts them
    to terms of at most two variables by introducing auxiliary variables.
    """
    ids = ID_Generator("z")
    two_posiform_terms = []
    for term in posiform_terms:
        if term.count("x") <= 2:
            two_posiform_terms.append(term)
        else:
            term_variables = [x for x in term.split(" * ") if "x" in x]
            new_terms = recursive_pairing(term_variables, ids)
            first_term = term.split(" *")[0]
            if "x" not in first_term:
                new_terms[0] = first_term + " * " + new_terms[0]
            two_posiform_terms += new_terms
    return two_posiform_terms


def convert_cnf_two_posiform(cnf_clauses):
    """
    Accepts a list of CNF clauses and converts them to 2-posiform directly.
    """
    ids = ID_Generator("z")
    two_posiform_terms = []
    for clause in cnf_clauses:
        clause_literals = clause.split(" || ")
        if clause.count("x") <= 2:
            clause = " * ".join(negate_literals(clause_literals))
            two_posiform_terms.append(clause)
        else:
            new_terms = recursive_pairing(clause_literals, ids)
            two_posiform_terms += new_terms
    return two_posiform_terms

def negative(literal):
    if "-" in literal:
        return literal.replace("-", "")
    else:
        return "-" + literal

def expand_term(term):
    """
    Expands and simplifies a term.
    """
    new_terms = []
    if len(term) == 3:
        constant, literal1, literal2 = term
        if "~" in literal1 and "~" in literal2:
            literal1 = literal1.replace("~", "")
            literal2 = literal2.replace("~", "")
            new_terms.append(constant)
            new_terms.append(negative(constant) + " * " + literal1)
            new_terms.append(negative(constant) + " * " + literal2)
            new_terms.append(constant + " * " + literal1 + " * " + literal2)
        elif "~" in literal1 and "~" not in literal2:
            literal1 = literal1.replace("~", "")
            new_terms.append(constant + " * " + literal2)
            new_terms.append(negative(constant) + " * " + literal1 + " * " + literal2)
        elif "~" not in literal1 and "~" in literal2:
            literal2 = literal2.replace("~", "")
            new_terms.append(constant + " * " + literal1)
            new_terms.append(negative(constant) + " * " + literal1 + " * " + literal2)
    elif len(term) == 2 and ("x" in term[0] or "z" in term[0]):
        literal1, literal2 = term
        if "~" in literal1 and "~" in literal2:
            literal1 = literal1.replace("~", "")
            literal2 = literal2.replace("~", "")
            new_terms.append("1")
            new_terms.append(literal1)
            new_terms.append(literal2)
            new_terms.append(literal1 + " * " + literal2)
        elif "~" in literal1 and "~" not in literal2:
            literal1 = literal1.replace("~", "")
            new_terms.append(literal2)
            new_terms.append("-1 * " + literal1 + " * " + literal2)
        elif "~" not in literal1 and "~" in literal2:
            literal2 = literal2.replace("~", "")
            new_terms.append(literal1)
            new_terms.append("-1 * " + literal1 + " * " + literal2)
    elif len(term) == 2:
        constant, literal1 = term
        if "~" in literal1:
            literal1 = literal1.replace("~", "")
            new_terms.append(constant)
            new_terms.append(negative(constant) + " * " + literal1)
        else:
            new_terms.append(" * ".join(term))
    else:
        new_terms.append(term[0])

    return new_terms

def convert_two_posiform_qubo(posiform):
    """
    Converts a list of two posiform terms into a QUBO.
    """
    qubo = []
    for term in posiform:
        term = term.split(" * ")
        qubo += expand_term(term)
    return qubo

def write_list(filename, lines):
    """
    Given a list of lines, write them.
    """
    with open(filename, "w") as outfile:
        for line in lines:
            outfile.write(line + "\n")

# Write something that reads QUBOs into an adjacency matrix
# Output some stats like #vertices, #edges, diameter
#
#
#
#

def formulate_graph(qubo):
    g = nx.Graph()
    for line in qubo:
        literals = line.split(" * ")
        if line.count("x") + line.count("z") == 2:
            # edge
            if len(literals) == 3:
                g.add_edge(literals[1], literals[2])
            else:
                g.add_edge(literals[0], literals[1])
        elif line.count("x") + line.count("z") == 2:
            # vertex
            if len(literals) == 2:
                g.add_vertex(literals[1])
            else:
                g.add_vertex(literals[0])
        else:
            # Constant, don't care for now
            pass
    try:
        v, e, d = g.order(), g.size(), nx.diameter(g)
        print "Vertices: ", v, " Edges: ", e, " Diameter: ", d
    except:
        print "Vertices: ", g.order(), " Edges: ", g.size()


if __name__=="__main__":
    # Read in the CNF file
    cnf_filename = sys.argv[1]
    cnf_clauses = []
    with open(cnf_filename, "r") as infile:
        for line in infile.readlines():
            cnf_clauses.append(line.replace("\n", ""))

    posiform = convert_cnf_two_posiform(cnf_clauses)
    write_list(cnf_filename.replace("cnf", "2posiform"), posiform)

    qubo = convert_two_posiform_qubo(posiform)
    write_list(cnf_filename.replace("cnf", "qubo"), qubo)
    formulate_graph(qubo)

    # posiform  = convert_cnf_posiform(cnf_clauses)
    # write_list(cnf_filename.replace("cnf", "posiform"), posiform)
    # two_posiform = convert_posiform_two_posiform(posiform)
