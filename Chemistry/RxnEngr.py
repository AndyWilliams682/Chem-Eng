import sympy as sp


rR = sp.S('0.4 * (x ^ 2)')
rS = sp.S('2 * x')
rA = -(rR + rS)
Yield_S_A = rS / -rA
# p1 = sp.plot(Yield_R_A, (sp.S('x'), 0, 7))
# p2 = sp.plot((1 / -rA).subs(sp.S('x'), sp.S('7 * (1 - X)')), (sp.S('X'), 0, 0.9))


def model_cr(initial_conc, final_conc):
    cr = sp.integrate(Yield_S_A, (sp.S('x'), final_conc, initial_conc)).evalf()
    overall_yield = cr / (initial_conc - final_conc)
    tau = initial_conc * sp.integrate((1 / -rA.subs(sp.S('x'), sp.S('40 * (1 - X)'))), (sp.S('X'), 0, 0.9))
    return cr, overall_yield, tau


def xa_ca(xa, ca0):
    return ca0 * (1 - xa)


print(model_cr(40, xa_ca(0.9, 40)))
