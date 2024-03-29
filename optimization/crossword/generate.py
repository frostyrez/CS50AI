import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            self.domains[var] = {word for word in self.domains[var] \
                                  if len(word) == var.length}


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        rev = False # revision made?
        i,j = self.crossword.overlaps[x,y]
        for xword in self.domains[x].copy():
            flag = 1 # if flag is still 1 after y is done iterating, remove
            for yword in self.domains[y].copy():
                if xword[i] == yword[j]:
                    flag = 0 # safe
                    break
            if flag == 1:
                self.domains[x].remove(xword)
                rev = True
        return rev



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = self.get_couples()
        while queue:
            x,y = queue[0]
            queue.remove(queue[0])
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                other_neighs = self.other_neighbors(x,y)
                for neighbor in other_neighs:
                    queue.append((neighbor,x))
        return True
    

    def get_couples(self):
        couples = [c for c in self.crossword.overlaps if self.crossword.overlaps[c]]
        tracker = set()
        to_remove = []
        for i in range(len(couples)):
            x,y = couples[i]
            if (y,x) in tracker:
                to_remove.append((x,y))
            else:
                tracker.add((x,y))
        couples = [x for x in couples if x not in to_remove]
        return couples


    def other_neighbors(self,x,y):
        neighs = [k for k in self.crossword.overlaps if x in k and self.crossword.overlaps[k]]
        # put x into left
        for n in range(len(neighs)):
            if neighs[n][1] == x:
                neighs[n] = (neighs[n][1],neighs[n][0])
        return [n[1] for n in neighs if n[1] != y]
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check variables
        if self.crossword.variables - set(assignment):
            return False
        # Check words
        for var in assignment:
            if not assignment[var]:
                return False
        return True
        


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # All values distinct
        words = [w for w in assignment.values() if w]
        if len(set(words)) != len(words):
            return False
        
        
        # All values correct length
        for var in assignment:
            if assignment[var] and len(assignment[var]) != var.length:
                return False

        # All overlaps consistent
        for overlap in self.get_couples():
            x,y = overlap
            xloc,yloc = self.crossword.overlaps[overlap]
            if (assignment[x] and assignment[y]) and assignment[x][xloc] != assignment[y][yloc]:
                return False
            
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Populate
        var_dict = dict.fromkeys(self.domains[var],0)
        for var_word in var_dict:
            neighbors = self.all_neighbors(var)
            for neighbor in neighbors:
                i,j = self.crossword.overlaps[(var,neighbor)]
                for neigh_word in self.domains[neighbor]:
                    if var_word[i] != neigh_word[j]:
                        var_dict[var_word] += 1
        # Sort
        var_dict = {k: v for k, v in sorted(var_dict.items(), key=lambda item: item[1])}
        return list(var_dict.keys())
            

    def all_neighbors(self,x):
        neighs = [k for k in self.crossword.overlaps if x in k and self.crossword.overlaps[k]]
        # put x into left
        for n in range(len(neighs)):
            if neighs[n][1] == x:
                neighs[n] = (neighs[n][1],neighs[n][0])
        return [n[1] for n in neighs]
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
    
        # Only heur 1:
        var_dict = {k: 0 for (k,v) in assignment.items() if v is None}
        for var in var_dict:
            var_dict[var] = len(self.domains[var])

        # Sort
        var_dict = {k: v for k, v in sorted(var_dict.items(), key=lambda item: item[1])}
        return list(var_dict.keys())[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        elif not assignment: # is empty
            assignment = dict.fromkeys(self.domains,None)
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            test_assignment = {k: v for k, v in assignment.items()}
            test_assignment[var] = value
            if self.consistent(test_assignment):
                assignment[var] = value
                saved_domains = {k: v for k, v in self.domains.items()}
                if self.ac3():
                    self.ac3()
                result = self.backtrack(assignment)
                if result:
                    return result
                self.domains = {k: v for k, v in saved_domains.items()}
                self.domains[var] = None
        return None
                

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
