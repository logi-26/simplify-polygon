# System imports
import matplotlib.pyplot as plt


class PlotGeometry:
    """
    Class for plotting geometries
    """

    def plot_polygon_difference(self, original_polygon, new_polygon):
        """
        This function plots the individual points from a polygon
        :param original_polygon: Shapely Polygon
        :param new_polygon: Shapely Polygon
        """

        # Get the polygon exterior co-ordinates as a list
        original_exterior_list = list(original_polygon.exterior.coords)
        new_exterior_list = list(new_polygon.exterior.coords)

        # Create the plot
        fig = plt.figure(1, figsize=(10, 10), dpi=90)

        # Loop through the points in the original polygon
        for point in original_exterior_list:
            # If the point is in the simplified polygon colour it blue, otherwise red
            if point in new_exterior_list:
                plt.scatter(point[0], point[1], color="#6699cc", alpha=0.7, s=200)
            else:
                plt.scatter(point[0], point[1], color="#de1212", alpha=0.7, s=200)

        # Display the plot
        plt.show()
        plt.close(fig)
