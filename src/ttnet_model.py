'''
Parameters for the TTW time and energy model
Glossy values from the DPP2-cc430 implementation

See `numericalModel_TTW.xslx` for details
'''

import math

# == Radio parameters ==
L_cal       = 3         # Bytes Length of calibration Bytes
L_header    = 5         # Bytes Length of Glossy header
Rbits       = 250       # bit/ms Radio bit rate

# == Glossy parameters
Tcal        = 0.096     # ms Length of calibration Bytes
Theader     = 0.16      # ms Length of LWB/Glossy header
Twu_data    = 0.13      # ms Wake-up time at slot start (radio off)
Twu_control = 1.2       # ms Radio start time for sync packets (radio off)
Tstart_slot = 0.100883333333333 # ms Radio start time (radio on)
Td          = 0.174671212121212 # ms Software delay between flood phases
TdeepWU     = 0.7417    # ms Additional setup time after from deep sleep

# == TTnet implementation parameters
L_beacon        = 2     # Bytes Beacon size
T_gap           = 1.5   # ms Gap time
T_gap_control   = 1.5   # ms Gap time (post_control)
T_guard         = 0.1   # ms Guard time Same for control and data slots (included in T_gap)
T_preprocess    = 2     # ms Pre-process time
T_switch        = 0.3   # ms Switch between RX/TX Includes the time for preamble and sync bytes
T_slack         = 0.25  # ms Slack time in T_slot_min() macro
T_slot_base     = 0.5   # ms Granularity of T_slot values
T_post_cb       = 1     # ms Time for the on_slot_post_cb() of the last slot [to measure, depends on the application]
T_round_end     = 1.5   # ms Time for state-keeping at the end of the Baloo round [upper-bounded to 0.5ms]

def compute_T_beacon(H,N):
    '''
    T_beacon = T_guard + (H + 2*N -1) * (8*( L_header + L_beacon )/Rbits + T_switch) + T_slack

    computed in ms
    '''
    return T_guard + (H + 2*N -1) * (8*( L_header + L_beacon )/Rbits + T_switch) + T_slack

def compute_T_slot(H,N,L):
    '''
    T_slot(L) = ceil( (H + 2*N -1) * (8*( L_header + L )/Rbits + T_switch) + T_slack )

    rounded up to T_slot_base
    computed in ms
    '''
    T_slot = (H + 2*N -1) * (8*( L_header + L )/Rbits + T_switch) + T_slack

    # round up to T_slot_base
    T_slot = T_slot_base * math.ceil(T_slot / T_slot_base)

    return T_slot

def compute_T_round(H,N,L,B):
    '''
    T_round(B,L) = T_guard + T_preprocess + T_beacon + T_gap_control + B*T_slot(L) + (B-1)* T_gap + T_round_end
    '''
    T_beacon = compute_T_beacon(H,N)
    T_slot   = compute_T_slot(H,N,L)
    return T_guard + T_preprocess + T_beacon + T_gap_control + B*T_slot + (B-1)* T_gap + T_round_end

def compute_T_on_beacon(H,N):
    '''
    T^on_beacon = T_start_slot + T_guard + (H + 2*N -1) * (T_d + T_cal + T_header + 8*L_beacon/Rbits)
    '''
    return Tstart_slot + T_guard + (H + 2*N -1) * (Td + Tcal + Theader + 8*L_beacon/Rbits)

def compute_T_on_slot(H,N,L):
    '''
    T^on_slot(L) = T_start_slot + T_guard + (H + 2*N -1) * (T_d + T_cal + T_header + 8*L/Rbits)
    '''
    return Tstart_slot + T_guard + (H + 2*N -1) * (Td + Tcal + Theader + 8*L/Rbits)

def compute_T_on_round(H,N,L,B):
    '''
    T^on_round = T^on_beacon + B*T^on_slot(L)
    '''
    T_on_beacon = compute_T_on_beacon(H,N)
    T_on_slot   = compute_T_on_slot(H,N,L)
    return T_on_beacon + B*T_on_slot

def compute_energy_saving(H,N,L,B):
    '''
    E = (T^on_no-round - T^on_round) / T^on_no-round
    T^on_no-round(B,L) = B * (T^on_beacon + T^on_slot(L))
    '''
    T_on_beacon   = compute_T_on_beacon(H,N)
    T_on_slot     = compute_T_on_slot(H,N,L)
    T_on_round    = compute_T_on_round(H,N,L,B)
    T_on_no_round = B*(T_on_slot + T_on_beacon)
    return (T_on_no_round - T_on_round) / T_on_no_round
