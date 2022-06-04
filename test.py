import math

sample = "0.11650  0.11300  0.09700  0.08250  0.06300  0.05600  0.12500\n\
0.07150  0.07550  0.05500  0.02150  0.02350  0.05550  0.10900\n\
0.09200  0.10550  0.07900  0.05187  0.04800  0.06450  0.09750\n\
0.09250  0.09500  0.05400  0.05900  0.06387  0.05000  0.09850\n\
0.13300  0.13750  0.12600  0.09587  0.09850  0.12450  0.12150\n\
0.14300  0.14300  0.14000  0.10000  0.12150  0.14100  0.12700\n\
0.14750  0.11850  0.12100  0.10400  0.12950  0.12100  0.17100"

# Goal values
# Raw values:
#       0.06	0.02	0.07
#       0.03	0.00	0.04
#       0.09	0.05	0.11
#
# Degrees:
#       43°CW	14°CW	50°CW
#       22°CW	0	29°CW
#       65°CW	36°CW	79°CW

print(sample)


def get_distance(ab_matrix):
    abs_points = ab_matrix.replace('\n', '  ').split('  ')
    rel_points = [0, 3, 6, 21, 27, 42, 45, 48]
    a = [0, 3, 6, 21, 27, 42, 45, 48]


    center = float(abs_points[24])
    for i in range(8):
        rel_points[i] = round((float(abs_points[ a[i] ]) - center), 2)

    print(f'rel_points:\n{rel_points} ')
    return rel_points


def to_degrees(distances):
    for i in range(8):
        screw_pitch = 0.5
        distances[i] = round((distances[i] / screw_pitch * 360),2)

    return distances


def degree_matrix_string(degrees):
    for i in range(8):
        postfix = 'CW' if degrees[i] > 0 else 'CCW'
        degrees[i] = f'{abs(degrees[i])}° {postfix if abs(degrees[i]) != 0.0 else ""}'
    print(f'degree:\n{degrees} ')
    return degrees

degree_matrix_string(to_degrees(get_distance(sample)))