def mean(data):
    return sum(data) / len(data)

def correlation_r(x, y):
    if len(x) != len(y):
        raise ValueError("Input lists must be of the same length.")
    
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n)) ** 0.5
    denominator_y = sum((y[i] - mean_y) ** 2 for i in range(n)) ** 0.5

    if denominator_x == 0 or denominator_y == 0:
        return 0.0  

    return numerator / (denominator_x * denominator_y)

def interpret_r(r):
    if r > 0.5:
        return ("Strong", "Positive")
    elif 0.3 <= r <= 0.5:
        return ("Moderate", "Positive")
    elif 0 < r < 0.3:
        return ("Weak", "Positive")
    elif r == 0:
        return ("None", "None")
    elif -0.3 < r < 0:
        return ("Weak", "Negative")
    elif -0.5 <= r <= -0.3:
        return ("Moderate", "Negative")
    elif r < -0.5:
        return ("Strong", "Negative")
    else:
        return ("Invalid", "Invalid")