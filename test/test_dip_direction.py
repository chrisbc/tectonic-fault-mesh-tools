from unittest import TestCase

import numpy as np
from shapely.geometry import LineString

from fault_mesh.faults.generic import (bearing_geq, bearing_leq,
                                       calculate_dip_direction,
                                       normalize_bearing, reverse_bearing,
                                       reverse_line, smallest_difference)


class test_bearing_functions(TestCase):
    def test_smallest_difference1(self):
        small_diff = smallest_difference(5, 355)
        self.assertAlmostEqual(small_diff, 10.0)

    def test_smallest_difference2(self):
        small_diff = smallest_difference(-4.0, 355)
        self.assertAlmostEqual(small_diff, 1.0)

    def test_smallest_difference3(self):
        small_diff = smallest_difference(46.0, 225)
        self.assertAlmostEqual(small_diff, 179)

    def test_smallest_difference4(self):
        small_diff = smallest_difference(44.0, 225)
        self.assertAlmostEqual(small_diff, 179)

    def test_normalize1(self):
        self.assertAlmostEqual(normalize_bearing(-45), 315)

    def test_normalize2(self):
        self.assertAlmostEqual(normalize_bearing(693), 333)

    def test_leq1(self):
        self.assertIs(bearing_leq(271.0, 90.0), True)

    def test_leq2(self):
        self.assertIs(bearing_leq(269.0, 90.0), False)

    def test_geq1(self):
        self.assertIs(bearing_geq(140.0, 315.0), False)

    def test_geq2(self):
        self.assertIs(bearing_geq(90.0, 315.0), True)

    def test_reverse_bearing1(self):
        self.assertAlmostEqual(180.1, reverse_bearing(0.1))


class test_geometric_functions(TestCase):
    def setUp(self) -> None:
        self.straight_fault_array = np.array(
            [[1640000.0, 5350000.0], [1650000.0, 5360000.0]]
        )
        self.array_reversed = self.straight_fault_array[-1::-1, :]
        self.straight_fault_linestring = LineString(self.straight_fault_array)
        self.bent_fault_array = np.array(
            [[1640000.0, 5350000.0], [1650000.0, 5360000.0], [1640000.0, 5370000.0]]
        )
        self.bent_array_reversed = self.bent_fault_array[-1::-1, :]
        self.bent_line = LineString(self.bent_array_reversed)

    def test_reverse_line1(self):
        reversed_straight = reverse_line(self.straight_fault_linestring)
        np.testing.assert_array_almost_equal(
            np.array(reversed_straight.coords), self.array_reversed
        )

    def test_reverse_line2(self):
        reversed_bent = reverse_line(self.bent_line)
        np.testing.assert_array_almost_equal(
            np.array(reversed_bent.coords), self.bent_fault_array
        )

    def test_dip_direction_straight1(self):
        self.assertAlmostEqual(
            calculate_dip_direction(self.straight_fault_linestring), 135.0
        )

    def test_dip_direction_straight2(self):
        self.assertAlmostEqual(
            calculate_dip_direction(
                LineString(reverse_line(self.straight_fault_linestring))
            ),
            315,
        )

    def test_dip_direction_bent1(self):
        self.assertAlmostEqual(calculate_dip_direction(self.bent_line), 270.0)

    def test_dip_direction_bent2(self):
        self.assertAlmostEqual(
            calculate_dip_direction(LineString(self.bent_fault_array)), 90.0
        )


# class test_dip_direction(TestCase):
