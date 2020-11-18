# -*- coding: utf-8 -*-
import math as m
import svgwrite as svg


def fractality_pair(poi_one, poi_two):

    x_one = poi_one[0]
    y_one = poi_one[1]

    x_two = poi_two[0]
    y_two = poi_two[1]

    # calculate coordinates of middle
    x_mid = (x_two + x_one) / 2.0
    y_mid = (y_two + y_one) / 2.0

    # calculate 1/3 of line
    x_1_3 = x_one + (x_two - x_one) / 3.0
    y_1_3 = y_one + (y_two - y_one) / 3.0

    # calculate 2/3 of line
    x_2_3 = x_one + 2.0 * (x_two - x_one) / 3.0
    y_2_3 = y_one + 2.0 * (y_two - y_one) / 3.0

    # calculate perpendicular length

    segment_length = ((x_one - x_two) ** 2 + (y_one - y_two) ** 2) ** 0.5
    perpend_length = (segment_length * (3.0 ** 0.5)) / 6.0

    segment_azi = 0
    tan_azi = 0

    if x_one == x_two:
        if y_two > y_one:  # we have 270 degrees
            segment_azi = 1.5 * m.pi
        else:
            segment_azi = m.pi / 2.0
    else:
        tan_azi = (y_two - y_one) / (x_two - x_one)
        if x_two > x_one:
            segment_azi = m.atan(tan_azi)
        else:
            segment_azi = m.atan(tan_azi) + m.pi

    perpend_azi = segment_azi - 0.5 * m.pi
    x_per = x_mid + perpend_length * m.cos(perpend_azi)
    y_per = y_mid + perpend_length * m.sin(perpend_azi)

    return (
        (x_one, y_one),
        (x_1_3, y_1_3),
        (x_per, y_per),
        (x_2_3, y_2_3),
        (x_two, y_two)
    )


def fractality_all(line_coords):
    
    ready_coords = ()
    fractaled = ()
    for i in range(0, len(line_coords) - 1):
        start_point = line_coords[i]
        end_point = line_coords[i + 1]
        
        fractaled = fractality_pair(start_point, end_point)
        if len(ready_coords) > 2:
            if ready_coords[len(ready_coords) - 1] == fractaled[0]:
                ready_coords += fractaled[1:]
            else:
                ready_coords += fractality_pair(start_point, end_point)
        else:
            ready_coords += fractality_pair(start_point, end_point)
    return ready_coords


def draw_fract(start_coords, n):
    dwg = svg.Drawing('test5.svg', profile='tiny', size=(u'640px', u'640px'))
    coords = start_coords
    for i in range(n):
        dwg.add(dwg.polyline(points=coords, stroke='black', stroke_width=0.5, fill='none'))
        coords = fractality_all(coords)
    dwg.save()
    print('Oke')


def prepare_sceleton(doc_size):
    scelet_rad = doc_size / 2 - 10
    x_center = y_center = doc_size / 2
    azi_upper_point = m.radians(30)    
    azi_right_point = m.radians(150)
    azi_left_point = m.radians(270)
    x_upper_point = x_center + scelet_rad * m.cos(azi_upper_point)
    y_upper_point = y_center + scelet_rad * m.sin(azi_upper_point)
    x_right_point = x_center + scelet_rad * m.cos(azi_right_point)
    y_right_point = y_center + scelet_rad * m.sin(azi_right_point)
    x_left_point = x_center + scelet_rad * m.cos(azi_left_point)
    y_left_point = y_center + scelet_rad * m.sin(azi_left_point)
    return (
        (x_upper_point, y_upper_point),
        (x_right_point, y_right_point),
        (x_left_point, y_left_point),
        (x_upper_point, y_upper_point)
    )

sceleton = prepare_sceleton(640)
draw_fract(sceleton, 7)
