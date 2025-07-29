from typing_extensions import Self
import numpy as np

from .atm_models import atm_models

default_curved = True
default_model = 17

r_e = 6.371 * 1e6  # radius of Earth

"""
    All functions use "grams" and "meters", only the functions that receive and
    return "atmospheric depth" use the unit "g/cm^2"

    Atmospheric density models as used in CORSIKA. The parameters are documented in the CORSIKA manual
    the parameters for the Auger atmospheres are documented in detail in GAP2011-133
    The May and October atmospheres describe the annual average best.
"""
h_max = 112829.2  # height above sea level where the mass overburden vanishes


class Atmosphere:
    """
    Interface to manage the calculation of atmospheric properties of the air shower.

    Ported over from radiotools.atmosphere.models and jaxified. Currently only the tools used in
    template synthesis are ported over, but in principle can port over other modules as well.
    """

    def __init__(
        self: Self,
        model: int = 17,
        n0: float = (1 + 292e-6),
        observation_level: float = 0.0,
    ) -> None:
        """
        Interface for calculating properties of the atmosphere.

        Allows to determine height, depth, density, distance, ... for any point along an (shower) axis.

        Parameters
        ----------
        model : int, default=17 (US standard)
            atmospheric model to select from. The list of models are shown in atmosphere/atm_models.py
        n0 : float, default = 1 + 292e-6
            the refractive index at sea level.
        observation_level : float, default = 0 m
            the height in which the shower is observed in meters
        """
        self._model = model
        self._n0 = n0
        self._obs_lvl = observation_level

        self.a = atm_models[model]["a"]
        self.b = atm_models[model]["b"]
        self.c = atm_models[model]["c"]
        self.layers = atm_models[model]["h"]

    def get_geometric_distance_grammage(
        self: Self, grammage: np.ndarray, zenith: np.ndarray
    ) -> np.ndarray:
        """
        Get the geometrical distance from some grammage in the shower.

        Parameters
        ----------
        grammage : np.ndarray
            The atmospheric depth in g/cm^2
        zenith : np.ndarray
            The zenith angle of the shower in radians

        Returns
        -------
        dis_above_ground : np.ndarray
            the geometric distance above the observation level
        """
        # the vertical height from each grammage from the observed
        # level in meters
        height = (
            self.get_vertical_height(grammage * np.cos(zenith) * 1e4) + self._obs_lvl
        )  # 1e4 is cm^2 -> m^2 conversion

        # now taking into the inclination of the shower to get the true
        # geometric distance above the observed level in meters
        r = r_e + self._obs_lvl  # radius of the Earth
        dis_above_ground = (
            height**2 + 2 * r * height + r**2 * np.cos(zenith) ** 2
        ) ** 0.5 - r * np.cos(zenith)

        return dis_above_ground
    
    def __get_density_from_height(self : Self, height : np.ndarray) -> np.ndarray:
        """
        Get the density at a specific height.

        This is a private function that takes height as arguments as opposed to 
        grammage & zenith to be consistent with the radiotools implementation.

        Parameters
        ----------
        height : jax.typoing.ArrayLike
            The height in meters

        Returns
        -------
        dens : jax.Array
            the density in each atmospheric depth in g/m^3
        """
        return np.piecewise(
            height,
            [
                height < self.layers[0],
                np.logical_and(
                    height > self.layers[0], height <= self.layers[1]
                ),
                np.logical_and(
                    height > self.layers[1], height <= self.layers[2]
                ),
                np.logical_and(
                    height > self.layers[2], height <= self.layers[3]
                ),
                np.logical_and(height > self.layers[3], height <= h_max),
                height > h_max,
            ],
            [
                lambda h: self.b[0] * np.exp(-1.0 * h / self.c[0]) / self.c[0],
                lambda h: self.b[1] * np.exp(-1.0 * h / self.c[1]) / self.c[1],
                lambda h: self.b[2] * np.exp(-1.0 * h / self.c[2]) / self.c[2],
                lambda h: self.b[3] * np.exp(-1.0 * h / self.c[3]) / self.c[3],
                lambda h: h * 0.0 + self.b[4] / self.c[4],
                lambda h: h * 0.0,
            ],
        )
    
    def get_density(
        self: Self, grammage: np.ndarray, zenith: np.ndarray
    ) -> np.ndarray:
        """
        Get the density at a specific atmospheric depth and zenith angle.

        Parameters
        ----------
        grammage : np.ndarray
            The atmospheric depth in g/cm^2
        zenith : np.ndarray
            The zenith angle of the shower in radians

        Returns
        -------
        dens : np.ndarray
            the density in each atmospheric depth in g/m^3
        """
        # the vertical height from each grammage from the observed
        # level in meters
        vert_height = (
            self.get_vertical_height(grammage * np.cos(zenith) * 1e4)
        )  # 1e4 is cm^2 -> m^2 conversion

        return self.__get_density_from_height(vert_height)

    def get_refractive_index(
        self: Self, grammage: np.ndarray, zenith: np.ndarray
    ) -> np.ndarray:
        """
        Calculate the refractive index of the atmosphere at a given height.

        Parameters
        ----------
        grammage : np.ndarray
            The atmospheric depth in g/cm^2
        zenith : np.ndarray
            The zenith angle of the shower in radians

        Returns
        -------
        n : jax.Array
            the refractive index at the given height(s).
        """
         # the vertical height from each grammage from the observed
        # level in meters
        vert_height = (
            self.get_vertical_height(grammage * np.cos(zenith) * 1e4)
        )  # 1e4 is cm^2 -> m^2 conversion
        # using Snell's law (?),
        # i.e. using the ratio of density at some atmosphere vs the one at ground (=0)
        return (self._n0 - 1) * self.__get_density_from_height(vert_height) / self.__get_density_from_height(0.0) + 1
    
    def get_cherenkov_angle(
        self: Self, grammage: np.ndarray, zenith: np.ndarray
    ) -> np.ndarray:
        """
        Calculate the cherenkov angle from the atmospheric depth and zenith angle.

        Parameters
        ----------
        grammage : np.ndarray
            The atmospheric depth in g/cm^2
        zenith : np.ndarray
            The zenith angle of the shower in radians

        Returns
        -------
        cherenkov_angle : np.ndarray
            the cherenkov angle in units of radian
        """
        return np.arccos(1.0 / self.get_refractive_index(grammage, zenith))

    def get_atmosphere(self: Self, height: np.ndarray) -> np.ndarray:
        """
        Get the atmospheric depth from a given height(s).

        Parameters
        ----------
        height : np.ndarray
            The height in m

        Returns
        -------
        X : jax.Array
            the grammage (atmospheric depth) in g/m^2
        """
        y = np.where(
            height < self.layers[0],
            self.a[0] + self.b[0] * np.exp(-1.0 * height / self.c[0]),
            self.a[1] + self.b[1] * np.exp(-1.0 * height / self.c[1]),
        )
        y = np.where(
            height < self.layers[1],
            y,
            self.a[2] + self.b[2] * np.exp(-1.0 * height / self.c[2]),
        )
        y = np.where(
            height < self.layers[2],
            y,
            self.a[3] + self.b[3] * np.exp(-1.0 * height / self.c[3]),
        )
        y = np.where(
            height < self.layers[3], y, self.a[4] - self.b[4] * height / self.c[4]
        )
        y = np.where(height < h_max, y, 0)
        return y
    
    def get_vertical_height(self: Self, at: np.ndarray) -> np.ndarray:
        """
        Get vertical height from atmosphere, i.e., mass overburden for different layer.

        Parameters
        ----------
        at : np.ndarray
            the zenith-angle-corrected atmopheric depth in g/m^2

        Returns
        -------
        h : np.ndarray
            the vertical height above sea level in meters
        """
        atms = np.array([self.get_atmosphere(self.layers[i]) for i in range(4)])

        return np.piecewise(
            np.asarray(at),
            [
                at > atms[0],
                np.logical_and(at < atms[0], at > atms[1]),
                np.logical_and(at < atms[1], at > atms[2]),
                np.logical_and(at < atms[2], at > atms[3]),
            ],
            [
                lambda att: -1.0 * self.c[0] * np.log((att - self.a[0]) / self.b[0]),
                lambda att: -1.0 * self.c[1] * np.log((att - self.a[1]) / self.b[1]),
                lambda att: -1.0 * self.c[2] * np.log((att - self.a[2]) / self.b[2]),
                lambda att: -1.0 * self.c[3] * np.log((att - self.a[3]) / self.b[3]),
                lambda att: -1.0 * self.c[4] * (att - self.a[4]) / self.b[4],
            ],
        )

    def get_xmax_from_distance(
        self: Self, distance: np.ndarray, zenith: np.ndarray
    ) -> np.ndarray:
        """
        Calculate the cherenkov angle from the atmospheric depth and zenith angle.

        Parameters
        ----------
        distance : np.ndarray
            The distance of the shower from the core axis in m
        zenith : jax.typing.ArrayLIke
            The zenith angle of the shower in radians

        Returns
        -------
        Xmax : np.ndarray
            The shower maximum in g/cm^2
        """
        # first convert distance & zxenith into the height of the xmax above ground
        r = r_e + self._obs_lvl
        x = distance * np.sin(zenith)
        y = distance * np.cos(zenith) + r
        height_xmax = (x**2 + y**2) ** 0.5 - r + self._obs_lvl

        # now use this to compute the atmospheric depth
        return (
            self.get_atmosphere(height=height_xmax)* 1e-4 / np.cos(zenith)
        )  # 1e-4 to convert to g/cm^2
