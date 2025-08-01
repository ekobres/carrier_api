from logging import getLogger
from dateutil.parser import isoparse
from datetime import datetime

from .const import SystemModes, TemperatureUnits, FanModes, ActivityTypes
from .util import safely_get_json_value

_LOGGER = getLogger(__name__)


class StatusZone:
    def __init__(self, status_zone_json: dict):
        self.api_id = safely_get_json_value(status_zone_json, "id", str)
        self.name: str = safely_get_json_value(status_zone_json, "name")
        self.current_activity: ActivityTypes = ActivityTypes(status_zone_json["currentActivity"])
        self.temperature: float = safely_get_json_value(status_zone_json, "rt", float)
        self.humidity: int = safely_get_json_value(status_zone_json, "rh", int)
        self.occupancy: bool = safely_get_json_value(status_zone_json, "occupancy") == "occupied"
        self.fan: FanModes = FanModes(status_zone_json["fan"])
        self.hold: bool = safely_get_json_value(status_zone_json, "hold") == "on"
        self.hold_until: str = safely_get_json_value(status_zone_json, "otmr")
        self.heat_set_point: float = safely_get_json_value(status_zone_json, "htsp", float)
        self.cool_set_point: float = safely_get_json_value(status_zone_json, "clsp", float)
        self.conditioning: str = safely_get_json_value(status_zone_json, "zoneconditioning")

    @property
    def zone_conditioning_const(self) -> SystemModes:
        match self.conditioning:
            case "active_heat" | "prep_heat" | "pending_heat":
                return SystemModes.HEAT
            case "active_cool" | "prep_cool" | "pending_cool":
                return SystemModes.COOL
            case "idle":
                return SystemModes.OFF
        raise ValueError(f"Unknown conditioning: {self.conditioning}")

    def __repr__(self):
        return {
            "id": self.api_id,
            "name": self.name,
            "current_activity": self.current_activity.value,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "fan": self.fan.value,
            "hold": self.hold,
            "occupancy": self.occupancy,
            "hold_until": self.hold_until,
            "heat_set_point": self.heat_set_point,
            "cool_set_point": self.cool_set_point,
            "conditioning": self.conditioning,
        }

    def __str__(self):
        return str(self.__repr__())



class StatusODU:
    """Represents the status of the Outdoor Unit (ODU)."""

    def __init__(self, raw: dict):
        self.raw = raw  # Set self.raw to the passed ODU data

        # Assign values from the JSON
        self.type = safely_get_json_value(self.raw, "type", str)
        self.operational_status = safely_get_json_value(self.raw, "opstat", str)
        self.idu_cfm = safely_get_json_value(self.raw, "iducfm", int)
        self.odu_coil_temp = safely_get_json_value(self.raw, "oducoiltmp", float)
        self.blower_rpm = safely_get_json_value(self.raw, "blwrpm", int)
        self.line_voltage = safely_get_json_value(self.raw, "linevolt", int)
        self.compressor_rpm = safely_get_json_value(self.raw, "comprpm", int)
        self.suction_pressure = safely_get_json_value(self.raw, "suctpress", int)
        self.suction_temp = safely_get_json_value(self.raw, "sucttemp", float)
        self.suction_superheat = safely_get_json_value(self.raw, "suctsupheat", float)
        self.discharge_temp = safely_get_json_value(self.raw, "dischargetmp", float)
        self.exv_position = safely_get_json_value(self.raw, "exvpos", int)
        self.ac_line_current = safely_get_json_value(self.raw, "aclinecurrent", float)
        self.dc_bus_voltage = safely_get_json_value(self.raw, "dcbusvoltage", float)
        self.discharge_pressure = safely_get_json_value(self.raw, "dischargepressure", float)
        self.discharge_superheat = safely_get_json_value(self.raw, "dischargesuperheat", float)
        self.ipm_temperature = safely_get_json_value(self.raw, "ipmtemperature", float)
        self.pfcm_temperature = safely_get_json_value(self.raw, "pfcmtemperature", float)
        self.outdoor_fan_rpm = safely_get_json_value(self.raw, "outdoorfanrpm", int)

    def __repr__(self):
        return {
            "type": self.type,
            "operational_status": self.operational_status,
            "idu_cfm": self.idu_cfm,
            "odu_coil_temp": self.odu_coil_temp,
            "blower_rpm": self.blower_rpm,
            "line_voltage": self.line_voltage,
            "compressor_rpm": self.compressor_rpm,
            "suction_pressure": self.suction_pressure,
            "suction_temp": self.suction_temp,
            "suction_superheat": self.suction_superheat,
            "discharge_temp": self.discharge_temp,
            "exv_position": self.exv_position,
            "ac_line_current": self.ac_line_current,
            "dc_bus_voltage": self.dc_bus_voltage,
            "discharge_pressure": self.discharge_pressure,
            "discharge_superheat": self.discharge_superheat,
            "ipm_temperature": self.ipm_temperature,
            "pfcm_temperature": self.pfcm_temperature,
            "outdoor_fan_rpm": self.outdoor_fan_rpm,
        }

    def __str__(self):
        return str(self.__repr__())

class StatusIDU:
    """Represents the status of the Indoor Unit (IDU)."""

    def __init__(self, raw: dict):
        self.raw = raw  # Set self.raw to the passed IDU data

        # Assign values from the JSON
        self.type = safely_get_json_value(self.raw, "type", str)
        self.operational_status = safely_get_json_value(self.raw, "opstat", str)
        self.airflow_cfm = safely_get_json_value(self.raw, "cfm", int)
        self.static_pressure = safely_get_json_value(self.raw, "statpress", float)
        self.blower_rpm = safely_get_json_value(self.raw, "blwrpm", int)

    def __repr__(self):
        return {
            "type": self.type,
            "operational_status": self.operational_status,
            "airflow_cfm": self.airflow_cfm,
            "static_pressure": self.static_pressure,
            "blower_rpm": self.blower_rpm,
        }

    def __str__(self):
        return str(self.__repr__())

class Status:
    outdoor_temperature: int | None = None
    mode: str | None = None
    temperature_unit: TemperatureUnits | None = None
    filter_used: int | None = None
    is_disconnected: bool | None = None
    airflow_cfm: int | None = None
    blower_rpm: int | None = None
    static_pressure: float | None = None
    humidity_level: int | None = None
    humidifier_on: bool | None = None
    uv_lamp_level: int | None = None
    outdoor_unit_operational_status: str | None = None
    indoor_unit_operational_status: str | None = None
    time_stamp: datetime | None = None
    zones: list[StatusZone] | None = None

    def __init__(
        self,
        raw: dict,
    ):
        self.raw = raw
        self.outdoor_temperature: float = safely_get_json_value(self.raw, "oat", float)
        self.mode: str = safely_get_json_value(self.raw, "mode")
        self.temperature_unit: TemperatureUnits = TemperatureUnits(self.raw["cfgem"])
        self.filter_used: int = safely_get_json_value(self.raw, "filtrlvl", int)
        self.humidity_level: int = safely_get_json_value(self.raw, "humlvl", int)
        if self.raw.get('humid') is not None:
            self.humidifier_on: bool = safely_get_json_value(self.raw, "humid", str) == 'on'
        self.uv_lamp_level: int = safely_get_json_value(self.raw, "uvlvl", int)
        self.is_disconnected: bool = safely_get_json_value(self.raw, "isDisconnected", bool)
        self.airflow_cfm: int = safely_get_json_value(self.raw, "idu.cfm", int)
        self.blower_rpm: int = safely_get_json_value(self.raw, "idu.blwrpm", int)
        self.static_pressure: int = safely_get_json_value(self.raw, "idu.statpress", float)
        self.outdoor_unit_operational_status: str = safely_get_json_value(self.raw, "odu.opstat")
        self.indoor_unit_operational_status: str = safely_get_json_value(self.raw, "idu.opstat")
        self.time_stamp = isoparse(safely_get_json_value(self.raw, "utcTime"))
        self.zones = []
        for zone_json in self.raw["zones"]:
            if safely_get_json_value(zone_json, "enabled") == "on":
                self.zones.append(StatusZone(zone_json))

        self.odu = StatusODU(self.raw.get("odu", {}))
        self.idu = StatusIDU(self.raw.get("idu", {}))

    @property
    def mode_const(self) -> SystemModes:
        match self.mode:
            case "gasheat" | "electric" | "hpheat":
                return SystemModes.HEAT
            case "dehumidify":
                return SystemModes.COOL
        raise ValueError(f"Unknown mode: {self.mode}")

    def __repr__(self):
        return {
            "outdoor_temperature": self.outdoor_temperature,
            "mode": self.mode,
            "temperature_unit": self.temperature_unit.value,
            "filter_used": self.filter_used,
            "is_disconnected": self.is_disconnected,
            "airflow_cfm": self.airflow_cfm,
            "blower_rpm": self.blower_rpm,
            "static_pressure": self.static_pressure,
            "humidity_level": self.humidity_level,
            "humidifier_on": self.humidifier_on,
            "outdoor_unit_operational_status": self.outdoor_unit_operational_status,
            "indoor_unit_operational_status": self.indoor_unit_operational_status,
            "zones": [zone.__repr__() for zone in self.zones],
            "odu": self.odu.__repr__(),  
            "idu": self.idu.__repr__(),  
        }

    def __str__(self):
        return str(self.__repr__())
