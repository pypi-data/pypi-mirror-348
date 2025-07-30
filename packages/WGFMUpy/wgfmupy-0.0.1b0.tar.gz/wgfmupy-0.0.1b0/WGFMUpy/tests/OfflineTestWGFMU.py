from user_param import *
import WGFMUpy
from matplotlib import pyplot as plt
import util_wgfmu

if __name__ == '__main__':

    WGFMU = WGFMUpy.WGFMU_class()
    WGFMU.openLogFile('wgfmu.log')

    channels = util_wgfmu.WGFMU_singlePulse(WGFMU=WGFMU, voltage=Vr, read=True, t_pulse_read=t_pulse_read,
                                            read_interval=read_interval, start_read_time=start_read_time, fall_time=fall_time,
                                            rise_time=rise_time, number_of_read_points=number_of_read_points, topChannel=topChannel,
                                            bottomChannel=bottomChannel)

    # WGFMU.setMeasureMode(channel_id=channels['reference'], measure_mode=WGFMU_MEASURE_MODE_CURRENT)
    # WGFMU.setMeasureMode(channel_id=channels['pulse'], measure_mode=WGFMU_MEASURE_MODE_VOLTAGE)

    # events = WGFMU.getMeasureEvents(channels['reference'])
    # for measId, event in enumerate(events):
    #    event_attr = WGFMU.getMeasureEventAttribute(bottomChannel, measId)
    measure_times = WGFMU.getMeasureTimes(channel_id=channels['reference'], offset=0)
    measure_times = WGFMU.getMeasureTimes(channel_id=channels['pulse'], offset=0)

    WGFMU.exportAscii('Test.csv')

    TE_time, TE_voltage = WGFMU.getForceValues(topChannel)
    BE_time, BE_voltage = WGFMU.getForceValues(bottomChannel)

    timeCommon = np.hstack((TE_time, BE_time))
    timeCommon = np.unique(timeCommon)
    timeCommon = np.sort(timeCommon)
    TE_voltage_interp = np.interp(timeCommon, TE_time, TE_voltage)
    BE_voltage_interp = np.interp(timeCommon, BE_time, BE_voltage)
    plt.plot(timeCommon, TE_voltage_interp-BE_voltage_interp, '.-', label='TE-BE programmed waveform')
    plt.plot(measure_times, np.zeros(measure_times.shape), 'x', label='measure sampling points')
    plt.xlabel('time')
    plt.ylabel('voltage')
    plt.legend()
    plt.show()