"""
Patches for generated CDK bindings.

This module contains patches that override certain types and converters
from the generated cdk.py bindings to provide a better Python experience.
"""

from enum import Enum

try:
    from .cdk import _UniffiConverterUInt64, _UniffiConverterRustBuffer

    Amount = int

    class _UniffiConverterTypeAmount(_UniffiConverterRustBuffer):
        @staticmethod
        def read(buf):
            return _UniffiConverterUInt64.read(buf)

        @staticmethod
        def check_lower(value):
            _UniffiConverterUInt64.check_lower(value)

        @staticmethod
        def write(value, buf):
            _UniffiConverterUInt64.write(value, buf)

except (ImportError, AttributeError):
    pass

try:
    from .cdk import _UniffiConverterString, _UniffiConverterRustBuffer, InternalError

    class CurrencyUnit(Enum):
        SAT = 1
        MSAT = 2
        USD = 3
        EUR = 4
        AUTH = 5
        CUSTOM = 6

        def __new__(cls, value):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.unit = None  # type: ignore[attr-defined]
            return obj

        @staticmethod
        def custom(unit: str):
            obj = object.__new__(CurrencyUnit)
            obj._value_ = CurrencyUnit.CUSTOM.value
            obj._name_ = "CUSTOM"
            obj.unit = unit  # type: ignore[attr-defined]
            return obj

        def is_SAT(self):
            return self is CurrencyUnit.SAT

        def is_MSAT(self):
            return self is CurrencyUnit.MSAT

        def is_USD(self):
            return self is CurrencyUnit.USD

        def is_EUR(self):
            return self is CurrencyUnit.EUR

        def is_AUTH(self):
            return self is CurrencyUnit.AUTH

        def is_CUSTOM(self):
            return self.value == CurrencyUnit.CUSTOM.value

        def __str__(self):
            if self.is_CUSTOM():
                return f"CurrencyUnit.CUSTOM(unit={getattr(self, 'unit', None)})"
            return f"CurrencyUnit.{self.name}()"

        def __eq__(self, other):
            if not isinstance(other, CurrencyUnit):
                return False
            if self.value != other.value:
                return False
            if self.is_CUSTOM():
                return getattr(self, "unit", None) == getattr(other, "unit", None)
            return True

    class _UniffiConverterTypeCurrencyUnit(_UniffiConverterRustBuffer):
        @staticmethod
        def read(buf):
            variant = buf.read_i32()
            if variant == CurrencyUnit.SAT.value:
                return CurrencyUnit.SAT
            if variant == CurrencyUnit.MSAT.value:
                return CurrencyUnit.MSAT
            if variant == CurrencyUnit.USD.value:
                return CurrencyUnit.USD
            if variant == CurrencyUnit.EUR.value:
                return CurrencyUnit.EUR
            if variant == CurrencyUnit.AUTH.value:
                return CurrencyUnit.AUTH
            if variant == CurrencyUnit.CUSTOM.value:
                unit_str = _UniffiConverterString.read(buf)
                return CurrencyUnit.custom(unit_str)
            raise InternalError("Raw enum value doesn't match any cases")

        @staticmethod
        def check_lower(value):
            if value.is_SAT():
                return
            if value.is_MSAT():
                return
            if value.is_USD():
                return
            if value.is_EUR():
                return
            if value.is_AUTH():
                return
            if value.is_CUSTOM():
                _UniffiConverterString.check_lower(getattr(value, "unit", None))
                return
            raise ValueError(value)

        @staticmethod
        def write(value, buf):
            buf.write_i32(value.value)
            if value.is_CUSTOM():
                _UniffiConverterString.write(getattr(value, "unit", None), buf)

except (ImportError, AttributeError):
    pass
