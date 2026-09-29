Before we read a single line

ruf - All checks passed! the code is shaped like working code 
MyPy - No issues found, typed annotated all claims hold
Pytest - All tests passed. 

As far as the tests are concerned all code is working correctly

run code

rishiram@MacBookPro centellic-FDE % /usr/local/bin/python3 /Users/rishiram/centellic-FDE/week1/day5/candidate-c/candidate-b/src/reconcile.py
Reconciliation(variance=Decimal('1E-14'), matched=False)
Reconciliation(variance=Decimal('-0.01'), matched=False)
Reconciliation(variance=Decimal('0.00'), matched=True)
rishiram@MacBookPro centellic-FDE % 


I would not choose b against the spec because

1. All arithmetic is exact. A binary float anywhere in the calculation is a defect.


and B does float conversion

running = 0.0
    for line in lines:
        running += float(line)
    variance = Decimal(str(running)) - Decimal(expected_total)

And even results in incorrect response
Reconciliation(variance=Decimal('1E-14'), matched=False)
Both A and C return true which is correct

also it returns '1E-14'?
Vio of the spec

4. `variance` is always quantised to two decimal places.