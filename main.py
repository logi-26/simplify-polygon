# System imports
from shapely.geometry import Polygon

# Local imports
from simplify_fields import SimplifyPolygon
from plotting import PlotGeometry


class Simplify:
    """
    Simplify class
    """

    def print_results(
        self,
        poly,
        original_area,
        original_poly_points,
        simplified_polygon,
        simplified_area,
        simplified_poly_points,
    ):
        """
        This function prints the polygon info
        :param poly: Shapely Polygon
        :param original_area: float
        :param original_poly_points: list
        :param simplified_polygon: Shapely Polygon
        :param simplified_area: float
        :param simplified_poly_points: list
        """
        print(f"\nOriginal Polygon: {poly}")
        print(f"Original Polygon Area: {round(original_area)}")
        print(f"Original Polygon Points: {len(original_poly_points)}")
        print(f"\nSimplified Polygon: {simplified_polygon}")
        print(f"Simplified Polygon Area: {round(simplified_area)}")
        print(f"Simplified Polygon Points: {len(simplified_poly_points)}")

        # Calculate the reduction percentage
        try:
            reduction_percent = round(
                100.0
                - (
                    100
                    * float(len(simplified_poly_points))
                    / float(len(original_poly_points))
                )
            )
            print(f"\nPolygon Reduction: {reduction_percent}%")
        except ZeroDivisionError:
            pass

    def simplify_polygon(self, in_poly):
        """
        Simplify a polygon
        :param in_poly: list
        """

        # Convert the points to a Shapely Polygon
        try:
            poly = Polygon(in_poly)
        except (ValueError, TypeError):
            print("ERROR: Unable to parse input polygon")
            poly = None

        if poly:
            # Reference to the polygon simplify class
            simple_poly_class = SimplifyPolygon()

            # Simplify the polygon using the algorithm
            simplified_polygon = simple_poly_class.run_simplification(poly)

            # Get the geodesic area of the original polygon
            original_area = simple_poly_class.polygon_geodesic_area(poly)

            # Get the exterior coordinates from the original polygon
            original_poly_points = list(poly.exterior.coords)

            # Get the geodesic area of the simplified polygon
            simplified_area = simple_poly_class.polygon_geodesic_area(
                simplified_polygon
            )

            # Get the exterior coordinates from the original polygon
            simplified_poly_points = list(simplified_polygon.exterior.coords)

            # Print the results
            self.print_results(
                poly,
                original_area,
                original_poly_points,
                simplified_polygon,
                simplified_area,
                simplified_poly_points,
            )

            return simplified_polygon


# Declare a sample polygon and then attempt to simplify it
the_polygon = [
    [0.1, 0],
    [0.12, 0],
    [1.1, 0],
    [1.12, 0],
    [1.1, 1],
    [1, 1],
    [0, 1],
    [0, 0],
]
simplify_class = Simplify()
simplified_polygon = simplify_class.simplify_polygon(the_polygon)

# Plot the polygon points
PlotGeometry = PlotGeometry()
PlotGeometry.plot_polygon_difference(Polygon(the_polygon), simplified_polygon)
