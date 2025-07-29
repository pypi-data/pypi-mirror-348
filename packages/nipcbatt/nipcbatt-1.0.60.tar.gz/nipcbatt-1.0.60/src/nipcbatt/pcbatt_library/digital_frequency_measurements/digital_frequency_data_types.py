""" Digital Frequency Measurement data types """  # noqa: D415, W505 - First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (159 > 100 characters) (auto-generated noqa)

from varname import nameof

from nipcbatt.pcbatt_library_core.pcbatt_data_types import PCBATestToolkitData
from nipcbatt.pcbatt_utilities.guard_utilities import Guard


class DigitalFrequencyRangeParameters(PCBATestToolkitData):
    """Defines the values used to establish the frequency range"""  # noqa: D415, W505 - First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (177 > 100 characters) (auto-generated noqa)

    def __init__(
        self, frequency_minimum_value_hertz: float, frequency_maximum_value_hertz: float
    ) -> None:
        """Initializes an instance of 'DigitalFrequencyRangeParameters'
           with specific values

        Args:
            frequency_minimum_value_hertz (float):
                The minimum value in the frequency range
            frequency_maximum_vlaue_hertz (float):
                The maximum value in the frequency range

        Raises: ValueError when,
            1) The value of frequency_minimum_value_hertz is None or is <= 0
            2) The value of frequency_maximum_vlue_hertz is None or is <= 0
        """  # noqa: D202, D205, D415, D417, W505 - No blank lines allowed after function docstring (auto-generated noqa), 1 blank line required between summary line and description (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), Missing argument descriptions in the docstring (auto-generated noqa), doc line too long (363 > 100 characters) (auto-generated noqa)

        # input validation
        Guard.is_not_none(frequency_minimum_value_hertz, nameof(frequency_minimum_value_hertz))
        Guard.is_greater_than_or_equal_to_zero(
            frequency_minimum_value_hertz, nameof(frequency_minimum_value_hertz)
        )

        Guard.is_not_none(frequency_maximum_value_hertz, nameof(frequency_maximum_value_hertz))
        Guard.is_greater_than_or_equal_to_zero(
            frequency_maximum_value_hertz, nameof(frequency_maximum_value_hertz)
        )

        # minimum frequency <= maximum frequency
        Guard.is_less_than_or_equal_to(
            frequency_minimum_value_hertz,
            frequency_maximum_value_hertz,
            "minimum frequency <= maximum frequency",
        )

        # assign to member variables
        self._frequency_minimum_value_hertz = frequency_minimum_value_hertz
        self._frequency_maximum_value_hertz = frequency_maximum_value_hertz

    @property
    def frequency_minimum_value_hertz(self) -> float:
        """
        :type:'float': Gets the minimum frquency in the range
        """  # noqa: D212, D415, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (211 > 100 characters) (auto-generated noqa)
        return self._frequency_minimum_value_hertz

    @property
    def frequency_maximum_value_hertz(self) -> float:
        """
        :type:'float': Gets the maximum frquency in the range
        """  # noqa: D212, D415, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (211 > 100 characters) (auto-generated noqa)
        return self._frequency_maximum_value_hertz


class DigitalFrequencyMeasurementCounterChannelParameters(PCBATestToolkitData):
    """Defines the values for frequency counter channels"""  # noqa: D415, W505 - First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (170 > 100 characters) (auto-generated noqa)

    def __init__(
        self,
        range_parameters: DigitalFrequencyRangeParameters,
        input_divisor_for_frequency_measurement: int,
        measurement_duration_seconds: float,
    ) -> None:
        """Initializes an instance of DigitalFrequencyMeasurementCounterChannelParameters

        Args:
            range_parameters (DigitalFrequencyRangeParameters): frequency range used in
              measurement. Defined by min frequency and max frequency.
            input_divisor_for_frequency_measurement (float): Divisor used for measurements
            measurement_duration_seconds (float): Length of capture

        Raises: ValueError when,
            1) The value of frequency_minimum_value_hertz is None or <= 0
            2) The value of frequency_maximum_value_hertz is None or <= 0
            3) The value of input_divisor_for_frequency_measurement is None or <= 4
            4) The value of measurement_duration_seconds is None or <= 0
        """  # noqa: D202, D415, W505 - No blank lines allowed after function docstring (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (199 > 100 characters) (auto-generated noqa)

        # input validation
        Guard.is_not_none(range_parameters, nameof(range_parameters))

        Guard.is_not_none(
            input_divisor_for_frequency_measurement,
            nameof(input_divisor_for_frequency_measurement),
        )
        Guard.is_greater_than_or_equal_to(
            input_divisor_for_frequency_measurement,
            4,
            nameof(input_divisor_for_frequency_measurement),
        )

        Guard.is_not_none(measurement_duration_seconds, nameof(measurement_duration_seconds))
        Guard.is_greater_than_zero(
            measurement_duration_seconds, nameof(measurement_duration_seconds)
        )

        # set member variables
        self._range_parameters = range_parameters
        self._input_divisor_for_frequency_measurement = input_divisor_for_frequency_measurement
        self._measurement_duration_seconds = measurement_duration_seconds

    @property
    def range_parameters(self) -> DigitalFrequencyRangeParameters:
        """
        :type:'DigitalFrequencyRangeParameters': Holds the frequency range
        """  # noqa: D212, D415, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (211 > 100 characters) (auto-generated noqa)
        return self._range_parameters

    @property
    def input_divisor_for_frequency_measurement(self) -> int:
        """
        :type:'int': The divisor used for measuring frequency
        """  # noqa: D212, D415, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (211 > 100 characters) (auto-generated noqa)
        return self._input_divisor_for_frequency_measurement

    @property
    def measurement_duration_seconds(self) -> float:
        """
        :type:'float': The duration of the measurement in seconds
        """  # noqa: D212, D415, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (211 > 100 characters) (auto-generated noqa)
        return self._measurement_duration_seconds


class DigitalFrequencyMeasurementConfiguration(PCBATestToolkitData):
    """Defines the values used in the creation of a Digital Frequency Measurement"""  # noqa: D415, W505 - First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (195 > 100 characters) (auto-generated noqa)

    def __init__(
        self,
        counter_channel_configuration_parameters: DigitalFrequencyMeasurementCounterChannelParameters,
    ) -> None:
        """Initializes an instance of 'DigitalFrequencyMeasurementConfiguration'
           with specific values

        Args:
            configuration_parameters: An instance of
            'DigitalFrequencyMeasurementCounterChannelParameters'

        Raises: ValueError when,
            1) The value of configuration_parameters is None
        """  # noqa: D202, D205, D415, D417, W505 - No blank lines allowed after function docstring (auto-generated noqa), 1 blank line required between summary line and description (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), Missing argument descriptions in the docstring (auto-generated noqa), doc line too long (363 > 100 characters) (auto-generated noqa)

        # input validation
        Guard.is_not_none(
            counter_channel_configuration_parameters,
            nameof(counter_channel_configuration_parameters),
        )

        # assign member variables
        self._configuration_parameters = counter_channel_configuration_parameters

    @property
    def counter_channel_configuration_parameters(
        self,
    ) -> DigitalFrequencyMeasurementCounterChannelParameters:
        """
        :type:'DigitalFrequencyMeasurementCounterChannelParameters': Holds the
        configuration parameters used for this measurement
        """  # noqa: D205, D212, D415, W505 - 1 blank line required between summary line and description (auto-generated noqa), Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (299 > 100 characters) (auto-generated noqa)
        return self._configuration_parameters


class DigitalFrequencyMeasurementResultData:
    """Defines the values inside a digital frequency result"""  # noqa: D415, W505 - First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (173 > 100 characters) (auto-generated noqa)

    def __init__(self, frequency: float):
        """Instantiates a DigitalFrequencyMeasurementResultData object
           with the value provided in the frequency argument

        Args:
            frequency (float): The measured digital frequency

        Raises:
            ValueError when the frequency is None or <= 0
        """  # noqa: D202, D205, D415, W505 - No blank lines allowed after function docstring (auto-generated noqa), 1 blank line required between summary line and description (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (287 > 100 characters) (auto-generated noqa)

        # input validation
        Guard.is_not_none(frequency, nameof(frequency))
        Guard.is_greater_than_or_equal_to_zero(frequency, nameof(frequency))

        # set member variable
        self._frequency = frequency

    @property
    def frequency(self) -> float:
        """
        :type:'float': The frequency captured in the measurement
        """  # noqa: D212, D415, W505 - Multi-line docstring summary should start at the first line (auto-generated noqa), First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (211 > 100 characters) (auto-generated noqa)
        return self._frequency
