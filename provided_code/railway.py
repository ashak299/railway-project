import matplotlib.pyplot as plt
import math
from dataclasses import dataclass


def fare_price(
    distance: float, different_regions: bool, hubs_in_dest_region: int
) -> float:
    """Returns the fare price for a direct leg.

    Args:
        distance(float) : distance between the start and destination
        different_regions(bool) : True if the start and destination are in different regions
        hubs_in_dest_region(int) : Number of hubs in the destination region

    Returns:
        float : Fare price for the journey.
    """

    price = 1 + distance * math.exp(-distance / 100) * (
        1 + (different_regions * hubs_in_dest_region) / 10
    )
    return price


@dataclass
class Station:
    """Class for Station"""

    name: str
    region: str
    crs: str
    lat: float
    lon: float
    hub: bool

    def __post_init__(self):
        # print("DEBUG: post_init called with types:")
        if not isinstance(self.name, str):
            raise ValueError(f"'name' must be a str, was {self.name}")

        if not isinstance(self.region, str):
            raise ValueError(f"'region' must be a str, was {self.region}")

        if not isinstance(self.crs, str):
            raise ValueError(f"'crs' must be a str, was {self.crs}")

        if not isinstance(self.lat, float):
            raise ValueError(f"'lat' must be a float, was {self.lat}")

        if not isinstance(self.lon, float):
            raise ValueError(f"'lon' must be a float, was {self.lon}")

        if not isinstance(self.hub, bool):
            raise ValueError(f"'hub' must be a bool, was {self.hub}")

        # check longitude and latitude
        if not (-90 <= self.lat <= 90):
            raise ValueError(
                f"'lat' must be between -90 and 90 degrees, it was {self.lat}"
            )

        if not (-180 <= self.lon <= 180):
            raise ValueError(
                f"'lon' must be between -180 and 180 degrees, it was {self.lon}"
            )

        # validate CRS
        if len(self.crs) != 3 or not self.crs.isupper():
            raise ValueError(f"'crs' must be 3 capital letters, it was {self.crs}")

    def distance_to(self):
        raise NotImplementedError


@dataclass
class RailNetwork:
    """Class for Rail Network"""

    def __init__(self, list_of_stations: list):
        stations = {}
        seen = set()

        for station in list_of_stations:
            # Checking for duplicate crs
            if station.crs in seen:
                raise ValueError(
                    f"CRS should be unique in a rail network, {station.crs} was duplicated"
                )
            seen.add(station.crs)

            stations[station.crs] = station

        self.stations = stations

    def regions(self):
        raise NotImplementedError

    def n_stations(self):
        raise NotImplementedError

    def hub_stations(self, region):
        raise NotImplementedError

    def closest_hub(self, s):
        raise NotImplementedError

    def journey_planner(self, start, dest):
        raise NotImplementedError

    def journey_fare(self, start, dest, summary):
        raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return
