import re, sys
from itertools import product

"""
Script for parsing SPLOT SXFM files into CNF files.
"""
class CSPNode:
    def __init__(self, node_input_id, node_id, node_type, node_name, node_parent, \
      node_ranges=None):
        self.input_id = node_input_id
        self.id = node_id
        self.type = node_type
        self.child_type = None
        self.name = node_name
        self.parent = node_parent
        self.children = []
        self.ranges = node_ranges

    def __str__(self):
        result = ""
        result += "  Node " + str(self.id) + ":\n"
        result += "   name=" + str(self.name) + "\n"
        result += "   type=" + str(self.type) + "\n"
        result += "   child_type=" + str(self.child_type) + "\n"
        result += "   parent=" + str(self.parent.name if self.parent else "None") + "\n"
        result += "   children=" + ",".join([child.name for child in self.children]) + "\n"
        return result

    def set_child_type(self, child_type):
        self.child_type = child_type

    def add_child(self, node_child):
        self.children.append(node_child)

class CSPTree:
    def __init__(self):
        self.root = None
        self.nodes = []
        self.crosstree_constraints = []

    def __str__(self):
        result = ""
        result += "CSP Tree:\n"
        result += " Nodes:\n"
        for node in self.nodes:
            result += str(node)
        result += " Constraints:\n"
        for constraint in self.crosstree_constraints:
            result += constraint
        return result

    def set_root(self, root):
        self.root = root

    def add(self, node):
        self.nodes.append(node)

    def add_crosstree_constraint(self, constraint):
        self.crosstree_constraints.append(constraint)

    def remove_group_nodes(self):
        """
        Remove the auxiliary group nodes that SPLOT adds to the CSP.
        """
        for node in self.nodes:
            if node.id == None:
                node.parent.children = node.children
                node.parent.child_type = node.type
                for child in node.children:
                    child.parent = node.parent
        self.nodes = [node for node in self.nodes if node.id is not None]

    def compute_children(self):
        for node in self.nodes:
            if node.parent != None:
                node.parent.add_child(node)

    def reassign_constraint_ids(self):
        new_constraints = []
        for constraint in self.crosstree_constraints:
            ids = constraint.replace("~", "").split("or")
            ids = [node_id.strip() for node_id in ids]
            new_constraint = constraint
            for node_id, node in product(ids, self.nodes):
                if node_id == node.input_id:
                    new_constraint = new_constraint.replace(node_id, node.id)
            new_constraints.append(new_constraint)
        self.crosstree_constraints = new_constraints

    def cleanup(self):
        self.compute_children()
        self.remove_group_nodes()
        self.reassign_constraint_ids()

    @staticmethod
    def cnf_mandatory(parent, child):
        return "~%s || %s\n%s || ~%s\n" % (parent.id, child.id, parent.id, child.id)

    @staticmethod
    def cnf_optional(parent, child):
        return "%s || ~%s\n" % (parent.id, child.id)

    @staticmethod
    def cnf_children_or(parent, children):
        result = ""
        for child in children:
            result += CSPTree.cnf_optional(parent, child)
        result += "~" + parent.id + " || " + " || ".join([child.id for child in children]) + "\n"
        return result

    @staticmethod
    def cnf_children_xor(parent, children):
        result = ""
        for child in children:
            result += parent.id + " || ~" + child.id + "\n"
        result += "~" + parent.id + " || " + " || ".join([child.id for child in children]) + "\n"
        result += " || ".join(["~" + child.id for child in children]) + "\n"
        for index, child in enumerate(children):
            if index == 0:
                before = ""
            else:
                before = " || ".join(["~" + _.id for _ in children[:index]]) + " || "
            if index < len(children)-1:
                after = " || " + " || ".join(["~" + _.id for _ in children[index+1:]]) + "\n"
            else:
                after = "\n"
            result += before + child.id + after
        return result

    @staticmethod
    def sat_mandatory(parent, child):
        return "%s <-> %s\n" % (parent.id, child.id)

    @staticmethod
    def sat_optional(parent, child):
        return "%s -> %s\n" % (child.id, parent.id)

    @staticmethod
    def sat_children_or(parent, children):
        return "%s <-> OR(%s)\n" % (parent.id, ",".join([child.id for child in children]))

    @staticmethod
    def sat_children_xor(parent, children):
        return "%s <-> XOR(%s)\n" % (parent.id, ",".join([child.id for child in children]))

    def write_to_cnf(self, filename):
        """
        Write a SAT in Conjunctive Normal Form.
        """
        with open(filename, "w") as outfile:
            for node in self.nodes:
                if node.child_type == "or":
                    outfile.write(CSPTree.cnf_children_or(node, node.children))
                elif node.child_type == "xor":
                    outfile.write(CSPTree.cnf_children_xor(node, node.children))
                else:
                    for child in node.children:
                        if child.type == "o":
                            outfile.write(CSPTree.cnf_optional(node, child))
                        elif child.type == "m":
                            outfile.write(CSPTree.cnf_mandatory(node, child))
            for constraint in self.crosstree_constraints:
                outfile.write(constraint.replace("or", "||"))

    def write_to_sat(self, filename):
        """
        Write directly to SAT (and, if, iff, etc.)
        """
        with open(filename, "w") as outfile:
            for node in self.nodes:
                if node.child_type == "or":
                    outfile.write(CSPTree.sat_children_or(node, node.children))
                elif node.child_type == "xor":
                    outfile.write(CSPTree.sat_children_xor(node, node.children))
                else:
                    for child in node.children:
                        if child.type == "o":
                            outfile.write(CSPTree.sat_optional(node, child))
                        elif child.type == "m":
                            outfile.write(CSPTree.sat_mandatory(node, child))
            for constraint in self.crosstree_constraints:
                outfile.write(constraint.replace("or", "||"))

    def write_name_lookup(self, filename):
        """
        Write a CSV file with the node names, node ID, and our internal ID.
        """
        with open(filename, "w") as outfile:
            for node in self.nodes:
                outfile.write("%s\t%s\t%s\n" % (node.name, node.input_id, node.id))

class ID_Generator:
    def __init__(self, variable):
        self.start = 0
        self.variable = variable

    def generate(self):
        self.start += 1
        return "%s%d" % (self.variable, self.start)

def read_sxfm(sxfm_filename):
    """
    Reads in a SPLOT product line model in SXFM format.
    Outputs a CSPTree.
    """
    ROOT_PATTERN = re.compile("\s*:r\s+[\s\w]*\([\s\w]+\)\s*")
    STANDARD_PATTERN = re.compile("\s*:[om]\s+[\s\w]*\([\s\w]+\)\s*")
    GROUP_PATTERN = re.compile("\s*:g\s+\([\s\w]+\)\s+\[\s*\d\s*,\s*[\d*\*]\s*\]\s*")
    CHILD_PATTERN = re.compile("\s*:[\s\w]+\([\s\w]+\)\s*")
    tree = CSPTree()
    ids = ID_Generator(variable="x")

    with open(sxfm_filename) as infile:
        # Till we hit the feature tree, keep reading
        line = infile.readline()
        while "<feature_tree>" not in line:
            line = infile.readline()

        # These lines are the feature tree
        line = infile.readline()
        last_num_tabs = -1
        node = None
        stack = []
        while "</feature_tree>" not in line:
            num_tabs = line.count("\t")
            for _ in xrange(last_num_tabs - num_tabs + 1):
                stack.pop()
            last_num_tabs = num_tabs

            if ROOT_PATTERN.findall(line):
                tmp = line[:line.index("(")].strip().split()
                node_type, node_name = tmp[0].replace(":",""), " ".join(tmp[1:])
                node_id = line[line.index("(")+1:line.index(")")]
                node = CSPNode(node_input_id=node_id,
                                node_id=ids.generate(),
                                node_type=node_type,
                                node_name=node_name,
                                node_parent=None)
                tree.set_root(node)
            elif STANDARD_PATTERN.findall(line):
                tmp = line[:line.index("(")].strip().split()
                node_type, node_name = tmp[0].replace(":",""), " ".join(tmp[1:])
                node_id = line[line.index("(")+1:line.index(")")]
                node = CSPNode(node_input_id=node_id,
                                node_id=ids.generate(),
                                node_type=node_type,
                                node_name=node_name,
                                node_parent=stack[-1])
            elif GROUP_PATTERN.findall(line):
                tmp = line[:line.index("(")].strip().split()
                node_type, node_name = tmp[0], " ".join(tmp[1:])
                node_id = line[line.index("(")+1:line.index(")")]
                node_ranges = line[line.index("[")+1:line.index("]")].split(",")
                node_type = "or" if node_ranges[1]=="*" else "xor"
                node = CSPNode(node_input_id=node_id,
                                node_id = None,
                                node_type=node_type,
                                node_name=node_name,
                                node_parent=stack[-1],
                                node_ranges=node_ranges)
            elif CHILD_PATTERN.findall(line):
                node_name = line[line.index(":")+1:line.index("(")].strip()
                node_id = node_id = line[line.index("(")+1:line.index(")")]
                node = CSPNode(node_input_id=node_id,
                               node_id=ids.generate(),
                               node_type="child",
                               node_name=node_name,
                               node_parent=stack[-1])

            stack.append(node)
            tree.add(node)
            line = infile.readline()

        # Then keep reading till we hit the constraints
        while "<constraints>" not in line:
            line = infile.readline()

        # These lines are the constraints
        line = infile.readline()
        while "</constraints>" not in line:
            line = line[line.index(":")+1:]
            tree.add_crosstree_constraint(line)
            line = infile.readline()

        # Do some post processing to clean up the tree
        tree.cleanup()
        return tree

def write_cnf(clauses, cnf_filename):
    with open(cnf_filename, "w") as outfile:
        outfile.write(clauses)
    print "Wrote CNF clauses to", cnf_filename

def write_cnf_name_lookup(name_lookup, filename):
    with open(filename, "w") as outfile:
        for key in name_lookup:
            outfile.write(key + " " + name_lookup[key] + "\n")
    print "Wrote CNF name-ID lookup to", filename

if __name__=="__main__":
    sxfm_filename = sys.argv[1]
    tree = read_sxfm(sxfm_filename)
    print tree
    tree.write_to_cnf(sxfm_filename.replace("xml", "cnf"))
    tree.write_to_sat(sxfm_filename.replace("xml", "sat"))
    tree.write_name_lookup(sxfm_filename.replace("xml", "csv"))

    # clauses, name_lookup = parse_sxfm_to_cnf(sxfm_filename)
    # print "Total literals: ", len(name_lookup)
    # print "Total clauses: ", clauses.count("\n")
    # write_cnf(clauses, cnf_filename)
    # write_cnf_name_lookup(name_lookup, cnf_filename + "_names")
