"""Sample neighboring vertex values with a distance falloff. Closer vertices carry more weight in
influencing the sampled value"""

import maya.api.OpenMaya as om2

"""Getting 0-1 percentage of all the distances, checking to make sure we do not divide by 0"""


def get_falloff(vertex_distance_list, vertex_value_list):
    """
    :param vertex_distance_list: float list with distances of nearby vertices. Must be same length as vertex_value list.
    :param vertex_value_list: Can be and array of MVectors, MColors, Floats.
    :return: Sum of the vertex_value_list with weight given to closer vertices.
    """

    if sum(vertex_distance_list) == 0:
        distances_percentages = [(x / 1) for x in vertex_distance_list]
    else:
        distances_percentages = [(x / sum(vertex_distance_list)) for x in vertex_distance_list]

    """Setting this so that the greater the distance value, the less weight it's vertex_value adds."""
    inverse_distance_percentage = [1 - x for x in distances_percentages]

    """Normalizing the inverse distance to multiply with the vertex values"""
    normalize_inverse_percentage = [x / sum(inverse_distance_percentage) for x in inverse_distance_percentage]

    """Multiply each vertex value with normalized inverse percentage and then gather the sum of that list, this will be 
    the new sampled value. Closer verts with contribute more to the sum."""
    new_vertex_value = \
        [vertex_value_list[x] * normalize_inverse_percentage[x] for x in range(len(normalize_inverse_percentage))]
    value_sum = om2.MColor((0, 0, 0, 1))
    for i in new_vertex_value:

        value_sum += i

    return value_sum


