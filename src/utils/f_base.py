def linear_interpolation(x, points):
    """
    Performs linear interpolation on a set of points.

    Args:
    - x (float): The x-value to interpolate.
    - points (list of tuples): A list of (x, f) pairs, where the xs are in sorted order.

    Returns:
    - float: The interpolated value, or 1 if x is less than the first x-value,
             or 0 if x is greater than the last x-value.
    """

    # Check if x is less than the first x-value
    if x < points[0][0]:
        return 1

    # Check if x is greater than the last x-value
    if x > points[-1][0]:
        return 0

    # Linear interpolation for values between points
    for i in range(len(points) - 1):
        if points[i][0] <= x <= points[i + 1][0]:
            xA, fA = points[i]
            xB, fB = points[i + 1]
            return fA + (fB - fA) * ((x - xA) / (xB - xA))

    # If x is not in the range, return None (this should not happen if inputs are correct)
    return None


def linear_interpolation_with_penalty(x, points, penalty_coef):
    """
    Performs linear interpolation on a set of points with a penalty coefficient for x-values
    greater than the largest x in points.

    Args:
    - x (float): The x-value to interpolate.
    - points (list of tuples): A list of (x, f) pairs, where the xs are in sorted order.
    - penalty_coef (float): The penalty coefficient to apply for x-values greater than the largest x.

    Returns:
    - float: The interpolated value, or 1 if x is less than the first x-value,
             or the penalized value if x is greater than the last x-value.
    """

    # If x is less than the smallest x in points, return 1
    if x < points[0][0]:
        return 1

    # If x is exactly one of the points, return the corresponding y
    for point in points:
        if x == point[0]:
            return point[1]

    # If x is greater than the largest x in points, apply the penalty
    if x > points[-1][0]:
        x_last, f_last = points[-1]
        # The linear function will have the form y = mx + c
        # We know the slope (m) and a point (x_last, f_last) through which the line passes
        # c can be calculated using the equation of the line y = mx + c
        c = f_last - (penalty_coef * x_last)
        return (penalty_coef * x) + c

    # Otherwise, find the two points (xA, fA) and (xB, fB) such that xA < x < xB
    for i in range(len(points) - 1):
        if points[i][0] < x < points[i + 1][0]:
            xA, fA = points[i]
            xB, fB = points[i + 1]
            # Perform the linear interpolation
            return fA + (fB - fA) * (x - xA) / (xB - xA)

    # If x is not in the range, return None (this should not happen if inputs are correct)
    return None
