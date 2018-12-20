import sympy as sp

# Add average_molar_mass attribute
# Make the sympy stuff happen in this class


class System(object):

    def __init__(self, balances):

        self.balances = balances
        self.info = {}
        self.equations = {}
        self.get_equations()

        self.unknowns = set()
        self.DoF = None
        self.solutions = None

        self.get_unknowns()
        self.get_dof()

    def update_balances(self, material):
        if material not in self.balances.keys():
            self.balances[material] = sp.S('0')

    def get_unknowns(self):
        for material, balance in self.balances.items():
            self.unknowns = self.unknowns.union(set(balance.atoms(sp.Symbol)))

    def get_dof(self):
        self.DoF = len(self.unknowns) - len(self.equations)
        self.solutions = None

        if self.DoF == 0:
            self.solve()

    def get_equations(self):
        self.equations = {**self.balances, **self.info}

    def check_info(self, info, equation):
        compatibility = 0
        info_unknowns = equation.atoms(sp.Symbol)

        for variable in info_unknowns:
            if variable in self.unknowns:
                compatibility += 1

        if compatibility == len(info_unknowns):
            self.info[info] = equation
            self.get_equations()
            self.get_dof()

    def clear_equations(self):
        for key, equation in self.equations.items():
            if len(equation.atoms(sp.S)) == 0:
                try:
                    self.balances.pop(key)

                except KeyError:
                    self.info.pop(key)

    def substitute(self, variable, value):
        if variable in self.unknowns:
            for key, equation in self.equations.items():
                self.equations[key] = self.equations[key].subs(variable, value)

                try:
                    self.balances[key] = self.balances[key].subs(variable, value)

                except KeyError:
                    self.info[key] = self.info[key].subs(variable, value)

            # self.clear_equations()
            # self.get_equations()
            self.unknowns.remove(variable)
            self.get_dof()

    def solve(self):
        """The solve method will build a matrix that sympy can solve with the sympy.solve() function. It will return the
        values in a dict which will then be used to store all solved unknowns to the dict_of_variables of the system."""

        # A pre-allocation for the matrix used to solve the system
        matrix = []

        # Each unknown must be put into a list so sympy can solve it
        unknowns_list = list(self.unknowns)

        # Each equation (except for the 'Total') will be appended to the matrix. This is done to allow for the user
        # or the code (when this feature is added) to easily double check the variables for accuracy
        for key, equation in self.equations.items():
            if key != 'Total':
                matrix.append(equation)

        # sympy does it's thing and returns a dict in the form of {symbol: solution}
        self.solutions = sp.solve(matrix, unknowns_list, dict=True)

    def __add__(self, addend):
        if type(addend) == System:
            total_balances = {}

            for material in set(list(self.balances.keys()) + list(addend.balances.keys())):

                total_balances[material] = 0

                if material in self.balances.keys():
                    total_balances[material] += self.balances[material]

                if material in addend.balances.keys():
                    total_balances[material] += addend.balances[material]

            summand_system = System(total_balances)

            for info, equation in {**self.info, **addend.info}.items():
                summand_system.check_info(info, equation)

            return summand_system

        else:
            for material in set(list(self.balances.keys()) + list(addend.composition.keys())):
                self.update_balances(material)
                addend.update_composition(material)
                self.balances[material] += addend.total * addend.composition[material]

            self.get_equations()
            self.get_unknowns()
            self.get_dof()

            return self


if __name__ == '__main__':
    print('ok')
