import numpy as np

# Configuration Flags
USE_B1500 = True  # If False, skip B1500-related functions and use fake values
SMUGateBiasing = False  # Use SMU for gate biasing (only affects runRandVDSP)
MEASURE = False
SAVE = False

B1500_addr = "GPIB0::17::INSTR"


# SMU and WGFMU Channel IDs
SMU1 = 201
SMU2 = 301
SMU3 = 401
SMU4 = 501
WGFMU1 = 101
WGFMU2 = 102

# Electrical and Timing Parameters
t_pulse = 500e-6  # Pulse width for writing
Vr = 0.2          # Read pulse amplitude
t_pulse_read = 100e-9   # Pulse width for reading
V_max = 3.3       # Maximum voltage (do not exceed)
V_min = -3.3      # Minimum voltage
Vgateread = 3.3
Vgatemin = 1.5
Vgatemax = 1.07
VgateReset = 3.3
VgateSet = 1.5

# Physical Channel Assignments
topChannel = WGFMU1       # Top electrode channel
bottomChannel = WGFMU2    # Bottom electrode channel
GateSMU = SMU2            # SMU channel for transistor gate
BodySMU = SMU4            # SMU channel for transistor body


rise_time = 10e-9
fall_time = 10e-9

start_read_time = 0
read_interval = 10e-9

end_read_time = t_pulse_read
read_duration = end_read_time - start_read_time
number_of_read_points = int(np.floor(read_duration / read_interval * 1e8) / 1e8)