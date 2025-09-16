def count_cal_norm(weight, height, age, activeness_cef, is_male):
    result = 9.99 * weight + 6.25 * height - 4.92 * age

    if is_male:
        result += 5
    elif not is_male:
        result -= 161

    result *= activeness_cef
    result = round(result)
    return result
