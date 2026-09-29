Chosen: a

Why: It matches all spec requirements
- Hits 1 as strings are converted straight into Decimal rather than using floats.
- Hits 2 because a variance of one pennt was rejected. print(reconcile(["10.00", "19.99"], "30.00"))  # one penny short, Reconciliation(variance=Decimal('-0.01'), matched=False)
- Hits 3 and we know this from the tests as they all pass
- Hits 4 and we can see this from the printed outputs: 
Reconciliation(variance=Decimal('0.00'), matched=True)
Reconciliation(variance=Decimal('-0.01'), matched=False)
Reconciliation(variance=Decimal('0.00'), matched=True)

Rejected: B, and C

B breaks two rules

1. All arithmetic is exact. A binary float anywhere in the calculation is a defect. it does a float conversion
4. `variance` is always quantised to two decimal places. Printed Reconciliation(variance=Decimal('1E-14'), matched=False) for the first one and 1E-14 is larger than two DP.

C breaks one rule
2. `matched` is `True` **only** on an exact zero variance. There is no tolerance. A one-penny discrepancy is a discrepancy. 
    Yet specifcally says
        """Return the variance between the statement lines and the expected total.

    Treats a variance within a one-penny tolerance as matched, so that rounding
    differences between systems do not surface as spurious discrepancies.
    """

    Even outputed: Reconciliation(variance=Decimal('-0.01'), matched=True), tests pass because the code is correct, the implementation is wrong


Consequences:

If B is shipped, float does not store exact values, it stores nearest binary approximation. Real value is lost and Decimal can't reapir that. Rounding errors will occur.
If C ships, real one-penny mismatches will be hidden as successful reconciliations, reducing the accuracy of financial reporting.