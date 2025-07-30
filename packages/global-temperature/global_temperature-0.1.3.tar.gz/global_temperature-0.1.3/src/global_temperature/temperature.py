from .temperature_monthly import TemperatureMonthly
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


from typing import Union, overload
from global_temperature.temperature_monthly import TemperatureMonthly


class TemperatureFactory:
    """
    Factory class to create Temperature objects.
    """

    @overload
    @staticmethod
    def create_temperature_object(
        data_type: str,
        search_radius: float = 0.1,
        source_folder: str | Path = "",
        geohash_precision: int = 1,
        max_cache_size: int = 200,
        grid_name: str = "01x01",
    ) -> TemperatureMonthly: ...

    @staticmethod
    def create_temperature_object(
        data_type: str, **kwargs
    ) -> Union[TemperatureMonthly]:
        """
        Creates a Temperature object based on the data type.

        Args:
            data_type (str): The type of temperature object to create ("monthly" supported only).
            **kwargs: Additional arguments to pass to the constructor.

        Returns:
            Union[TemperatureMonthly, TemperatureDaily]: The created temperature object.

        Raises:
            ValueError: If the data type is not supported.
        """
        if data_type == "monthly":
            return TemperatureMonthly(**kwargs)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
