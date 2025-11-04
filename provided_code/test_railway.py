from railway import Station, RailNetwork
import pytest


# fare price : assert right price, check negative distance, regions, hubs


@pytest.mark.parametrize(
    ["name", "region", "crs", "lat", "lon", "hub"],
    [
        pytest.param(2, "London", "KGX", 51.530827, 0.122907, 1, id="invalid name"),
        pytest.param(
            "London Kings Cross", 2, "KGX", 51.530827, 0.122907, 1, id="invalid region"
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "kgx",
            51.530827,
            0.122907,
            1,
            id="lower case CRS",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "KGXT",
            51.530827,
            0.122907,
            1,
            id="four letter CRS",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            2,
            51.530827,
            0.122907,
            1,
            id="invalid CRS",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "KGX",
            "fifty-one",
            0.122907,
            1,
            id="invalid latitude",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "KGX",
            91.530827,
            0.122907,
            1,
            id="latitude out of range",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "KGX",
            91.530827,
            "0.122907",
            1,
            id="invalid longitutde",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "KGX",
            91.530827,
            -181,
            1,
            id="longitude out of range",
        ),
        pytest.param(
            "London Kings Cross",
            "London",
            "KGX",
            91.530827,
            0.122907,
            "1",
            id="invalid hub",
        ),
    ],
)
def test_station_constructor(name, region, crs, lat, lon, hub):
    with pytest.raises(ValueError):
        Station(name=name, region=region, crs=crs, lat=lat, lon=lon, hub=hub)


def test_duplicate_crs_rail_network():
    with pytest.raises(ValueError):
        brighton = Station(
            name="Brighton",
            region="South East",
            crs="BTN",
            lat=50.829659,
            lon=-0.141234,
            hub=True,
        )

        kings_cross = Station(
            name="London Kings Cross",
            region="London",
            crs="KGX",
            lat=51.530827,
            lon=-0.122907,
            hub=True,
        )

        # duplicating CRS here

        edinburgh_park = Station(
            name="Edinburgh Park",
            region="Scotland",
            crs="KGX",
            lat=55.927615,
            lon=-3.307829,
            hub=False,
        )

        list_of_stations = [brighton, kings_cross, edinburgh_park]

        RailNetwork(list_of_stations)
