from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.CarUsageType import CarUsageType
    from msgspec_schemaorg.enums.intangible.DriveWheelConfigurationValue import DriveWheelConfigurationValue
    from msgspec_schemaorg.models.intangible.EngineSpecification import EngineSpecification
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.enums.intangible.SteeringPositionValue import SteeringPositionValue
from datetime import date
from typing import Optional, Union, Dict, List, Any


class Vehicle(Product):
    """A vehicle is a device that is designed or used to transport people or cargo over land, water, air, or through space."""
    type: str = field(default_factory=lambda: "Vehicle", name="@type")
    fuelType: Union[List[Union['URL', str, 'QualitativeValue']], Union['URL', str, 'QualitativeValue'], None] = None
    fuelConsumption: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    mileageFromOdometer: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    vehicleInteriorType: Union[List[str], str, None] = None
    fuelEfficiency: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    vehicleModelDate: Union[List[date], date, None] = None
    cargoVolume: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    vehicleSeatingCapacity: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    numberOfForwardGears: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    seatingCapacity: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    emissionsCO2: Union[List[int | float], int | float, None] = None
    productionDate: Union[List[date], date, None] = None
    steeringPosition: Union[List['SteeringPositionValue'], 'SteeringPositionValue', None] = None
    numberOfDoors: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    tongueWeight: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    purchaseDate: Union[List[date], date, None] = None
    vehicleEngine: Union[List['EngineSpecification'], 'EngineSpecification', None] = None
    vehicleTransmission: Union[List[Union['URL', str, 'QualitativeValue']], Union['URL', str, 'QualitativeValue'], None] = None
    payload: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    vehicleIdentificationNumber: Union[List[str], str, None] = None
    dateVehicleFirstRegistered: Union[List[date], date, None] = None
    driveWheelConfiguration: Union[List[Union[str, 'DriveWheelConfigurationValue']], Union[str, 'DriveWheelConfigurationValue'], None] = None
    meetsEmissionStandard: Union[List[Union['URL', str, 'QualitativeValue']], Union['URL', str, 'QualitativeValue'], None] = None
    vehicleSpecialUsage: Union[List[Union[str, 'CarUsageType']], Union[str, 'CarUsageType'], None] = None
    fuelCapacity: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    knownVehicleDamages: Union[List[str], str, None] = None
    trailerWeight: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    weightTotal: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfAirbags: Union[List[Union[int | float, str]], Union[int | float, str], None] = None
    vehicleConfiguration: Union[List[str], str, None] = None
    callSign: Union[List[str], str, None] = None
    accelerationTime: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    numberOfAxles: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    modelDate: Union[List[date], date, None] = None
    bodyType: Union[List[Union['URL', str, 'QualitativeValue']], Union['URL', str, 'QualitativeValue'], None] = None
    vehicleInteriorColor: Union[List[str], str, None] = None
    numberOfPreviousOwners: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    wheelbase: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    speed: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None