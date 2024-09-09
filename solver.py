import sympy
from sympy.printing import latex
from sympy.parsing.sympy_parser import parse_expr
from math import log10, floor

def main(inputs):
    equation = inputs["equation"]
    eq_beforeequal, eq_afterequal = equation.split('=')
    result = sympy.parsing.sympy_parser.parse_expr(eq_afterequal)

    list_variables = result.free_symbols
    partials = []
    deltas = []
    firststep = "\\delta{" + eq_beforeequal + "}=" + "\\sqrt{"
    secondstep = "\\delta{" + eq_beforeequal + "}=" + "\\sqrt{"
    for i, var in enumerate(list_variables):
        key_str = '\\frac{\partial ' + eq_beforeequal + '}{\\partial ' +str(var)+'}'
        partial = [key_str, latex(sympy.diff(result, var))]
        partials.append(partial)
        delta_sym = "\\delta{" + str(var) + "}"
        delta = [str(var), sympy.Symbol(delta_sym)]
        deltas.append(delta)
        
    
        firststep += "(" + partials[i][0] + ")^2(" + str(delta_sym) + ")^2" 
        if i < len(list_variables) - 1:
            firststep += "+"
        secondstep += "(" + partials[i][1] + ")^2(" + str(delta_sym) + ")^2" 
        if i < len(list_variables) - 1:
            secondstep += "+"
    firststep += "}"
    secondstep += "}"
    formatted_partials = []
    for i in range(len(partials)):
        temp_list = [partials[i][0], partials[i][1]]
        formatted_partials.append('='.join(temp_list))
        

    plugin = None
    # parse substitution
    if inputs["substitution"]:
        substituted_vars = inputs["substitution"]  # example: "substitution": "\delta x=1,x=2,\delta y=4"

        eqn = get_sympy(inputs)
        subs = substituted_vars.split(",")
        var_value = [sub.split("=") for sub in subs]

        for var, value in var_value:
            if "\delta" in var:
                var = f"({var})"

            var = sympy.Symbol(var)
            eqn = eqn.subs(var, float(value))
        
        if eqn.is_number:
            plugin = "\\delta{" + eq_beforeequal + "}=" + str(float(eqn))

    return { 
        "firststep": firststep,
        "secondstep": secondstep,
        "partials": formatted_partials,
        "plugin": plugin,
    }

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

def get_sympy(inputs):
    # extract input
    equation = inputs["equation"]
    # seperate the LHS and RHS of the equation
    lhs, rhs = equation.split('=')

    # parse equation
    lhs = sympy.Symbol(lhs)
    rhs = parse_expr(rhs)

    rhs_vars = rhs.free_symbols
    d_lhs = 0  # error of LHS
    d_lhs_vars = []  # stores variable symbols (partials and deltas)

    # create non-substituted equation for error
    for var in rhs_vars:
        partial = sympy.Symbol(r"(\frac{\partial " + str(lhs) + r"}{\partial " + str(var) + r"})")
        delta = sympy.Symbol("(\\delta " + str(var) + ")")
        d_lhs = sympy.Add(d_lhs, (partial ** 2) * (delta ** 2))
        d_lhs_vars.append({
            "partial": partial, 
            "delta": delta
            })
    # finally, sqrt
    d_lhs = sympy.nsimplify(sympy.sqrt(d_lhs))

    # take partials and substitute
    partials = []  # storing all partial derivatives
    d_lhs_subs = d_lhs
    for i, var in enumerate(rhs_vars):
        # take partial derivative
        diff = sympy.diff(rhs, var)

        # sub in error equation (d_lhs)
        d_lhs_subs = d_lhs_subs.subs(d_lhs_vars[i]["partial"], diff)

    return d_lhs_subs
