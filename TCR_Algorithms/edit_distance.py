def edit_distance_leq_one(a: str, b: str) -> bool:
    """
    Return True if edit distance between a and b is <= 1.
    """
    if abs(len(a) - len(b)) > 1:
        return False
    i, j = 0, 0
    diff = 0

    while i < len(a) and j < len(b):
        if a[i] != b[j]:
            diff += 1
            if diff > 1:
                return False
            # substitution
            if len(a) == len(b):
                i += 1
                j += 1
            # deletion in a
            elif len(a) > len(b):
                i += 1
            # insertion in a
            else:
                j += 1
        else:
            i += 1
            j += 1
    if i < len(a) or j < len(b):
        diff += 1
    return diff <= 1
