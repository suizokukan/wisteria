"""
TODO
"""
import statistics


def pseudo_geometric_mean(values):
    """
TODO
statistics.geometric_mean() applied to a serie of <values> that may contain 0.
Une valeur approchée est calculée.
    """
    values2 = []
    for value in values:
        if value == 0:
            values2.append(0.00000000000001)
        else:
            values2.append(value)
    return statistics.geometric_mean(values2)


def remove_absurd_values(values,
                         max_récusés_coeff=0.05,
                         replace_0geometricmean_by=0.000001,
                         max_ratio_value_geometricmean=25):
    """
TODO
                (bool)success, values
    """
    # ---- special case: all values are 0 ----
    if values.count(0) == len(values):
        return True, values

    # ---- normal case ----
    success = True

    # max_récusés can't be set to 0, its minimal value is 1:
    max_récusés = max(len(values) * max_récusés_coeff, 1)

    # TODO : why geometric ?
    geometricmean = pseudo_geometric_mean(values)
    if geometricmean == 0:
        geometricmean = replace_0geometricmean_by
    indexes_to_be_removed = []
    for value_index, value in enumerate(values):
        if not 0 <= abs(value/geometricmean) <= max_ratio_value_geometricmean:
            indexes_to_be_removed.append(value_index)
    for value_index in indexes_to_be_removed[::-1]:
        del values[value_index]

    if len(indexes_to_be_removed) > max_récusés:
        success = False

    return success, values
