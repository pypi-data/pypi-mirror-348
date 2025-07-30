def WGFMU_singlePulse(WGFMU, voltage=0, read=True, t_pulse_read=40e-9, rise_time=10e-9, fall_time=10e-9,
                      start_read_time=0, number_of_read_points=1000, read_interval=10e-9, topChannel=101,
                      bottomChannel=102):

    if voltage >= 0:
        channels = {
            'pulse': topChannel,
            'reference': bottomChannel
        }
    else:
        channels = {
            'pulse': bottomChannel,
            'reference': topChannel
        }

    WGFMU.clear()  # 9

    # pulse
    WGFMU.createPattern(pattern_name="pulse", initial_voltage=0)  # 0 ms, 0 V
    WGFMU.addVector(pattern_name="pulse", delta_time=rise_time, voltage=voltage)  # 10 ns rise time, Vr V
    WGFMU.addVector(pattern_name="pulse", delta_time=t_pulse_read - rise_time - fall_time,
                    voltage=voltage)  # t_read - 20 ns, Vr V
    WGFMU.addVector(pattern_name="pulse", delta_time=fall_time, voltage=0)  # 10 ns fall time, 0 V
    WGFMU.setMeasureEvent(pattern_name='pulse', event_name='Vmeas', time=start_read_time,
                          measurement_points=number_of_read_points, measurement_interval=read_interval,
                          averaging_time=10e-9, raw_data=WGFMU.MEASURE_EVENT_DATA_RAW)

    #  reference
    WGFMU.createPattern(pattern_name="reference", initial_voltage=0)  # 0 ms, 0 V
    WGFMU.addVector(pattern_name="reference", delta_time=rise_time, voltage=0)  # 10 ns rise time, 0 V
    WGFMU.addVector(pattern_name="reference", delta_time=t_pulse_read - rise_time - fall_time,
                    voltage=0)  # t_read - 20 ns, 0 V
    WGFMU.addVector(pattern_name="reference", delta_time=fall_time, voltage=0)  # 10 ns fall time, 0 V

    WGFMU.setMeasureEvent(pattern_name="reference", event_name="Imeas", time=start_read_time,
                          measurement_points=number_of_read_points, measurement_interval=10e-9, averaging_time=10e-9,
                          raw_data=WGFMU.MEASURE_EVENT_DATA_RAW)  # WGFMU.setMeasureEvent(pattern_name="meas", event_name="Imeas",time=0.00000001, measurement_points=1, measurement_interval=t_read - 0.00000002, averaging_time=t_read - 0.00000002, raw_data=WGFMU_MEASURE_EVENT_DATA_RAW)  # meas from 10 ns, 1 points, 0.01 ms interval, no averaging

    WGFMU.addSequence(channel_id=channels['pulse'], pattern_name="pulse", loop_count=1)  # 1 pulse output
    WGFMU.addSequence(channel_id=channels['reference'], pattern_name="reference", loop_count=1)  # 1 "pulse" output

    return channels
