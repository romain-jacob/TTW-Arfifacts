"""
Analysis functions related to the Time-Triggered Wireless project.

@author: Romain Jacob
@date: 10.04.2020
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import src.colors as colors
from src.ttnet_model import *
from src.ttnet_plots import *
import triscale

# Series list
serie_1 = {'label' : 'serie1',
           'node_list' : [1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15, 16,
                          17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 32, 33]}
serie_2 = {'label' : 'serie2',
           'node_list' : [1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15, 16,
                          17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 32, 33]}
serie_3 = {'label' : 'serie3',
           'node_list' : [1, 2, 3, 4, 6, 8, 10, 11, 13, 15, 16, 17,
                          18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33]}

linewidth_pt = 384
linewidth_px = 512 # https://www.ninjaunits.com/converters/pixels/points-pixels/

# ==============================================================================
def compute_KPIs(
    KPI_energy,
    KPI_round,
    Bs,
    Ls,
    H,
    N,
    to_plot=[],
    verbose=False
):

    # Result storage
    KPI_energy_values = []
    KPI_round_values  = []

    # Computing TTnet model values
    columns = [
        'L',
        'B',
        'round_model',
        'energy_model',]
    tmp = []
    for L in Ls:
        for B in Bs:
            tmp.append([
                L,
                B,
                compute_T_round(H,N,L,B),
                round(100*compute_energy_saving(H,N,L,B))
            ])
    df_summary = pd.DataFrame(tmp, columns=columns)

    raw_data_folder = Path('data_raw')
    out_data_folder = Path('data_processed')
    for serie_id in [serie_1, serie_2, serie_3]:

        # Retrieve data for a series
        df_all, df = parse_test_series(serie_id,
                                       raw_data_folder,
                                       out_data_folder,
                                       plot=False
                                      )

        # Temporary data storage
        tmp_nrg_column = []
        tmp_rd_column  = []

        for L in Ls:

            # Temporary data storage
            tmp_nrg = []
            tmp_rd  = []
            tmp_nrg_test = []
            tmp_rd_test  = []
            tmp_nrg_min  = []
            tmp_rd_max   = []

            for B in Bs:

                # Extract the data corresponding to a given (B,L,H,N) set
                x = (df.loc[(df['B_n_slots']==B) &
                            (df['L_payload_size']==L) &
                            (df['H']==H) &
                            (df['N']==N)]).dropna()

                # Compute the energy KPI
                data = x.energy_savings.values
                test, KPI_value = triscale.analysis_kpi(data, KPI_energy, to_plot, verbose=verbose)

                # Store intermediate results
                tmp_nrg.append(KPI_value)
                tmp_nrg_test.append(test)
                tmp_nrg_min.append(np.nanmin(data))
                if np.isnan(KPI_value):
                    # Negative value to indicate that the KPI could not be computed (not enough data samples)
                    tmp_nrg_column.append(-round(np.nanmin(data)))
                else:
                    tmp_nrg_column.append(round(KPI_value))

                # Compute the round length KPI
                data = x.T_round.values
                test, KPI_value = triscale.analysis_kpi(data, KPI_round, to_plot, verbose=verbose)

                # Store intermediate results
                tmp_rd.append(KPI_value/1000)
                tmp_rd_test.append(test)
                tmp_rd_max.append(np.nanmax(data)/1000)
                if np.isnan(KPI_value):
                    # Negative value to indicate that the KPI could not be computed (not enough data samples)
                    tmp_rd_column.append(-round(np.nanmax(data)/1000,2))
                else:
                    tmp_rd_column.append(round(KPI_value/1000,2))


            ## Store KPI values under two different format for later processing/displaying
            # Store the KPI values (1)
            KPI_energy_values.append({  'series':serie_id['label'],
                                        'L':L,
                                        'data':{
                                            'B':Bs,
                                            'KPI':tmp_nrg,
                                            'test':tmp_nrg_test,
                                            'max':tmp_nrg_min
                                        }
                                     })
            KPI_round_values.append({'series':serie_id['label'],
                                     'L':L,
                                     'data':{
                                         'B':Bs,
                                         'KPI':np.array(tmp_rd),
                                         'test':tmp_rd_test,
                                         'max':tmp_rd_max}})
        # Store the KPI values (2)
        df_summary[ 'energy_' + serie_id['label'] ] = tmp_nrg_column
        df_summary[ 'round_' + serie_id['label'] ]  = tmp_rd_column

    # Set payload and number of slots as indexes
    df_summary.set_index(['L','B'], inplace=True)

    # Reorder columns
    cols = list(df_summary.columns.values)
    cols_reorder = [ cols[k] for k in [3,5,7,0,2,4,6,1]]
    df_summary = df_summary[cols_reorder]

    # Print out details
    if verbose:
        print('Round lengths')

        for series in KPI_round_values:
            print(series['L'], series['data']['B'])
            print(series['data']['test'])
            print(series['data']['KPI'])
            print(series['data']['max'])
            print([compute_T_round(4,2,series['L'],b) for b in [5,10,30]])
            print()

        print('Energy savings')

        for series in KPI_energy_values:
            print(series['L'], series['data']['B'])
            print(series['data']['test'])
            print(series['data']['KPI'])
            print(series['data']['max'])
            print([100*compute_energy_saving(4,2,series['L'],b) for b in [5,10,30]])
            print()

    return KPI_energy_values, KPI_round_values, df_summary


# ==============================================================================
def parse_test_series(  series_data,
                        raw_data_folder,
                        out_data_folder,
                        force_computation=False,
                        H=4,
                        N=2,
                        plot=True,
                        plot_save=False,
                        plot_layout={},
                        verbose=False,
                        sample=None):

    # Series metadata
    serie               = series_data['label']
    node_lists          = series_data['node_list']
    print("Parsing %s ..." % serie)

    # Raw data
    raw_data_folder     = Path(raw_data_folder)
    raw_data_folder     = raw_data_folder / serie
    data_folder         = raw_data_folder / "results"
    logs_folder         = raw_data_folder / "results_error_logs"

    # Output data folder
    out_folder          = Path(out_data_folder)
    out_folder          = out_folder / serie
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    out_file            = out_folder / (serie+'_all.csv')
    metric_file         = out_folder / (serie+'_metrics.csv')

    # Plot folder
    plot_folder         = Path("plots")
    plot_folder         = plot_folder / serie

    # Debug counter
    counter_possible_time_sync_errors = 0

    if not force_computation:
        try:
            df_all = pd.read_csv(out_file)
            df_all.set_index('test_number', drop=True, inplace=True)
            df_metric = pd.read_csv(metric_file)
            df_metric.set_index('test_number', drop=True, inplace=True)
            print('%s : Processed data retrieved (not computed).' % serie)
            if plot:
                plot_series(df_all,
                            custom_layout=plot_layout,
                            save=plot_save,
                            plot_path=plot_folder,
                            prefix=serie+'_',
                            sample=sample)
            return df_all, df_metric
        except FileNotFoundError:
            print('No existing file found. Computing.')

    out_data = []
    out_data_labels = ['test_number',
                      'date_time',
                      'B_n_slots',
                      'L_payload_size',
                      'R_random_seed',
                      'H',
                      'N',
                      'node_id',
                      'T_round',
                      'T_round_1slot',
                      'T_on_round',
                      'T_on_without_round',
                      'energy_savings']

    metric_data = []
    metric_data_labels = ['test_number',
                      'date_time',
                      'B_n_slots',
                      'L_payload_size',
                      'R_random_seed',
                      'H',
                      'N',
                      'T_round',
                      'energy_savings']

    folder_list = [test_folder for test_folder in os.listdir(str(data_folder)) if os.path.isdir(os.path.join(str(data_folder), test_folder))]
    for test_folder in sorted(folder_list):

        # Collect test information from summary
        df_current = pd.read_csv( str(data_folder / test_folder / "testsummary.csv"), delimiter = ',')
        test_nb = df_current.at[0,"test_number"]
        payload = df_current.at[0,"L_payload_size"]
        n_slots = df_current.at[0,"B_n_slots"]
        rand_seed = df_current.at[0,"R_random_seed"]
        date_time = df_current.at[0,"date_time"]

        # Open the test serial log
        f = open( str(data_folder / test_folder / "serial.csv"), "r")

        test_result = np.zeros((len(node_lists), 5), dtype=np.float)
        node_index  = 0

        for node_id in node_lists:

            # reset file read offset
            f.seek(0, 0)

            # tmp log
            first_measure = True        # Flag for the first time we measure Tround
            nrg_log = []
            lat_log = []
            counter = 2* (n_slots + 1)  # number of lines with useful information to extract
            missed_error = 0            # number of times the node missed the control packet of a slot
                                        # -> abort scanning after twice:
                                        # -> T,E data becomes highly unreliable

            # read first line
            line = f.readline()
            while counter != 0 and line != '':
                if line[0]=='#':
                    line = f.readline()
                    continue

                tmp = line[0:-1].split(',')
                if int(tmp[2]) == node_id:

                    '''
                    `sched rcv` is printed when a node successfuly bootstrap.
                    The rest of the message shows the control message payload.
                    A value of `1` marks the round where the measurement is taken.
                    If a node bootstrap in the measuring round, the measured value is irrelevant,
                    as nodes start measuring from the start of the bootstrapping attempt.
                    -> Discard this value.
                    '''
                    if "sched rcv (1" in tmp[4]:
                        error_log = str(test_nb) + ' : Node ' + str(node_id) + ' bootstrapped on measured round'
                        error_log = error_log + '; discard it.'
                        if verbose:
                            print(error_log)
                        break

                    # Count the number of rounds with a slot miss
                    if "Missed 1 slots! Binary: 1" in tmp[4]:
                        missed_error += 1

                    # Count the number of rounds with a control miss
                    if "Schedule missed or corrupted" in tmp[4]:
                        missed_error += 1

                    if missed_error >= 2:
                        error_log = str(test_nb) + ' : Node ' + str(node_id) + ' multiple slot/control misses, data is unreliable'
                        error_log = error_log + '; discard it.'
                        if verbose:
                            print(error_log)
                        break

                    if "3] Missed 1 slots! Binary: 1" in tmp[4]:
                        counter_possible_time_sync_errors += 1
                        error_log = str(test_nb) + ' : Node ' + str(node_id) + ' may suffer from the time sync error'
                        error_log = error_log + '; discard it.'
                        if verbose:
                            print(error_log)
                        break

                    if "E: " in tmp[4]:
                        (trash, nrg) = tmp[4].split('E: ')
                        #print(nrg)
                        nrg_log.append(int(nrg))
                        counter -= 1

                    if "T: " in tmp[4]:
                        # Check that the first measurement happens in the
                        # correct round
                        if first_measure:
                            if "4] T: " in tmp[4]:
                                # Fine
                                first_measure = False
                            else:
                                # Nor fine
                                error_log = str(test_nb) + ' : Node ' + str(node_id) + ' missed first measure round'
                                error_log = error_log + '; discard it.'
                                if verbose:
                                    print(error_log)
                                break
                        (trash, lat) = tmp[4].split('T: ')
                        lat_log.append(int(lat))
                        counter -= 1

                line = f.readline()

            # Log test results
            if counter != 0:
                # Data is missing! Likely, this node failed to execute correctly
                # Discard all data from this node
                error_log = str(test_nb) + ' : Node ' + str(node_id) + ' missing some data'
                error_log = error_log + '; discard it.'
                if verbose:
                    print(error_log)

                # Log the node serial output for inspection
                log_file = str(test_nb) + "_" + str(node_id)
                log_file = logs_folder / log_file
                string = str(node_id) + "," + str(node_id) + ","
                cmd = "sed '/" + string + "/!d' " + str(data_folder / test_folder / "serial.csv") + "> " + str(log_file)
                os.system(cmd)

                test_result[node_index][0] = np.nan
                test_result[node_index][1] = np.nan
                test_result[node_index][2] = np.nan
                test_result[node_index][3] = np.nan
                test_result[node_index][4] = np.nan
            else:

                # double-check the values
                '''
                If the first measurement we have is smaller than the expected
                length of one round, this means the node missed the round
                where the measurement round took place (because it bootstrapped
                very late, or simply because it failed receiving the control packet).
                -> Discard the data from that node.
                '''
                T_round_1slot_theo = compute_T_round(H,N,payload,1)*1000 # in us
                if lat_log[0] < T_round_1slot_theo:
                    # We missed the round with B slots, discard data
                    test_result[node_index][0] = np.nan
                    test_result[node_index][1] = np.nan
                    test_result[node_index][2] = np.nan
                    test_result[node_index][3] = np.nan
                    test_result[node_index][4] = np.nan
                    error_log = str(test_nb) + ' : Node ' + str(node_id) + ' missed the measuring round'
                    error_log = error_log + '; discard it.'
                    if verbose:
                        print(error_log)
                else:
                    test_result[node_index][0] = nrg_log[0]         # T_on_round
                    test_result[node_index][1] = sum(nrg_log[1:])   # T_on_without_round
                    test_result[node_index][2] = lat_log[0]         # T_round
                    test_result[node_index][3] = max(lat_log[1:])   # T_round_1slot
                    test_result[node_index][4] = ((test_result[node_index][1]
                                                  - test_result[node_index][0])
                                                  / test_result[node_index][1])*100 # energy_savings

            # Save the node data
            out_data.append([
                                test_nb,
                                date_time,
                                n_slots,
                                payload,
                                rand_seed,
                                H,
                                N,
                                node_id,
                                test_result[node_index][2],
                                test_result[node_index][3],
                                test_result[node_index][0],
                                test_result[node_index][1],
                                test_result[node_index][4]
                            ])

            # Increment the node index
            node_index += 1

        # Compute the metrics for the test
        T_round            = np.nanmax(test_result,axis=0)[2]
        energy_savings     = np.nanmedian(test_result,axis=0)[4]
        if np.isnan(T_round) or energy_savings.min() < 0 or T_round.min() < 0:
            if verbose:
                print(str(test_nb) + ' completely failed!')
            T_round = np.nan
            energy_savings = np.nan
        # Save the metri data
        metric_data.append([
                            test_nb,
                            date_time,
                            n_slots,
                            payload,
                            rand_seed,
                            H,
                            N,
                            T_round,
                            energy_savings
                        ])

    # Save the DataFrames to csv
    df_metric = pd.DataFrame(metric_data, columns=metric_data_labels)
    df_metric.set_index('test_number', drop=True, inplace=True)
    df_metric.to_csv(metric_file)

    df_all = pd.DataFrame(out_data, columns=out_data_labels)
    df_all.set_index('test_number', drop=True, inplace=True)
    df_all.to_csv(out_file)

    # Debug outputs:
    if verbose:
        print('Number of possible time sync error: %d'
                % counter_possible_time_sync_errors)

    if plot:
        plot_series(df_all,
                    custom_layout=plot_layout,
                    save=plot_save,
                    plot_path=plot_folder,
                    prefix=serie+'_')

    return df_all, df_metric
