import ctypes
import numpy as np

class WGFMU_class:
    def __init__(self, library_path='C:/Windows/System32/wgfmu.dll'):
        try:
            self._lib = ctypes.WinDLL(library_path)
            self._define_argtypes_restypes()
        except OSError as e:
            self._lib = None
            raise OSError(f"Error loading WGFMU library from {library_path}: {e}")

    # Functions

    # Common - Initialize

    def openSession(self, address: str) -> None:
        """Opens a session with the WGFMU device at the specified address."""
        address_encoded = address.encode('utf-8')
        result = self._lib.WGFMU_openSession(address_encoded)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def closeSession(self) -> None:
        """Closes the current session with the WGFMU device."""
        result = self._lib.WGFMU_closeSession()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def initialize(self) -> None:
        """Initializes the WGFMU device."""
        result = self._lib.WGFMU_initialize()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def setTimeout(self, timeout: float) -> None:
        """Sets the timeout for WGFMU operations in seconds."""
        result = self._lib.WGFMU_setTimeout(timeout)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def doSelfCalibration(self) -> tuple[int, str]:
        """Performs self-calibration of the WGFMU device."""
        result = ctypes.c_int()
        detail_buffer = ctypes.create_string_buffer(2048)  # Assuming a maximum detail size
        size = ctypes.c_int(ctypes.sizeof(detail_buffer))
        calibration_result = self._lib.WGFMU_doSelfCalibration(ctypes.byref(result), detail_buffer, ctypes.byref(size))
        if calibration_result != self.NO_ERROR:
            raise self._handle_error(calibration_result)
        return result.value, detail_buffer.value.decode('utf-8')

    def doSelfTest(self) -> tuple[int, str]:
        """Performs a self-test of the WGFMU device."""
        result = ctypes.c_int()
        detail_buffer = ctypes.create_string_buffer(2048)  # Assuming a maximum detail size
        size = ctypes.c_int(ctypes.sizeof(detail_buffer))
        test_result = self._lib.WGFMU_doSelfTest(ctypes.byref(result), detail_buffer, ctypes.byref(size))
        if test_result != self.NO_ERROR:
            raise self._handle_error(test_result)
        return result.value, detail_buffer.value.decode('utf-8')

    def getChannelIdSize(self) -> int:
        """Gets the number of available channels on the WGFMU device."""
        size = ctypes.c_int()
        result = self._lib.WGFMU_getChannelIdSize(ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getChannelIds(self) -> list[int]:
        """Gets a list of available channel IDs on the WGFMU device."""
        size = self.getChannelIdSize()
        if size > 0:
            channel_ids_array = (ctypes.c_int * size)()
            result_size = ctypes.c_int(size)
            result = self._lib.WGFMU_getChannelIds(channel_ids_array, ctypes.byref(result_size))
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return list(channel_ids_array)
        else:
            return []

    # Common - Error and Warning

    def getErrorSize(self) -> int:
        """Gets the size of the last error message."""
        size = ctypes.c_int()
        result = self._lib.WGFMU_getErrorSize(ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getError(self) -> str:
        """Gets the last error message."""
        size = self.getErrorSize()
        if size > 0:
            error_buffer = ctypes.create_string_buffer(size)
            result = self._lib.WGFMU_getError(error_buffer, ctypes.byref(ctypes.c_int(size)))
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return error_buffer.value.decode('utf-8')
        return ""

    def getErrorSummarySize(self) -> int:
        """Gets the size of the accumulated error summary."""
        size = ctypes.c_int()
        result = self._lib.WGFMU_getErrorSummarySize(ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getErrorSummary(self) -> str:
        """Gets the accumulated error summary."""
        size = self.getErrorSummarySize()
        if size > 0:
            error_summary_buffer = ctypes.create_string_buffer(size)
            result = self._lib.WGFMU_getErrorSummary(error_summary_buffer, ctypes.byref(ctypes.c_int(size)))
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return error_summary_buffer.value.decode('utf-8')
        return ""

    def treatWarningsAsErrors(self, warning_level: int) -> None:
        """Sets the warning level at which warnings should be treated as errors."""
        result = self._lib.WGFMU_treatWarningsAsErrors(warning_level)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def setWarningLevel(self, warning_level: int) -> None:
        """Sets the current warning level."""
        result = self._lib.WGFMU_setWarningLevel(warning_level)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getWarningLevel(self) -> int:
        """Gets the current warning level."""
        warning_level = ctypes.c_int()
        result = self._lib.WGFMU_getWarningLevel(ctypes.byref(warning_level))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return warning_level.value

    def getWarningSummarySize(self) -> int:
        """Gets the size of the accumulated warning summary."""
        size = ctypes.c_int()
        result = self._lib.WGFMU_getWarningSummarySize(ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getWarningSummary(self) -> str:
        """Gets the accumulated warning summary."""
        size = self.getWarningSummarySize()
        if size > 0:
            warning_summary_buffer = ctypes.create_string_buffer(size)
            result = self._lib.WGFMU_getWarningSummary(warning_summary_buffer, ctypes.byref(ctypes.c_int(size)))
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return warning_summary_buffer.value.decode('utf-8')
        return ""

    def openLogFile(self, file_name: str) -> None:
        """Opens a log file for WGFMU operations."""
        file_name_encoded = file_name.encode('utf-8')
        result = self._lib.WGFMU_openLogFile(file_name_encoded)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def closeLogFile(self) -> None:
        """Closes the currently open log file."""
        result = self._lib.WGFMU_closeLogFile()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # Common - Setup

    def setOperationMode(self, channel_id: int, operation_mode: int) -> None:
        """Sets the operation mode for a channel."""
        result = self._lib.WGFMU_setOperationMode(channel_id, operation_mode)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getOperationMode(self, channel_id: int) -> int:
        """Gets the current operation mode for a channel."""
        operation_mode = ctypes.c_int()
        result = self._lib.WGFMU_getOperationMode(channel_id, ctypes.byref(operation_mode))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return operation_mode.value

    def setForceVoltageRange(self, channel_id: int, force_voltage_range: int) -> None:
        """Sets the force voltage range for a channel."""
        result = self._lib.WGFMU_setForceVoltageRange(channel_id, force_voltage_range)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getForceVoltageRange(self, channel_id: int) -> int:
        """Gets the current force voltage range for a channel."""
        force_voltage_range = ctypes.c_int()
        result = self._lib.WGFMU_getForceVoltageRange(channel_id, ctypes.byref(force_voltage_range))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return force_voltage_range.value

    def setMeasureMode(self, channel_id: int, measure_mode: int) -> None:
        """Sets the measure mode for a channel."""
        result = self._lib.WGFMU_setMeasureMode(channel_id, measure_mode)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getMeasureMode(self, channel_id: int) -> int:
        """Gets the current measure mode for a channel."""
        measure_mode = ctypes.c_int()
        result = self._lib.WGFMU_getMeasureMode(channel_id, ctypes.byref(measure_mode))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measure_mode.value

    def setMeasureVoltageRange(self, channel_id: int, measure_voltage_range: int) -> None:
        """Sets the measure voltage range for a channel."""
        result = self._lib.WGFMU_setMeasureVoltageRange(channel_id, measure_voltage_range)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getMeasureVoltageRange(self, channel_id: int) -> int:
        """Gets the current measure voltage range for a channel."""
        measure_voltage_range = ctypes.c_int()
        result = self._lib.WGFMU_getMeasureVoltageRange(channel_id, ctypes.byref(measure_voltage_range))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measure_voltage_range.value

    def setMeasureCurrentRange(self, channel_id: int, measure_current_range: int) -> None:
        """Sets the measure current range for a channel."""
        result = self._lib.WGFMU_setMeasureCurrentRange(channel_id, measure_current_range)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getMeasureCurrentRange(self, channel_id: int) -> int:
        """Gets the current measure current range for a channel."""
        measure_current_range = ctypes.c_int()
        result = self._lib.WGFMU_getMeasureCurrentRange(channel_id, ctypes.byref(measure_current_range))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measure_current_range.value

    def setForceDelay(self, channel_id: int, force_delay: float) -> None:
        """Sets the delay before forcing a value on a channel."""
        result = self._lib.WGFMU_setForceDelay(channel_id, force_delay)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getForceDelay(self, channel_id: int) -> float:
        """Gets the current delay before forcing a value on a channel."""
        force_delay = ctypes.c_double()
        result = self._lib.WGFMU_getForceDelay(channel_id, ctypes.byref(force_delay))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return force_delay.value

    def setMeasureDelay(self, channel_id: int, measure_delay: float) -> None:
        """Sets the delay before taking a measurement on a channel."""
        result = self._lib.WGFMU_setMeasureDelay(channel_id, measure_delay)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getMeasureDelay(self, channel_id: int) -> float:
        """Gets the current delay before taking a measurement on a channel."""
        measure_delay = ctypes.c_double()
        result = self._lib.WGFMU_getMeasureDelay(channel_id, ctypes.byref(measure_delay))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measure_delay.value

    def setMeasureEnabled(self, channel_id: int, measure_enabled: int) -> None:
        """Enables or disables measurement for a channel."""
        result = self._lib.WGFMU_setMeasureEnabled(channel_id, measure_enabled)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def isMeasureEnabled(self, channel_id: int) -> bool:
        """Checks if measurement is enabled for a channel."""
        measure_enabled = ctypes.c_int()
        result = self._lib.WGFMU_isMeasureEnabled(channel_id, ctypes.byref(measure_enabled))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return bool(measure_enabled.value)

    def setTriggerOutMode(self, channel_id: int, trigger_out_mode: int, polarity: int) -> None:
        """Sets the trigger output mode and polarity for a channel."""
        result = self._lib.WGFMU_setTriggerOutMode(channel_id, trigger_out_mode, polarity)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getTriggerOutMode(self, channel_id: int) -> tuple[int, int]:
        """Gets the current trigger output mode and polarity for a channel."""
        trigger_out_mode = ctypes.c_int()
        polarity = ctypes.c_int()
        result = self._lib.WGFMU_getTriggerOutMode(channel_id, ctypes.byref(trigger_out_mode), ctypes.byref(polarity))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return trigger_out_mode.value, polarity.value

    # Common - Measurement

    def connect(self, channel_id: int) -> None:
        """Connects the specified channel of the WGFMU."""
        result = self._lib.WGFMU_connect(channel_id)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def disconnect(self, channel_id: int) -> None:
        """Disconnects the specified channel of the WGFMU."""
        result = self._lib.WGFMU_disconnect(channel_id)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Initialize

    def clear(self) -> None:
        """Clears all configured settings, patterns, and sequences on the WGFMU."""
        result = self._lib.WGFMU_clear()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Setup - Pattern

    def createPattern(self, pattern_name: str, initial_voltage: float) -> None:
        """Creates a new waveform pattern with an initial voltage."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        result = self._lib.WGFMU_createPattern(pattern_name_encoded, initial_voltage)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def addVector(self, pattern_name: str, delta_time: float, voltage: float) -> None:
        """Adds a single vector (time increment and voltage) to an existing pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        result = self._lib.WGFMU_addVector(pattern_name_encoded, delta_time, voltage)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def addVectors(self, pattern_name: str, delta_times: list[float], voltages: list[float]) -> None:
        """Adds multiple vectors to an existing pattern."""
        if len(delta_times) != len(voltages):
            raise ValueError("The number of delta times must match the number of voltages.")
        size = len(delta_times)
        pattern_name_encoded = pattern_name.encode('utf-8')
        delta_times_array = (ctypes.c_double * size)(*delta_times)
        voltages_array = (ctypes.c_double * size)(*voltages)
        result = self._lib.WGFMU_addVectors(
            pattern_name_encoded,
            delta_times_array,
            voltages_array,
            size,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def setVector(self, pattern_name: str, time: float, voltage: float) -> None:
        """Sets the voltage at a specific time within an existing pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        result = self._lib.WGFMU_setVector(pattern_name_encoded, time, voltage)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def setVectors(self, pattern_name: str, times: list[float], voltages: list[float]) -> None:
        """Sets the voltages at specific times within an existing pattern."""
        if len(times) != len(voltages):
            raise ValueError("The number of times must match the number of voltages.")
        size = len(times)
        pattern_name_encoded = pattern_name.encode('utf-8')
        times_array = (ctypes.c_double * size)(*times)
        voltages_array = (ctypes.c_double * size)(*voltages)
        result = self._lib.WGFMU_setVectors(
            pattern_name_encoded,
            times_array,
            voltages_array,
            size,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Setup - Pattern Opeartion

    def createMergedPattern(self, pattern_name: str, pattern1: str, pattern2: str, axis: int) -> None:
        """Creates a new pattern by merging two existing patterns."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        pattern1_encoded = pattern1.encode('utf-8')
        pattern2_encoded = pattern2.encode('utf-8')
        result = self._lib.WGFMU_createMergedPattern(
            pattern_name_encoded,
            pattern1_encoded,
            pattern2_encoded,
            axis,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def createMultipliedPattern(self, pattern_name: str, pattern1: str, time_factor: float,
                                voltage_factor: float) -> None:
        """Creates a new pattern by multiplying an existing pattern's time and voltage values."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        pattern1_encoded = pattern1.encode('utf-8')
        result = self._lib.WGFMU_createMultipliedPattern(
            pattern_name_encoded,
            pattern1_encoded,
            time_factor,
            voltage_factor,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def createOffsetPattern(self, pattern_name: str, pattern1: str, time_offset: float, voltage_offset: float) -> None:
        """Creates a new pattern by offsetting an existing pattern's time and voltage values."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        pattern1_encoded = pattern1.encode('utf-8')
        result = self._lib.WGFMU_createOffsetPattern(
            pattern_name_encoded,
            pattern1_encoded,
            time_offset,
            voltage_offset,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Setup - Event

    def setMeasureEvent(
            self,
            pattern_name: str,
            event_name: str,
            time: float,
            measurement_points: int,
            measurement_interval: float,
            averaging_time: float,
            raw_data: int,
    ) -> None:
        """Sets a measure event for a specific pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        event_name_encoded = event_name.encode('utf-8')
        result = self._lib.WGFMU_setMeasureEvent(
            pattern_name_encoded,
            event_name_encoded,
            time,
            measurement_points,
            measurement_interval,
            averaging_time,
            raw_data,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def setRangeEvent(self, pattern_name: str, event_name: str, time: float, range_index: int) -> None:
        """Sets a range change event for a specific pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        event_name_encoded = event_name.encode('utf-8')
        result = self._lib.WGFMU_setRangeEvent(
            pattern_name_encoded,
            event_name_encoded,
            time,
            range_index,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def setTriggerOutEvent(self, pattern_name: str, event_name: str, time: float, duration: float) -> None:
        """Sets a trigger output event for a specific pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        event_name_encoded = event_name.encode('utf-8')
        result = self._lib.WGFMU_setTriggerOutEvent(
            pattern_name_encoded,
            event_name_encoded,
            time,
            duration,
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Setup - Sequence

    def addSequence(self, channel_id: int, pattern_name: str, loop_count: float) -> None:
        """Adds a single pattern to the sequence for a channel."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        result = self._lib.WGFMU_addSequence(channel_id, pattern_name_encoded, loop_count)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def addSequences(self, channel_id: int, pattern_names: list[str], loop_counts: list[float]) -> None:
        """Adds multiple patterns to the sequence for a channel."""
        if len(pattern_names) != len(loop_counts):
            raise ValueError("The number of pattern names must match the number of loop counts.")
        size = len(pattern_names)
        pattern_names_encoded = [(name.encode('utf-8')) for name in pattern_names]
        pattern_names_ptr_array = (ctypes.c_char_p * size)(*pattern_names_encoded)
        loop_counts_array = (ctypes.c_double * size)(*loop_counts)

        result = self._lib.WGFMU_addSequences(
            channel_id,
            ctypes.cast(pattern_names_ptr_array, ctypes.POINTER(ctypes.c_char_p)),
            loop_counts_array,
            size
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Setup Check - Pattern

    def getPatternForceValueSize(self, pattern_name: str) -> int:
        """Gets the size of the force value array for a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        size = ctypes.c_int()
        result = self._lib.WGFMU_getPatternForceValueSize(pattern_name_encoded, ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getPatternForceValues(self, pattern_name: str, offset: int = 0) -> tuple[np.ndarray, np.ndarray]:
        """Retrieves the time and force value vectors for a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        size = self.getPatternForceValueSize(pattern_name)
        if size > 0:
            count = ctypes.c_int(size)
            times = (ctypes.c_double * size)()
            values = (ctypes.c_double * size)()
            result = self._lib.WGFMU_getPatternForceValues(pattern_name_encoded, offset, ctypes.byref(count), times,
                                                           values)
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return np.array(times), np.array(values)
        else:
            return np.array([]), np.array([])

    def getPatternForceValue(self, pattern_name: str, index: int) -> tuple[float, float]:
        """Gets a specific time and force value from a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        time_val = ctypes.c_double()
        value_val = ctypes.c_double()
        result = self._lib.WGFMU_getPatternForceValue(pattern_name_encoded, index, ctypes.byref(time_val),
                                                      ctypes.byref(value_val))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return time_val.value, value_val.value

    def getPatternInterpolatedForceValue(self, pattern_name: str, time_s: float) -> float:
        """Gets the interpolated force value at a specific time in a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        value = ctypes.c_double()
        result = self._lib.WGFMU_getPatternInterpolatedForceValue(pattern_name_encoded, time_s, ctypes.byref(value))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return value.value

    def getPatternMeasureTimeSize(self, pattern_name: str) -> int:
        """Gets the size of the measure time array for a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        size = ctypes.c_int()
        result = self._lib.WGFMU_getPatternMeasureTimeSize(pattern_name_encoded, ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getPatternMeasureTimes(self, pattern_name: str, offset: int = 0) -> np.ndarray:
        """Retrieves the measure time vector for a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        size = self.getPatternMeasureTimeSize(pattern_name)
        if size > 0:
            count = ctypes.c_int(size)
            times = (ctypes.c_double * size)()
            result = self._lib.WGFMU_getPatternMeasureTimes(pattern_name_encoded, offset, ctypes.byref(count), times)
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return np.array(times)
        else:
            return np.array([])

    def getPatternMeasureTime(self, pattern_name: str, index: int) -> float:
        """Gets a specific measure time from a pattern."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        time_val = ctypes.c_double()
        result = self._lib.WGFMU_getPatternMeasureTime(pattern_name_encoded, index, ctypes.byref(time_val))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return time_val.value

    # WGFMU - Setup Check - Sequence

    def getForceValueSize(self, channel_id: int) -> float:
        """Gets the size of the force value data for a channel."""
        size = ctypes.c_double()
        result = self._lib.WGFMU_getForceValueSize(channel_id, ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getForceValues(self, channel_id: int, offset: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        """Retrieves vectors of force times and values for a channel."""
        size_val = self.getForceValueSize(channel_id)
        if size_val > 0:
            size_int = int(size_val)
            size_c = ctypes.c_int(size_int)
            force_times_c = (ctypes.c_double * size_int)()
            force_values_c = (ctypes.c_double * size_int)()
            result = self._lib.WGFMU_getForceValues(
                channel_id,
                offset,
                ctypes.byref(size_c),
                force_times_c,
                force_values_c
            )
            if result == self.NO_ERROR:
                force_times = np.array(force_times_c)
                force_values = np.array(force_values_c)
                return force_times, force_values
            else:
                raise self._handle_error(result)
        else:
            return np.array([]), np.array([])

    def getForceValue(self, channel_id: int, index: float) -> tuple[float, float]:
        """Gets a specific force time and value for a channel at a given index."""
        force_time = ctypes.c_double()
        force_value = ctypes.c_double()
        result = self._lib.WGFMU_getForceValue(channel_id, index, ctypes.byref(force_time), ctypes.byref(force_value))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return force_time.value, force_value.value

    def getInterpolatedForceValue(self, channel_id: int, time: float) -> float:
        """Gets the interpolated force value for a channel at a given time."""
        force_value = ctypes.c_double()
        result = self._lib.WGFMU_getInterpolatedForceValue(channel_id, time, ctypes.byref(force_value))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return force_value.value

    def getMeasureTimeSize(self, channel_id: int) -> int:
        """Gets the size of the measurement time vector for a channel."""
        size = ctypes.c_int()
        result = self._lib.WGFMU_getMeasureTimeSize(channel_id, ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getMeasureTimes(self, channel_id: int, offset: int = 0) -> np.ndarray:
        """Retrieves the measurement time vector for a channel."""
        size = self.getMeasureTimeSize(channel_id)
        if size > 0:
            size_c = ctypes.c_int(size)
            measure_times_c = (ctypes.c_double * size)()
            result = self._lib.WGFMU_getMeasureTimes(channel_id, offset, ctypes.byref(size_c), measure_times_c)
            if result != self.NO_ERROR:
                raise self._handle_error(result)
            return np.array(measure_times_c)
        else:
            return np.array([])

    def getMeasureTime(self, channel_id: int, index: int) -> float:
        """Gets a specific measurement time for a channel at a given index."""
        measure_time = ctypes.c_double()
        result = self._lib.WGFMU_getMeasureTime(channel_id, index, ctypes.byref(measure_time))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measure_time.value

    # WGFMU - Setup Check - Event

    def getMeasureEventSize(self, channelId: int) -> int:
        """Gets the number of measure events defined in a pattern."""
        size = ctypes.c_int()
        result = self._lib.WGFMU_getMeasureEventSize(channelId, ctypes.byref(size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return size.value

    def getMeasureEvents(self, channel_id: int, measId: int = 0) -> list[dict]:
        """Retrieves details of multiple measure events for a channel."""
        num_events = self.getMeasureEventSize(channel_id)  # Assuming this function exists
        if num_events == 0:
            return []

        pattern_name_buffer_size = 512  # Choose a reasonable max string length
        event_name_buffer_size = 512

        pattern_name_buffers = (ctypes.c_char * pattern_name_buffer_size * num_events)()
        event_name_buffers = (ctypes.c_char * event_name_buffer_size * num_events)()

        pattern_names_ptr = (ctypes.POINTER(ctypes.c_char) * num_events)()
        event_names_ptr = (ctypes.POINTER(ctypes.c_char) * num_events)()
        cycles = (ctypes.c_int * num_events)()
        loops = (ctypes.c_double * num_events)()
        counts = (ctypes.c_int * num_events)()
        offsets = (ctypes.c_int * num_events)()
        sizes = (ctypes.c_int * num_events)()
        size_out = ctypes.c_int(num_events)

        # Set the pointers to point to the allocated buffers
        for i in range(num_events):
            pattern_names_ptr[i] = ctypes.cast(
                ctypes.addressof(pattern_name_buffers[i * pattern_name_buffer_size]),
                ctypes.POINTER(ctypes.c_char)
            )
            event_names_ptr[i] = ctypes.cast(
                ctypes.addressof(event_name_buffers[i * event_name_buffer_size]),
                ctypes.POINTER(ctypes.c_char)
            )

        result = self._lib.WGFMU_getMeasureEvents(
            channel_id,
            measId,
            ctypes.byref(size_out),
            ctypes.cast(pattern_names_ptr, ctypes.POINTER(ctypes.c_char_p)),
            ctypes.cast(event_names_ptr, ctypes.POINTER(ctypes.c_char_p)),
            cycles,
            loops,
            counts,
            offsets,
            sizes
        )

        if result != self.NO_ERROR:
            raise self._handle_error(result)

        events = []
        for i in range(size_out.value):
            pattern_name = ctypes.string_at(pattern_names_ptr[i]).decode('utf-8')
            event_name = ctypes.string_at(event_names_ptr[i]).decode('utf-8')
            events.append({
                "patternName": pattern_name,
                "eventName": event_name,
                "cycle": cycles[i],
                "loop": loops[i],
                "count": counts[i],
                "offset": offsets[i],
                "size": sizes[i],
            })

        return events

    def getMeasureEvent(self, channel_id: int, index: int) -> dict:
        """Retrieves the details of a single measure event for a channel at a given index."""
        pattern_name_buffer = ctypes.create_string_buffer(256)  # Assuming a max length for patternName
        event_name_buffer = ctypes.create_string_buffer(256)  # Assuming a max length for eventName
        cycle = ctypes.c_int()
        loop = ctypes.c_double()
        count = ctypes.c_int()
        offset = ctypes.c_int()
        size = ctypes.c_int()

        result = self._lib.WGFMU_getMeasureEvent(
            channel_id,
            index,
            pattern_name_buffer,
            event_name_buffer,
            ctypes.byref(cycle),
            ctypes.byref(loop),
            ctypes.byref(count),
            ctypes.byref(offset),
            ctypes.byref(size)
        )

        if result != self.NO_ERROR:
            raise self._handle_error(result)

        return {
            "patternName": pattern_name_buffer.value.decode('utf-8'),
            "eventName": event_name_buffer.value.decode('utf-8'),
            "cycle": cycle.value,
            "loop": loop.value,
            "count": count.value,
            "offset": offset.value,
            "size": size.value,
        }

    def getMeasureEventAttribute(self, channel_id: int, index: int) -> dict:
        """Retrieves specific attributes of a single measure event for a channel at a given index."""
        time = ctypes.c_double()
        measurement_points = ctypes.c_int()
        measurement_interval = ctypes.c_double()
        averaging_time = ctypes.c_double()
        raw_data = ctypes.c_int()

        result = self._lib.WGFMU_getMeasureEventAttribute(
            channel_id,
            index,
            ctypes.byref(time),
            ctypes.byref(measurement_points),
            ctypes.byref(measurement_interval),
            ctypes.byref(averaging_time),
            ctypes.byref(raw_data)
        )

        if result != self.NO_ERROR:
            raise self._handle_error(result)

        return {
            "time": time.value,
            "measurementPoints": measurement_points.value,
            "measurementInterval": measurement_interval.value,
            "averagingTime": averaging_time.value,
            "rawData": raw_data.value,  # Returning the integer value of rawData
        }

    # WGFMU - Import / Export

    def exportAscii(self, file_name: str) -> None:
        """Exports WGFMU data to an ASCII file."""
        file_name_encoded = file_name.encode('utf-8')
        result = self._lib.WGFMU_exportAscii(file_name_encoded)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Measurement

    def update(self) -> None:
        """Updates the WGFMU device with the latest settings."""
        result = self._lib.WGFMU_update()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def update_channel(self, channel_id: int) -> None:
        """Updates a specific channel of the WGFMU device with the latest settings."""
        result = self._lib.WGFMU_updateChannel(channel_id)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def execute(self) -> None:
        """Starts the execution of the configured waveform generation and measurement."""
        result = self._lib.WGFMU_execute()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def abort(self) -> None:
        """Immediately stops the ongoing waveform generation and measurement."""
        result = self._lib.WGFMU_abort()
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def abortChannel(self, channel_id: int) -> None:
        """Immediately stops the ongoing waveform generation and measurement for a specific channel."""
        result = self._lib.WGFMU_abortChannel(channel_id)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def getStatus(self) -> tuple[int, float, float]:
        """Gets the current status, elapsed time, and total time of the WGFMU execution."""
        status = ctypes.c_int()
        elapsed_time = ctypes.c_double()
        total_time = ctypes.c_double()

        result = self._lib.WGFMU_getStatus(
            ctypes.byref(status),
            ctypes.byref(elapsed_time),
            ctypes.byref(total_time)
        )

        if result != self.NO_ERROR:
            raise self._handle_error(result)

        return status.value, elapsed_time.value, total_time.value

    def getChannelStatus(self, channel_id: int) -> tuple[int, float, float]:
        """Gets the current status, elapsed time, and total time for a specific channel of the WGFMU."""
        status = ctypes.c_int()
        elapsed_time = ctypes.c_double()
        total_time = ctypes.c_double()

        result = self._lib.WGFMU_getChannelStatus(
            channel_id,
            ctypes.byref(status),
            ctypes.byref(elapsed_time),
            ctypes.byref(total_time)
        )

        if result != self.NO_ERROR:
            raise self._handle_error(result)

        return status.value, elapsed_time.value, total_time.value

    def waitUntilCompleted(self, timeout_ms: int = -1) -> None:
        """Waits until the WGFMU operation is completed or a timeout occurs.

        Args:
            timeout_ms: The maximum time to wait in milliseconds.
                        Use -1 to wait indefinitely.
        Raises:
            Exception: If a timeout occurs (if timeout_ms is not -1) or if an error occurs.
        """
        result = self._lib.WGFMU_waitUntilCompleted(timeout_ms)
        if result == self.ERROR_CODE_MIN:  # Assuming a specific error code for timeout
            raise Exception(f"Timeout occurred while waiting for WGFMU completion ({timeout_ms} ms).")
        elif result != self.NO_ERROR:
            raise self._handle_error(result)

    # WGFMU - Data Retrieve - Measure Value

    def getMeasureValueSize(self, channel_id: int) -> tuple[int, int]:
        """Gets the measured and total size of the measurement values for a channel."""
        measured_size = ctypes.c_int()
        total_size = ctypes.c_int()
        result = self._lib.WGFMU_getMeasureValueSize(channel_id, ctypes.byref(measured_size), ctypes.byref(total_size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measured_size.value, total_size.value

    def getMeasureValues(self, channel_id: int, offset: int = 0) -> tuple[np.ndarray, np.ndarray]:
        """Retrieves vectors of measurement times and values for a channel."""
        measured_size, _ = self.getMeasureValueSize(channel_id)
        if measured_size > 0:
            size_c = ctypes.c_int(measured_size)
            measure_times_c = (ctypes.c_double * measured_size)()
            measure_values_c = (ctypes.c_double * measured_size)()

            result = self._lib.WGFMU_getMeasureValues(
                channel_id,
                offset,
                ctypes.byref(size_c),
                measure_times_c,
                measure_values_c
            )
            if result == self.NO_ERROR:
                measure_times = np.array(measure_times_c)
                measure_values = np.array(measure_values_c)
                return measure_times, measure_values
            else:
                raise self._handle_error(result)
        else:
            return np.array([]), np.array([])

    def getMeasureValue(self, channel_id: int, index: int) -> tuple[float, float]:
        """Gets a specific measurement time and value for a channel at a given index."""
        measure_time = ctypes.c_double()
        measure_value = ctypes.c_double()
        result = self._lib.WGFMU_getMeasureValue(channel_id, index, ctypes.byref(measure_time),
                                                 ctypes.byref(measure_value))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measure_time.value, measure_value.value

    # WGFMU - Data Retrieve - Measure Event

    def getCompletedMeasureEventSize(self, channel_id: int) -> tuple[int, int]:
        """Gets the measured and total size of the completed measure events for a channel."""
        measured_size = ctypes.c_int()
        total_size = ctypes.c_int()
        result = self._lib.WGFMU_getCompletedMeasureEventSize(channel_id, ctypes.byref(measured_size),
                                                              ctypes.byref(total_size))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return measured_size.value, total_size.value

    def isMeasureEventCompleted(
            self,
            channel_id: int,
            pattern_name: str,
            event_name: str,
            cycle: int,
            loop: float,
            count: int,
    ) -> tuple[bool, int, int, int, int]:
        """Checks if a specific measure event is completed and returns its information."""
        pattern_name_encoded = pattern_name.encode('utf-8')
        event_name_encoded = event_name.encode('utf-8')
        completed = ctypes.c_int()
        index = ctypes.c_int()
        offset = ctypes.c_int()
        size = ctypes.c_int()

        result = self._lib.WGFMU_isMeasureEventCompleted(
            channel_id,
            pattern_name_encoded,
            event_name_encoded,
            cycle,
            loop,
            count,
            ctypes.byref(completed),
            ctypes.byref(index),
            ctypes.byref(offset),
            ctypes.byref(size),
        )
        if result != self.NO_ERROR:
            raise self._handle_error(result)

        return bool(completed.value), index.value, offset.value, size.value, result

    # DC - Measure

    def dcForceVoltage(self, channel_id: int, voltage: float) -> None:
        """Forces a DC voltage on the specified channel."""
        result = self._lib.WGFMU_dcforceVoltage(channel_id, voltage)
        if result != self.NO_ERROR:
            raise self._handle_error(result)

    def dcMeasureValue(self, channel_id: int) -> float:
        """Measures the current DC value on the specified channel."""
        value = ctypes.c_double()
        result = self._lib.WGFMU_dcmeasureValue(channel_id, ctypes.byref(value))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return value.value

    def dcMeasureAveragedValue(self, channel_id: int, count: int, interval: int) -> float:
        """Measures the averaged DC value on the specified channel over a number of readings."""
        value = ctypes.c_double()
        result = self._lib.WGFMU_dcmeasureAveragedValue(channel_id, count, interval, ctypes.byref(value))
        if result != self.NO_ERROR:
            raise self._handle_error(result)
        return value.value

    # _handle_error

    def _handle_error(self, error_code: int):
        """Internal method to handle WGFMU errors."""
        error_buffer = ctypes.create_string_buffer(256)  # Adjust size as needed
        result = self._lib.WGFMU_getError(error_buffer, ctypes.byref(ctypes.c_int(ctypes.sizeof(error_buffer))))
        if result == self.NO_ERROR:
            error_message = error_buffer.value.decode('utf-8')
            return Exception(f"WGFMU Error {error_code}: {error_message}")
        else:
            return Exception(f"WGFMU Error {error_code}: Could not retrieve detailed error message.")

    def _define_argtypes_restypes(self):
        # Common - Initialize
        self._lib.WGFMU_openSession.argtypes = [ctypes.c_char_p]
        self._lib.WGFMU_openSession.restype = ctypes.c_int

        self._lib.WGFMU_closeSession.argtypes = []
        self._lib.WGFMU_closeSession.restype = ctypes.c_int

        self._lib.WGFMU_initialize.argtypes = []
        self._lib.WGFMU_initialize.restype = ctypes.c_int

        self._lib.WGFMU_setTimeout.argtypes = [ctypes.c_double]
        self._lib.WGFMU_setTimeout.restype = ctypes.c_int

        self._lib.WGFMU_doSelfCalibration.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_char_p,
                                                      ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_doSelfCalibration.restype = ctypes.c_int

        self._lib.WGFMU_doSelfTest.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_char_p,
                                               ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_doSelfTest.restype = ctypes.c_int

        self._lib.WGFMU_getChannelIdSize.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getChannelIdSize.restype = ctypes.c_int

        self._lib.WGFMU_getChannelIds.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getChannelIds.restype = ctypes.c_int

        # Common - Error and Warning
        self._lib.WGFMU_getErrorSize.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getErrorSize.restype = ctypes.c_int

        self._lib.WGFMU_getError.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getError.restype = ctypes.c_int

        self._lib.WGFMU_getErrorSummarySize.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getErrorSummarySize.restype = ctypes.c_int

        self._lib.WGFMU_getErrorSummary.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getErrorSummary.restype = ctypes.c_int

        self._lib.WGFMU_treatWarningsAsErrors.argtypes = [ctypes.c_int]
        self._lib.WGFMU_treatWarningsAsErrors.restype = ctypes.c_int

        self._lib.WGFMU_setWarningLevel.argtypes = [ctypes.c_int]
        self._lib.WGFMU_setWarningLevel.restype = ctypes.c_int

        self._lib.WGFMU_getWarningLevel.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getWarningLevel.restype = ctypes.c_int

        self._lib.WGFMU_getWarningSummarySize.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getWarningSummarySize.restype = ctypes.c_int

        self._lib.WGFMU_getWarningSummary.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getWarningSummary.restype = ctypes.c_int

        self._lib.WGFMU_openLogFile.argtypes = [ctypes.c_char_p]
        self._lib.WGFMU_openLogFile.restype = ctypes.c_int

        self._lib.WGFMU_closeLogFile.argtypes = []
        self._lib.WGFMU_closeLogFile.restype = ctypes.c_int

        # Common - Setup
        self._lib.WGFMU_setOperationMode.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setOperationMode.restype = ctypes.c_int

        self._lib.WGFMU_getOperationMode.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getOperationMode.restype = ctypes.c_int

        self._lib.WGFMU_setForceVoltageRange.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setForceVoltageRange.restype = ctypes.c_int

        self._lib.WGFMU_getForceVoltageRange.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getForceVoltageRange.restype = ctypes.c_int

        self._lib.WGFMU_setMeasureMode.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setMeasureMode.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureMode.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureMode.restype = ctypes.c_int

        self._lib.WGFMU_setMeasureVoltageRange.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setMeasureVoltageRange.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureVoltageRange.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureVoltageRange.restype = ctypes.c_int

        self._lib.WGFMU_setMeasureCurrentRange.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setMeasureCurrentRange.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureCurrentRange.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureCurrentRange.restype = ctypes.c_int

        self._lib.WGFMU_setForceDelay.argtypes = [ctypes.c_int, ctypes.c_double]
        self._lib.WGFMU_setForceDelay.restype = ctypes.c_int

        self._lib.WGFMU_getForceDelay.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getForceDelay.restype = ctypes.c_int

        self._lib.WGFMU_setMeasureDelay.argtypes = [ctypes.c_int, ctypes.c_double]
        self._lib.WGFMU_setMeasureDelay.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureDelay.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getMeasureDelay.restype = ctypes.c_int

        self._lib.WGFMU_setMeasureEnabled.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setMeasureEnabled.restype = ctypes.c_int

        self._lib.WGFMU_isMeasureEnabled.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_isMeasureEnabled.restype = ctypes.c_int

        self._lib.WGFMU_setTriggerOutMode.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self._lib.WGFMU_setTriggerOutMode.restype = ctypes.c_int

        self._lib.WGFMU_getTriggerOutMode.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                      ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getTriggerOutMode.restype = ctypes.c_int

        # Common - Measurement
        self._lib.WGFMU_connect.argtypes = [ctypes.c_int]
        self._lib.WGFMU_connect.restype = ctypes.c_int

        self._lib.WGFMU_disconnect.argtypes = [ctypes.c_int]
        self._lib.WGFMU_disconnect.restype = ctypes.c_int

        # WGFMU - Initialize
        self._lib.WGFMU_clear.argtypes = []
        self._lib.WGFMU_clear.restype = ctypes.c_int

        # WGFMU - Setup - Pattern
        self._lib.WGFMU_createPattern.argtypes = [ctypes.c_char_p, ctypes.c_double]
        self._lib.WGFMU_createPattern.restype = ctypes.c_int

        self._lib.WGFMU_addVector.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
        self._lib.WGFMU_addVector.restype = ctypes.c_int

        self._lib.WGFMU_addVectors.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double),
                                               ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        self._lib.WGFMU_addVectors.restype = ctypes.c_int

        self._lib.WGFMU_setVector.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
        self._lib.WGFMU_setVector.restype = ctypes.c_int

        self._lib.WGFMU_setVectors.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double),
                                               ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        self._lib.WGFMU_setVectors.restype = ctypes.c_int

        # WGFMU - Setup - Pattern Operation
        self._lib.WGFMU_createMergedPattern.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self._lib.WGFMU_createMergedPattern.restype = ctypes.c_int

        self._lib.WGFMU_createMultipliedPattern.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,
                                                            ctypes.c_double]
        self._lib.WGFMU_createMultipliedPattern.restype = ctypes.c_int

        self._lib.WGFMU_createOffsetPattern.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,
                                                        ctypes.c_double]
        self._lib.WGFMU_createOffsetPattern.restype = ctypes.c_int

        # WGFMU - Setup - Event
        self._lib.WGFMU_setMeasureEvent.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_int,
                                                    ctypes.c_double, ctypes.c_double, ctypes.c_int]
        self._lib.WGFMU_setMeasureEvent.restype = ctypes.c_int

        self._lib.WGFMU_setRangeEvent.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_int]
        self._lib.WGFMU_setRangeEvent.restype = ctypes.c_int

        self._lib.WGFMU_setTriggerOutEvent.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,
                                                       ctypes.c_double]
        self._lib.WGFMU_setTriggerOutEvent.restype = ctypes.c_int

        # WGFMU - Setup - Sequence
        self._lib.WGFMU_addSequence.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_double]
        self._lib.WGFMU_addSequence.restype = ctypes.c_int

        self._lib.WGFMU_addSequences.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p),
                                                 ctypes.POINTER(ctypes.c_double), ctypes.c_int]
        self._lib.WGFMU_addSequences.restype = ctypes.c_int

        # WGFMU - Setup Check - Pattern
        self._lib.WGFMU_getPatternForceValueSize.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getPatternForceValueSize.restype = ctypes.c_int

        self._lib.WGFMU_getPatternForceValues.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                          ctypes.POINTER(ctypes.c_double),
                                                          ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getPatternForceValues.restype = ctypes.c_int

        self._lib.WGFMU_getPatternForceValue.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                                         ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getPatternForceValue.restype = ctypes.c_int

        self._lib.WGFMU_getPatternInterpolatedForceValue.argtypes = [ctypes.c_char_p, ctypes.c_double,
                                                                     ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getPatternInterpolatedForceValue.restype = ctypes.c_int

        self._lib.WGFMU_getPatternMeasureTimeSize.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getPatternMeasureTimeSize.restype = ctypes.c_int

        self._lib.WGFMU_getPatternMeasureTimes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                           ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getPatternMeasureTimes.restype = ctypes.c_int

        self._lib.WGFMU_getPatternMeasureTime.argtypes = [ctypes.c_char_p, ctypes.c_int,
                                                          ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getPatternMeasureTime.restype = ctypes.c_int

        # WGFMU - Setup Check - Sequence
        self._lib.WGFMU_getForceValueSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getForceValueSize.restype = ctypes.c_int

        self._lib.WGFMU_getForceValues.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_int),
                                                   ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getForceValues.restype = ctypes.c_int

        self._lib.WGFMU_getForceValue.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double),
                                                  ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getForceValue.restype = ctypes.c_int

        self._lib.WGFMU_getInterpolatedForceValue.argtypes = [ctypes.c_int, ctypes.c_double,
                                                              ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getInterpolatedForceValue.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureTimeSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureTimeSize.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureTimes.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                    ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getMeasureTimes.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureTime.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getMeasureTime.restype = ctypes.c_int

        # WGFMU - Setup Check - Event
        self._lib.WGFMU_getMeasureEventSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureEventSize.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureEvents.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                     ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p),
                                                     ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double),
                                                     ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                                     ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureEvents.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureEvent.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
                                                    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double),
                                                    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                                    ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureEvent.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureEventAttribute.argtypes = [ctypes.c_int, ctypes.c_int,
                                                             ctypes.POINTER(ctypes.c_double),
                                                             ctypes.POINTER(ctypes.c_int),
                                                             ctypes.POINTER(ctypes.c_double),
                                                             ctypes.POINTER(ctypes.c_double),
                                                             ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureEventAttribute.restype = ctypes.c_int

        # WGFMU - Import / Export
        self._lib.WGFMU_exportAscii.argtypes = [ctypes.c_char_p]
        self._lib.WGFMU_exportAscii.restype = ctypes.c_int

        # WGFMU - Measurement
        self._lib.WGFMU_update.argtypes = []
        self._lib.WGFMU_update.restype = ctypes.c_int

        self._lib.WGFMU_updateChannel.argtypes = [ctypes.c_int]
        self._lib.WGFMU_updateChannel.restype = ctypes.c_int

        self._lib.WGFMU_execute.argtypes = []
        self._lib.WGFMU_execute.restype = ctypes.c_int

        self._lib.WGFMU_abort.argtypes = []
        self._lib.WGFMU_abort.restype = ctypes.c_int

        self._lib.WGFMU_abortChannel.argtypes = [ctypes.c_int]
        self._lib.WGFMU_abortChannel.restype = ctypes.c_int

        self._lib.WGFMU_getStatus.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double),
                                              ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getStatus.restype = ctypes.c_int

        self._lib.WGFMU_getChannelStatus.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                     ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getChannelStatus.restype = ctypes.c_int

        self._lib.WGFMU_waitUntilCompleted.argtypes = []
        self._lib.WGFMU_waitUntilCompleted.restype = ctypes.c_int

        # WGFMU - Data Retrieve - Measure Value
        self._lib.WGFMU_getMeasureValueSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                        ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getMeasureValueSize.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                     ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getMeasureValues.restype = ctypes.c_int

        self._lib.WGFMU_getMeasureValue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                                    ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_getMeasureValue.restype = ctypes.c_int

        # WGFMU - Data Retrieve - Measure Event
        self._lib.WGFMU_getCompletedMeasureEventSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                                 ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_getCompletedMeasureEventSize.restype = ctypes.c_int

        self._lib.WGFMU_isMeasureEventCompleted.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
                                                            ctypes.c_int,
                                                            ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                                            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                                            ctypes.POINTER(ctypes.c_int)]
        self._lib.WGFMU_isMeasureEventCompleted.restype = ctypes.c_int

        # DC - Measure
        self._lib.WGFMU_dcforceVoltage.argtypes = [ctypes.c_int, ctypes.c_double]
        self._lib.WGFMU_dcforceVoltage.restype = ctypes.c_int

        self._lib.WGFMU_dcmeasureValue.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_dcmeasureValue.restype = ctypes.c_int

        self._lib.WGFMU_dcmeasureAveragedValue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                                           ctypes.POINTER(ctypes.c_double)]
        self._lib.WGFMU_dcmeasureAveragedValue.restype = ctypes.c_int

    @property
    def NO_ERROR(self):
        return WGFMU_NO_ERROR

    @property
    def PARAMETER_OUT_OF_RANGE_ERROR(self):
        return WGFMU_PARAMETER_OUT_OF_RANGE_ERROR

    @property
    def ILLEGAL_STRING_ERROR(self):
        return WGFMU_ILLEGAL_STRING_ERROR

    @property
    def CONTEXT_ERROR(self):
        return WGFMU_CONTEXT_ERROR

    @property
    def FUNCTION_NOT_SUPPORTED_ERROR(self):
        return WGFMU_FUNCTION_NOT_SUPPORTED_ERROR

    @property
    def COMMUNICATION_ERROR(self):
        return WGFMU_COMMUNICATION_ERROR

    @property
    def FW_ERROR(self):
        return WGFMU_FW_ERROR

    @property
    def LIBRARY_ERROR(self):
        return WGFMU_LIBRARY_ERROR

    @property
    def ERROR(self):
        return WGFMU_ERROR

    @property
    def CHANNEL_NOT_FOUND_ERROR(self):
        return WGFMU_CHANNEL_NOT_FOUND_ERROR

    @property
    def PATTERN_NOT_FOUND_ERROR(self):
        return WGFMU_PATTERN_NOT_FOUND_ERROR

    @property
    def EVENT_NOT_FOUND_ERROR(self):
        return WGFMU_EVENT_NOT_FOUND_ERROR

    @property
    def PATTERN_ALREADY_EXISTS_ERROR(self):
        return WGFMU_PATTERN_ALREADY_EXISTS_ERROR

    @property
    def SEQUENCER_NOT_RUNNING_ERROR(self):
        return WGFMU_SEQUENCER_NOT_RUNNING_ERROR

    @property
    def RESULT_NOT_READY_ERROR(self):
        return WGFMU_RESULT_NOT_READY_ERROR

    @property
    def RESULT_OUT_OF_DATE(self):
        return WGFMU_RESULT_OUT_OF_DATE

    @property
    def ERROR_CODE_MIN(self):
        return WGFMU_ERROR_CODE_MIN

    @property
    def PASS(self):
        return WGFMU_PASS

    @property
    def FAIL(self):
        return WGFMU_FAIL

    @property
    def WARNING_LEVEL_OFFSET(self):
        return WGFMU_WARNING_LEVEL_OFFSET

    @property
    def WARNING_LEVEL_OFF(self):
        return WGFMU_WARNING_LEVEL_OFF

    @property
    def WARNING_LEVEL_SEVERE(self):
        return WGFMU_WARNING_LEVEL_SEVERE

    @property
    def WARNING_LEVEL_NORMAL(self):
        return WGFMU_WARNING_LEVEL_NORMAL

    @property
    def WARNING_LEVEL_INFORMATION(self):
        return WGFMU_WARNING_LEVEL_INFORMATION

    @property
    def OPERATION_MODE_OFFSET(self):
        return WGFMU_OPERATION_MODE_OFFSET

    @property
    def OPERATION_MODE_DC(self):
        return WGFMU_OPERATION_MODE_DC

    @property
    def OPERATION_MODE_FASTIV(self):
        return WGFMU_OPERATION_MODE_FASTIV

    @property
    def OPERATION_MODE_PG(self):
        return WGFMU_OPERATION_MODE_PG

    @property
    def OPERATION_MODE_SMU(self):
        return WGFMU_OPERATION_MODE_SMU

    @property
    def FORCE_VOLTAGE_RANGE_OFFSET(self):
        return WGFMU_FORCE_VOLTAGE_RANGE_OFFSET

    @property
    def FORCE_VOLTAGE_RANGE_AUTO(self):
        return WGFMU_FORCE_VOLTAGE_RANGE_AUTO

    @property
    def FORCE_VOLTAGE_RANGE_3V(self):
        return WGFMU_FORCE_VOLTAGE_RANGE_3V

    @property
    def FORCE_VOLTAGE_RANGE_5V(self):
        return WGFMU_FORCE_VOLTAGE_RANGE_5V

    @property
    def FORCE_VOLTAGE_RANGE_10V_NEGATIVE(self):
        return WGFMU_FORCE_VOLTAGE_RANGE_10V_NEGATIVE

    @property
    def FORCE_VOLTAGE_RANGE_10V_POSITIVE(self):
        return WGFMU_FORCE_VOLTAGE_RANGE_10V_POSITIVE

    @property
    def MEASURE_MODE_OFFSET(self):
        return WGFMU_MEASURE_MODE_OFFSET

    @property
    def MEASURE_MODE_VOLTAGE(self):
        return WGFMU_MEASURE_MODE_VOLTAGE

    @property
    def MEASURE_MODE_CURRENT(self):
        return WGFMU_MEASURE_MODE_CURRENT

    @property
    def MEASURE_VOLTAGE_RANGE_OFFSET(self):
        return WGFMU_MEASURE_VOLTAGE_RANGE_OFFSET

    @property
    def MEASURE_VOLTAGE_RANGE_5V(self):
        return WGFMU_MEASURE_VOLTAGE_RANGE_5V

    @property
    def MEASURE_VOLTAGE_RANGE_10V(self):
        return WGFMU_MEASURE_VOLTAGE_RANGE_10V

    @property
    def MEASURE_CURRENT_RANGE_OFFSET(self):
        return WGFMU_MEASURE_CURRENT_RANGE_OFFSET

    @property
    def MEASURE_CURRENT_RANGE_1UA(self):
        return WGFMU_MEASURE_CURRENT_RANGE_1UA

    @property
    def MEASURE_CURRENT_RANGE_10UA(self):
        return WGFMU_MEASURE_CURRENT_RANGE_10UA

    @property
    def MEASURE_CURRENT_RANGE_100UA(self):
        return WGFMU_MEASURE_CURRENT_RANGE_100UA

    @property
    def MEASURE_CURRENT_RANGE_1MA(self):
        return WGFMU_MEASURE_CURRENT_RANGE_1MA

    @property
    def MEASURE_CURRENT_RANGE_10MA(self):
        return WGFMU_MEASURE_CURRENT_RANGE_10MA

    @property
    def MEASURE_ENABLED_OFFSET(self):
        return WGFMU_MEASURE_ENABLED_OFFSET

    @property
    def MEASURE_ENABLED_DISABLE(self):
        return WGFMU_MEASURE_ENABLED_DISABLE

    @property
    def MEASURE_ENABLED_ENABLE(self):
        return WGFMU_MEASURE_ENABLED_ENABLE

    @property
    def TRIGGER_OUT_MODE_OFFSET(self):
        return WGFMU_TRIGGER_OUT_MODE_OFFSET

    @property
    def TRIGGER_OUT_MODE_DISABLE(self):
        return WGFMU_TRIGGER_OUT_MODE_DISABLE

    @property
    def TRIGGER_OUT_MODE_START_EXECUTION(self):
        return WGFMU_TRIGGER_OUT_MODE_START_EXECUTION

    @property
    def TRIGGER_OUT_MODE_START_SEQUENCE(self):
        return WGFMU_TRIGGER_OUT_MODE_START_SEQUENCE

    @property
    def TRIGGER_OUT_MODE_START_PATTERN(self):
        return WGFMU_TRIGGER_OUT_MODE_START_PATTERN

    @property
    def TRIGGER_OUT_MODE_EVENT(self):
        return WGFMU_TRIGGER_OUT_MODE_EVENT

    @property
    def TRIGGER_OUT_POLARITY_OFFSET(self):
        return WGFMU_TRIGGER_OUT_POLARITY_OFFSET

    @property
    def TRIGGER_OUT_POLARITY_POSITIVE(self):
        return WGFMU_TRIGGER_OUT_POLARITY_POSITIVE

    @property
    def TRIGGER_OUT_POLARITY_NEGATIVE(self):
        return WGFMU_TRIGGER_OUT_POLARITY_NEGATIVE

    @property
    def AXIS_OFFSET(self):
        return WGFMU_AXIS_OFFSET

    @property
    def AXIS_TIME(self):
        return WGFMU_AXIS_TIME

    @property
    def AXIS_VOLTAGE(self):
        return WGFMU_AXIS_VOLTAGE

    @property
    def STATUS_OFFSET(self):
        return WGFMU_STATUS_OFFSET

    @property
    def STATUS_COMPLETED(self):
        return WGFMU_STATUS_COMPLETED

    @property
    def STATUS_DONE(self):
        return WGFMU_STATUS_DONE

    @property
    def STATUS_RUNNING(self):
        return WGFMU_STATUS_RUNNING

    @property
    def STATUS_ABORT_COMPLETED(self):
        return WGFMU_STATUS_ABORT_COMPLETED

    @property
    def STATUS_ABORTED(self):
        return WGFMU_STATUS_ABORTED

    @property
    def STATUS_RUNNING_ILLEGAL(self):
        return WGFMU_STATUS_RUNNING_ILLEGAL

    @property
    def STATUS_IDLE(self):
        return WGFMU_STATUS_IDLE

    @property
    def MEASURE_EVENT_OFFSET(self):
        return WGFMU_MEASURE_EVENT_OFFSET

    @property
    def MEASURE_EVENT_NOT_COMPLETED(self):
        return WGFMU_MEASURE_EVENT_NOT_COMPLETED

    @property
    def MEASURE_EVENT_COMPLETED(self):
        return WGFMU_MEASURE_EVENT_COMPLETED

    @property
    def MEASURE_EVENT_DATA_OFFSET(self):
        return WGFMU_MEASURE_EVENT_DATA_OFFSET

    @property
    def MEASURE_EVENT_DATA_AVERAGED(self):
        return WGFMU_MEASURE_EVENT_DATA_AVERAGED

    @property
    def MEASURE_EVENT_DATA_RAW(self):
        return WGFMU_MEASURE_EVENT_DATA_RAW


# API Return Value - Error Code
WGFMU_NO_ERROR                           = 0
WGFMU_PARAMETER_OUT_OF_RANGE_ERROR      = -1
WGFMU_ILLEGAL_STRING_ERROR              = -2
WGFMU_CONTEXT_ERROR                     = -3
WGFMU_FUNCTION_NOT_SUPPORTED_ERROR      = -4
WGFMU_COMMUNICATION_ERROR               = -5
WGFMU_FW_ERROR                          = -6
WGFMU_LIBRARY_ERROR                     = -7
WGFMU_ERROR                             = -8
WGFMU_CHANNEL_NOT_FOUND_ERROR           = -9
WGFMU_PATTERN_NOT_FOUND_ERROR           = -10
WGFMU_EVENT_NOT_FOUND_ERROR             = -11
WGFMU_PATTERN_ALREADY_EXISTS_ERROR      = -12
WGFMU_SEQUENCER_NOT_RUNNING_ERROR       = -13
WGFMU_RESULT_NOT_READY_ERROR            = -14
WGFMU_RESULT_OUT_OF_DATE                = -15

WGFMU_ERROR_CODE_MIN                    = -9999

# WGFMU_doSelfCalibration, WGFMU_doSelfTest
WGFMU_PASS = 0
WGFMU_FAIL = 1

# WGFMU_treatWarningsAsErrors, WGFMU_setWarningLevel
WGFMU_WARNING_LEVEL_OFFSET              = 1000
WGFMU_WARNING_LEVEL_OFF                = WGFMU_WARNING_LEVEL_OFFSET + 0
WGFMU_WARNING_LEVEL_SEVERE             = WGFMU_WARNING_LEVEL_OFFSET + 1
WGFMU_WARNING_LEVEL_NORMAL             = WGFMU_WARNING_LEVEL_OFFSET + 2
WGFMU_WARNING_LEVEL_INFORMATION        = WGFMU_WARNING_LEVEL_OFFSET + 3

# WGFMU_setOperationMode
WGFMU_OPERATION_MODE_OFFSET             = 2000
WGFMU_OPERATION_MODE_DC                = WGFMU_OPERATION_MODE_OFFSET + 0
WGFMU_OPERATION_MODE_FASTIV            = WGFMU_OPERATION_MODE_OFFSET + 1
WGFMU_OPERATION_MODE_PG                = WGFMU_OPERATION_MODE_OFFSET + 2
WGFMU_OPERATION_MODE_SMU               = WGFMU_OPERATION_MODE_OFFSET + 3

# WGFMU_setForceVoltageRange
WGFMU_FORCE_VOLTAGE_RANGE_OFFSET        = 3000
WGFMU_FORCE_VOLTAGE_RANGE_AUTO         = WGFMU_FORCE_VOLTAGE_RANGE_OFFSET + 0
WGFMU_FORCE_VOLTAGE_RANGE_3V           = WGFMU_FORCE_VOLTAGE_RANGE_OFFSET + 1
WGFMU_FORCE_VOLTAGE_RANGE_5V           = WGFMU_FORCE_VOLTAGE_RANGE_OFFSET + 2
WGFMU_FORCE_VOLTAGE_RANGE_10V_NEGATIVE = WGFMU_FORCE_VOLTAGE_RANGE_OFFSET + 3
WGFMU_FORCE_VOLTAGE_RANGE_10V_POSITIVE = WGFMU_FORCE_VOLTAGE_RANGE_OFFSET + 4

# WGFMU_setMeasureMode
WGFMU_MEASURE_MODE_OFFSET               = 4000
WGFMU_MEASURE_MODE_VOLTAGE             = WGFMU_MEASURE_MODE_OFFSET + 0
WGFMU_MEASURE_MODE_CURRENT             = WGFMU_MEASURE_MODE_OFFSET + 1

# WGFMU_setMeasureVoltageRange
WGFMU_MEASURE_VOLTAGE_RANGE_OFFSET      = 5000
WGFMU_MEASURE_VOLTAGE_RANGE_5V         = WGFMU_MEASURE_VOLTAGE_RANGE_OFFSET + 1
WGFMU_MEASURE_VOLTAGE_RANGE_10V        = WGFMU_MEASURE_VOLTAGE_RANGE_OFFSET + 2

# WGFMU_setMeasureCurrentRange
WGFMU_MEASURE_CURRENT_RANGE_OFFSET      = 6000
WGFMU_MEASURE_CURRENT_RANGE_1UA        = WGFMU_MEASURE_CURRENT_RANGE_OFFSET + 1
WGFMU_MEASURE_CURRENT_RANGE_10UA       = WGFMU_MEASURE_CURRENT_RANGE_OFFSET + 2
WGFMU_MEASURE_CURRENT_RANGE_100UA      = WGFMU_MEASURE_CURRENT_RANGE_OFFSET + 3
WGFMU_MEASURE_CURRENT_RANGE_1MA        = WGFMU_MEASURE_CURRENT_RANGE_OFFSET + 4
WGFMU_MEASURE_CURRENT_RANGE_10MA       = WGFMU_MEASURE_CURRENT_RANGE_OFFSET + 5

# WGFMU_setMeasureEnabled
WGFMU_MEASURE_ENABLED_OFFSET            = 7000
WGFMU_MEASURE_ENABLED_DISABLE          = WGFMU_MEASURE_ENABLED_OFFSET + 0
WGFMU_MEASURE_ENABLED_ENABLE           = WGFMU_MEASURE_ENABLED_OFFSET + 1

# WGFMU_setTriggerOutMode
WGFMU_TRIGGER_OUT_MODE_OFFSET           = 8000
WGFMU_TRIGGER_OUT_MODE_DISABLE         = WGFMU_TRIGGER_OUT_MODE_OFFSET + 0
WGFMU_TRIGGER_OUT_MODE_START_EXECUTION = WGFMU_TRIGGER_OUT_MODE_OFFSET + 1
WGFMU_TRIGGER_OUT_MODE_START_SEQUENCE  = WGFMU_TRIGGER_OUT_MODE_OFFSET + 2
WGFMU_TRIGGER_OUT_MODE_START_PATTERN   = WGFMU_TRIGGER_OUT_MODE_OFFSET + 3
WGFMU_TRIGGER_OUT_MODE_EVENT           = WGFMU_TRIGGER_OUT_MODE_OFFSET + 4

WGFMU_TRIGGER_OUT_POLARITY_OFFSET       = 8100
WGFMU_TRIGGER_OUT_POLARITY_POSITIVE    = WGFMU_TRIGGER_OUT_POLARITY_OFFSET + 0
WGFMU_TRIGGER_OUT_POLARITY_NEGATIVE    = WGFMU_TRIGGER_OUT_POLARITY_OFFSET + 1

# WGFMU_createMergedPattern
WGFMU_AXIS_OFFSET                       = 9000
WGFMU_AXIS_TIME                        = WGFMU_AXIS_OFFSET + 0
WGFMU_AXIS_VOLTAGE                     = WGFMU_AXIS_OFFSET + 1

# WGFMU_getStatus, WGFMU_getChannelStatus
WGFMU_STATUS_OFFSET                     = 10000
WGFMU_STATUS_COMPLETED                 = WGFMU_STATUS_OFFSET + 0
WGFMU_STATUS_DONE                      = WGFMU_STATUS_OFFSET + 1
WGFMU_STATUS_RUNNING                   = WGFMU_STATUS_OFFSET + 2
WGFMU_STATUS_ABORT_COMPLETED          = WGFMU_STATUS_OFFSET + 3
WGFMU_STATUS_ABORTED                  = WGFMU_STATUS_OFFSET + 4
WGFMU_STATUS_RUNNING_ILLEGAL          = WGFMU_STATUS_OFFSET + 5
WGFMU_STATUS_IDLE                     = WGFMU_STATUS_OFFSET + 6

# WGFMU_isMeasureEventCompleted
WGFMU_MEASURE_EVENT_OFFSET              = 11000
WGFMU_MEASURE_EVENT_NOT_COMPLETED     = WGFMU_MEASURE_EVENT_OFFSET + 0
WGFMU_MEASURE_EVENT_COMPLETED         = WGFMU_MEASURE_EVENT_OFFSET + 1

# WGFMU_setMeasureEvent
WGFMU_MEASURE_EVENT_DATA_OFFSET         = 12000
WGFMU_MEASURE_EVENT_DATA_AVERAGED     = WGFMU_MEASURE_EVENT_DATA_OFFSET + 0
WGFMU_MEASURE_EVENT_DATA_RAW          = WGFMU_MEASURE_EVENT_DATA_OFFSET + 1

