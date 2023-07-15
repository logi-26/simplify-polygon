# System imports
from shapely.geometry import Polygon
from numpy import deg2rad, sin, cos, arctan2, sqrt, diff, pi


class SimplifyPolygon:
    """
    Class for simplifying a Shapely Polygon
    """

    def polygon_geodesic_area(self, poly):
        """
        This function computes the area of a polygon, assuming a spherical Earth
        :param poly: Shapely Polygon
        :return: polygon geodesic area
        """

        # Aproximate radius of Earth
        radius = 6378137

        # Get the polygon exterior coordinates
        lons, lats = poly.exterior.coords.xy

        # Convert the lattitude and longitude degress to radius
        lats = deg2rad(lats)
        lons = deg2rad(lons)

        # Perform calculation
        a = sin(lats / 2) ** 2 + cos(lats) * sin(lons / 2) ** 2
        colat = 2 * arctan2(sqrt(a), sqrt(1 - a))
        az = arctan2(cos(lats) * sin(lons), sin(lats)) % (2 * pi)
        daz = diff(az)
        daz = (daz + pi) % (2 * pi) - pi
        deltas = diff(colat) / 2
        colat = colat[0:-1] + deltas

        # Perform integral
        integrands = (1 - cos(colat)) * daz

        # Integrate
        area = abs(sum(integrands)) / (4 * pi)
        area = min(area, 1 - area)

        return (
            area * 4 * pi * radius**2 / 10000 if radius is not None else area / 10000
        )

    def _get_triangle_area(self, start_point, mid_point, end_point):
        """
        This function gets the geodesic area of the triangle
        :param start_point: Shapely Point
        :param mid_point: Shapely Point
        :param end_point: Shapely Point
        :return: polygon geodesic area
        """

        # Generate a Shapely Polygon from the 3 Points
        three_point_polygon = Polygon([start_point, mid_point, end_point])

        # Return the geodesic area of the Polygon
        return self.polygon_geodesic_area(three_point_polygon)

    def _simplify(self, poly):
        """
        This function simplifies the Polygon
        :param poly: Shapely Polygon
        :return: Shapely Polygon
        """

        # Get the current area of the polygon
        original_poly_area = self.polygon_geodesic_area(poly)

        # Get the field exterior points from the boundary polygon
        original_poly_points = list(poly.exterior.coords)

        # Our initial margin of error
        err_margin = 0.00002

        # Main loop to simplify the field boundary and check the field area
        simplification_accepted = False
        loop_count = 0
        while err_margin > 0.000001 and not simplification_accepted:
            # Increment the loop counter
            loop_count += 1

            # Create a copy of the original polygon boundary points
            new_poly = original_poly_points.copy()

            # Loop through the outter polygon points
            # (stop 2 points before the end of the list to prevent index out of range)
            i = 0
            while i < len(new_poly) - 2:
                # Get the next 3 points from the polygon
                start_point = new_poly[i]
                mid_point = new_poly[i + 1]
                end_point = new_poly[i + 2]

                # Calculate the area of the 3 points (triangle)
                triangle_area = self._get_triangle_area(
                    start_point, mid_point, end_point
                )

                # If the area of the 3 points is greater than our margin of error,
                # increment the loop counter to move on to the next point
                if triangle_area > err_margin:
                    i += 1
                else:
                    # Remove the point from the copied list of polygon points
                    new_poly.pop(i + 1)

            # If there are more than 3 points left after the simplification process has been completed
            new_poly_area = 0
            if len(new_poly) > 3:
                # Get the area of the newly simplified polygon
                new_poly_area = self.polygon_geodesic_area(Polygon(new_poly))

                # Round the orignal polygon area size and
                # the newly simplified polygon area size to 2 decimal places
                original_rounded_poly_area = round(original_poly_area, 2)
                new_rounded_poly_area = round(new_poly_area, 2)

                # If the original rounded area matches the simplified rounded area
                # this simplification can be accepted otherwise decreae the margin of error
                if original_rounded_poly_area == new_rounded_poly_area:
                    simplification_accepted = True
                else:
                    err_margin = err_margin * 0.9
            else:
                err_margin = err_margin * 0.9

        # If we have gone beyond our margin of error and the polygon does not match in size
        # (we revert to the original polygon)
        if not simplification_accepted:
            new_poly = original_poly_points.copy()

        return Polygon(new_poly)

    def run_simplification(self, poly):
        """
        This runs the Polygon simplification process
        :param poly: Shapely Polygon
        :return: Shapely Polygon
        """

        # Get the number of holes
        number_of_holes = len(poly.interiors)

        # If the field contains any holes
        field_interiors = poly.interiors if number_of_holes > 0 else None

        # Simplify the polygon using the algorithm
        simplified_polygon = self._simplify(poly)

        if simplified_polygon.is_valid:
            # If the field boundary contains any holes
            if field_interiors is not None:
                return Polygon(
                    simplified_polygon.exterior.coords,
                    [inner for inner in field_interiors],
                )
            else:
                return simplified_polygon
