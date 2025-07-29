function constraint_func1(x1, x2)
    # 1st constraint function written in matlab of 
    # the test problem HS15 from the Hock & Schittkowski collection.
    #   min   100 (x2 - x1^2)^2 + (1 - x1)^2
    #   s.t.  x1 x2 >= 1
    #         x1 + x2^2 >= 0
    #         x1 <= 0.5

    constr1 = x1 .* x2 .- 1
    return constr1
end