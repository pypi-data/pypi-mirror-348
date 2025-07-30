# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

from ph_units.unit_types._base import Base_UnitType


class WattHour(Base_UnitType):
    """Wh"""

    __symbol__ = "WH"
    __aliases__ = ["WATT-HOUR", "WATT-HOURS", "WHR"]
    __factors__ = {
        "BTU": "{}*3.41214",
        "KBTU": "{}*0.00341214",
        "WH": "{}*1",
        "KWH": "{}*0.001",
        "J": "{}*3600",
        "KJ": "{}*3.6",
        "MJ": "{}*0.0036",
        "GJ": "{}*0.0000036",
        "THERM": "{}*0.0000341214115648838",
    }


class KiloWattHour(Base_UnitType):
    """KWH"""

    __symbol__ = "KWH"
    __aliases__ = ["KWHR", "KWH/YR", "KWH/A", "KWH/M", "KWH/MONTH"]
    __factors__ = {
        "BTU": "{}*3412.14",
        "KBTU": "{}*3.41214",
        "WH": "{}*1000",
        "KWH": "{}*1",
        "J": "{}*3600000",
        "KJ": "{}*3600",
        "MJ": "{}*3.6",
        "GJ": "{}*0.0036",
        "THERM": "{}*0.0341214115648838",
    }


class BTU(Base_UnitType):
    """BTU"""

    __symbol__ = "BTU"
    __aliases__ = []
    __factors__ = {
        "BTU": "{}*1",
        "KBTU": "{}*0.001",
        "WH": "{}*0.293071",
        "KWH": "{}*0.000293071",
        "J": "{}*1055.06",
        "KJ": "{}*1.05506",
        "MJ": "{}*0.00105506",
        "GJ": "{}*0.00000105506",
        "THERM": "{}*0.00001",
    }


class KiloBTU(Base_UnitType):
    """KBTU"""

    __symbol__ = "KBTU"
    __aliases__ = []
    __factors__ = {
        "BTU": "{}*1000",
        "KBTU": "{}*1",
        "WH": "{}*293.071",
        "KWH": "{}*0.293071",
        "J": "{}*1055060",
        "KJ": "{}*1055.06",
        "MJ": "{}*1.05506",
        "GJ": "{}*0.00105506",
        "THERM": "{}*0.01",
    }


class Joule(Base_UnitType):
    """J"""

    __symbol__ = "J"
    __aliases__ = ["JOULE"]
    __factors__ = {
        "BTU": "{}*0.000947817",
        "KBTU": "{}*0.000000947817",
        "WH": "{}*0.000277778",
        "KWH": "{}*0.00000027778 ",
        "J": "{}*1",
        "KJ": "{}*0.001",
        "MJ": "{}*0.000001",
        "GJ": "{}*0.000000001",
        "THERM": "{}*0.0000000094781698791",
    }


class KiloJoule(Base_UnitType):
    """KJ"""

    __symbol__ = "KJ"
    __aliases__ = ["KILOJOULE"]
    __factors__ = {
        "BTU": "{}*0.947817",
        "KBTU": "{}*0.000947817",
        "WH": "{}*0.277778",
        "KWH": "{}*0.000277778",
        "J": "{}*1000",
        "KJ": "{}*1",
        "MJ": "{}*0.001",
        "GJ": "{}*0.000001",
        "THERM": "{}*0.00000947817",
    }


class MegaJoule(Base_UnitType):
    """MJ"""

    __symbol__ = "MJ"
    __aliases__ = ["MEGAJOULE"]
    __factors__ = {
        "BTU": "{}*947.817",
        "KBTU": "{}*0.947817",
        "WH": "{}*277.778",
        "KWH": "{}*0.277778",
        "J": "{}*1000000",
        "KJ": "{}*1000",
        "MJ": "{}*1",
        "GJ": "{}*0.001",
        "THERM": "{}*0.00947817",
    }


class GigaJoule(Base_UnitType):
    """GJ"""

    __symbol__ = "GJ"
    __aliases__ = ["GIGAJOULE"]
    __factors__ = {
        "BTU": "{}*947817.120313",
        "KBTU": "{}*947.817120313",
        "WH": "{}*277777.778",
        "KWH": "{}*277.778",
        "J": "{}*1000000000",
        "KJ": "{}*1000000",
        "MJ": "{}*1000",
        "GJ": "{}*1",
        "THERM": "{}*9.47817120313",
    }


class Therm(Base_UnitType):
    """THERM"""

    __symbol__ = "THERM"
    __aliases__ = ["THERMS"]
    __factors__ = {
        "BTU": "{}*100000",
        "KBTU": "{}*100",
        "WH": "{}*29_307.11111111",
        "KWH": "{}*29.307111111111",
        "J": "{}*105_505_600",
        "KJ": "{}*105505.60000",
        "MJ": "{}*105.50560000",
        "GJ": "{}*0.10550560000",
        "THERM": "{}*1",
    }


# ----------------- Energy Per Person ---------------


class KiloWattHourPerPerson(Base_UnitType):
    """KWH/PERSON"""

    __symbol__ = "KWH/PERSON"
    __aliases__ = ["KWH/PERSON-YR", "KWH/PERSON-A", "KWH/PERSON-MONTH"]
    __factors__ = {
        "WH/PERSON": "{}*1000",
        "KWH/PERSON": "{}*1",
        "BTU/PERSON": "{}*3412.14",
        "KBTU/PERSON": "{}*3.41214",
        "MJ/PERSON": "{}*3.6",
        "KJ/PERSON": "{}*3600",
    }


class KiloBTUPerPerson(Base_UnitType):
    """KBTU/PERSON"""

    __symbol__ = "KBTU/PERSON"
    __aliases__ = []
    __factors__ = {
        "WH/PERSON": "{}*293.071",
        "KWH/PERSON": "{}*0.293071",
        "BTU/PERSON": "{}*1000",
        "KBTU/PERSON": "{}*1",
        "MJ/PERSON": "{}*1.05506",
        "KJ/PERSON": "{}*1055.06",
    }


# ----------------- Energy Per Area -----------------


class WattHoursPerKilometerSquared(Base_UnitType):
    """WH/KM2"""

    __symbol__ = "WH/KM2"
    __aliases__ = []
    __factors__ = {"WH/KM2": "{}*1", "BTU/FT2": "{}*0.000000317"}


class WattHoursPerMeterSquared(Base_UnitType):
    """WH/M2"""

    __symbol__ = "WH/M2"
    __aliases__ = []
    __factors__ = {
        "WH/M2": "{}*1",
        "WH/FT2": "{}*0.092903",
        "KWH/M2": "{}*0.001",
        "KWH/FT2": "{}*0.000092903",
        "BTU/FT2": "{}*0.316998",
        "KBTU/FT2": "{}*0.000316998",
    }


class WattHoursPerFootSquared(Base_UnitType):
    """WH/FT2"""

    __symbol__ = "WH/FT2"
    __aliases__ = []
    __factors__ = {
        "WH/M2": "{}*10.7639",
        "WH/FT2": "{}*1",
        "KWH/M2": "{}*0.0107639",
        "KWH/FT2": "{}*0.001",
        "BTU/FT2": "{}*3.413",
        "KBTU/FT2": "{}*0.003413",
    }


class KiloWattHoursPerFootSquared(Base_UnitType):
    """KWH/FT2"""

    __symbol__ = "KWH/FT2"
    __aliases__ = ["KWH/SF", "KWH/FT²"]
    __factors__ = {
        "WH/M2": "{}*10763.9",
        "WH/FT2": "{}*1000",
        "KWH/M2": "{}*10.7639",
        "KWH/FT2": "{}*1",
        "BTU/FT2": "{}*3413",
        "KBTU/FT2": "{}*3.413",
    }


class KiloWattHoursPerInchSquared(Base_UnitType):
    """KWH/IN2"""

    __symbol__ = "KWH/IN2"
    __aliases__ = ["KWH/IN²", "KWH/SQ-Inch", "KWH/SQ-Inches"]
    __factors__ = {
        "WH/M2": "({}*1000)/0.00064516",
        "WH/FT2": "{}*1000*144",
        "KWH/M2": "{}*1_550.0031000062001",
        "KWH/IN2": "{}*1",
        "KWH/FT2": "{}*144",
        "BTU/FT2": "{}*3412.142*144",
        "KBTU/FT2": "{}*3.412142*144",
    }


class KilowattHoursPerMeterSquared(Base_UnitType):
    """KWH/M2"""

    __symbol__ = "KWH/M2"
    __aliases__ = ["KWH/M²MONTH", "KWH/M²A", "KWH/M²"]
    __factors__ = {
        "WH/M2": "{}*1000",
        "WH/FT2": "{}*92.903",
        "KWH/M2": "{}*1",
        "KWH/IN2": "{}*(1/1550.0031)",
        "KWH/FT2": "{}*0.092903040",
        "BTU/FT2": "{}*316.998330628",
        "KBTU/FT2": "{}*0.316998286",
    }


class KBtuPerFootSquared(Base_UnitType):
    """KBTU/FT2"""

    __symbol__ = "KBTU/FT2"
    __aliases__ = ["KBTU/SF", "KBTU/FT²MONTH", "KBTU/FT²YR", "KBTU/FT²A", "KBTU/FT²"]
    __factors__ = {
        "WH/M2": "{}*3154.59",
        "WH/FT2": "{}*293.071",
        "KWH/M2": "{}*3.15459",
        "KWH/FT2": "{}*0.293071",
        "BTU/FT2": "{}*1000",
        "KBTU/FT2": "{}*1",
    }


class BtuPerFootSquared(Base_UnitType):
    """BTU/FT2"""

    __symbol__ = "BTU/FT2"
    __aliases__ = ["BTU/SF", "BTU/FT²"]
    __factors__ = {
        "WH/M2": "{}*3.15459",
        "WH/FT2": "{}*0.293071",
        "KWH/M2": "{}*0.00315459",
        "KWH/FT2": "{}*0.000293071",
        "BTU/FT2": "{}*1",
        "KBTU/FT2": "{}*0.001",
    }


# ----------------- Energy Per Volume -----------------


class WattHoursPerMeterCubed(Base_UnitType):
    """WH/M3"""

    __symbol__ = "WH/M3"
    __aliases__ = ["WH/M³"]
    __factors__ = {"WH/M3": "{}*1", "W/CFM": "{}*1.699010796"}


class MegaJoulePerMeterCubedKelvin(Base_UnitType):
    """MJ/M3K"""

    __symbol__ = "MJ/M3K"
    __aliases__ = []
    __factors__ = {"MJ/M3K": "{}*1", "BTU/FT3F": "{}*14.91066014"}


class BtuPerFootCubedDegreeFarenheirt(Base_UnitType):
    """BTU/FT3F"""

    __symbol__ = "BTU/FT3F"
    __aliases__ = ["BTU/FT3°F"]
    __factors__ = {"MJ/M3K": "{}*0.067066112", "BTU/FT3F": "{}*1"}


# ----------------- Energy Per Mass -----------------


class JoulePerKilogramDegreeKelvin(Base_UnitType):
    """J/KG-K"""

    __symbol__ = "J/KGK"
    __aliases__ = ["J/KG-K"]
    __factors__ = {"J/KGK": "{}*1", "BTU/LBF": "{}*0.000238846"}


class BtuPerPoundDegreeFarenheirt(Base_UnitType):
    """BTU/LB-F"""

    __symbol__ = "BTU/LBF"
    __aliases__ = ["BTU/LB-F", "BTU/LB°F"]
    __factors__ = {"J/KGK": "{}*4186.800585", "BTU/LBF": "{}*1"}


class WattHoursPerFootSquaredDegreeFarenheirt(Base_UnitType):
    """WH/FT2F"""

    __symbol__ = "WH/FT2F"
    __aliases__ = ["WH/FT2-F", "WH/FT2°F", "WH/FT²F"]
    __factors__ = {
        "WH/M2K": "{}*19.37503875",
        "WH/FT2F": "{}*1",
        "BTU/FT2F": "{}*3.412141156",
    }


class WattHoursPerMeterSqauredPerDegreeKelvin(Base_UnitType):
    """WH/M2K"""

    __symbol__ = "WH/M2K"
    __aliases__ = ["WH/M2K", "WH/M²K"]
    __factors__ = {
        "WH/M2K": "{}*1",
        "WH/FT2F": "{}*0.0516128",
        "BTU/FT2F": "{}*0.1761102",
    }


class BtuPerSquareFootDegreeFarenheirt(Base_UnitType):
    """BTU/FT2-F"""

    __symbol__ = "BTU/FT2F"
    __aliases__ = ["BTU/FT2-F", "BTU/FT2°F", "BTU/FT²F"]
    __factors__ = {
        "BTU/FT2F": "{}*1",
        "WH/FT2F": "{}*0.293071111",
        "WH/M2K": "{}*5.678264134",
    }


# ----------------- Primary Energy Factors -----------------


class KiloWattHourPerKiloWattHour(Base_UnitType):
    """KWH/KWH"""

    __symbol__ = "KWH/KWH"
    __aliases__ = ["KWH/KWH"]
    __factors__ = {"KWH/KWH": "{}*1", "BTU/BTU": "{}*1"}


class BtuPerBtu(Base_UnitType):
    """BTU/BTU"""

    __symbol__ = "BTU/BTU"
    __aliases__ = ["BTU/BTU"]
    __factors__ = {"KWH/KWH": "{}*1", "BTU/BTU": "{}*1"}


# ----------------- ENERGY COST ---------------------


class CostPerTherm(Base_UnitType):
    __symbol__ = "COST/THERM"
    __aliases__ = ["COST/THERM"]
    __factors__ = {
        "COST/THERM": "{}*1",
        "COST/KWH": "{}/29.307111111111",
    }


class CostPerKiloWattHour(Base_UnitType):
    __symbol__ = "COST/KWH"
    __aliases__ = ["COST/KWH"]
    __factors__ = {
        "COST/KWH": "{}*1",
        "COST/THERM": "{}*29.307111111111",
    }
