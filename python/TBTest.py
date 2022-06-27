#map voltage range to turbidity (NTU)
for x in range(250, 425, 10):
    x = float(x/100.0)
    A = (-1120.4 * (x * x))
    B = (5742.3 * x)    
    C = 4352.9
#    print x, A, B, C
    tb = A + B - C
    print tb
    
