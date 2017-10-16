import datetime
import numpy as np
import pandas as pd


def get_ts_range(init_dt, end_dt, ts_range=900):
    time_ranges = []
    i = 0
    while (init_dt+i*datetime.timedelta(seconds=ts_range)) <= end_dt:
        time_ranges.append(init_dt+i*datetime.timedelta(seconds=ts_range))
        i += 1
    return time_ranges


def get_floor_range(dtime, min_range=15):
    floor_interval = datetime.datetime(dtime.year, dtime.month, dtime.day, dtime.hour,
                                       dtime.minute - (dtime.minute % min_range), 0)
    return floor_interval


def get_ceil_range(dtime, min_range=15):
    floor_interval = get_floor_range(dtime, min_range=min_range)
    ceil_interval = floor_interval + datetime.timedelta(seconds=min_range*60)
    return ceil_interval


def get_times_by_interval(dt_ini, dt_end):
    # Compute floor and ceil interval limits
    init = datetime.datetime(dt_ini.year, dt_ini.month, dt_ini.day, dt_ini.hour, dt_ini.minute - (dt_ini.minute % 15), 0)
    endt = datetime.datetime(dt_end.year, dt_end.month, dt_end.day, dt_end.hour, dt_end.minute - (dt_end.minute % 15), 0)
    endt = endt + datetime.timedelta(seconds=900)
    
    # Assign times
    interval_ranges = get_ts_range(init, endt, 900)
    times = np.zeros(len(interval_ranges))
    times[0] = (dt_ini - interval_ranges[0]).total_seconds()
    times[-1] = (interval_ranges[-1] - dt_end).total_seconds()
    times[1:-1] = 900
    
    return interval_ranges, times


def read_blood_glucose():
    blood_glucose = pd.read_csv('input/blood-glucose.csv', header=None,
                                names=['times', 'blood_glucose'])
    blood_glucose = blood_glucose[~ pd.isnull(blood_glucose['blood_glucose'])]
    f_datetime = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S+00:00')
    blood_glucose['times'] = blood_glucose['times'].apply(f_datetime)
    return blood_glucose


def read_motion():
    names=['times', 'stationary', 'walking', 'running', 'automotive', 'cycling']
    motion = pd.read_csv('input/motion.tsv', sep='\t', names=names, header=None)
    f_datetime = lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    motion['times'] = motion['times'].apply(f_datetime)
    return motion

    
def get_blood_std_48h(dtime, motion, blood_glucose):
    time_ranges_blood, blood_glucose_interp = get_blood_data(motion, blood_glucose)
    dtime = get_floor_range(dtime, min_range=15)
    init_t = dtime - datetime.timedelta(seconds=2*24*60*60)
    try:
        idx = time_ranges_blood.index(init_t)
        blood = blood_glucose_interp[idx:]
        blood = blood[blood == 0]
        std_48h = blood.std()
    except:
        raise IndexError("Datetime not in the range of the available data.")
    return std_48h

    
def get_blood_data(motion, blood_glucose):
    # Get time ranges of the whole data
    init_dt = datetime.datetime(2017, 5, 23, 0, 0)
    end_dt = datetime.datetime(2017, 6, 3, 0, 0)
    time_ranges = get_ts_range(init_dt, end_dt, 900)
    
    times = list(motion['times'])
    times_intervals = np.zeros((len(time_ranges), 5))
    col_activities = ['stationary', 'walking', 'running', 'automotive', 'cycling']

    for i_col, col in enumerate(col_activities):
        idxs = np.where(np.diff(motion[col].as_matrix()) == -1)[0]
        # For each interval of activity
        for i in idxs:
            dt_ini = times[i]
            dt_end = times[i+1]
            # Fill times activity
            interval_ranges, times_intervals_range = get_times_by_interval(dt_ini, dt_end)

            i_init = time_ranges.index(interval_ranges[0])
            for i_i in range(len(times_intervals_range)):
                times_intervals[i_init + i_i, i_col] += times_intervals_range[i_i]

    times_activities_48h = time_ranges[192:]
    times_intervals_48h = np.zeros((len(times_intervals)-192, 5))
    std_intervals_48h = np.zeros((len(times_intervals)-192, 5))

    for i in range(len(times_intervals)-192):
        times_intervals_48h[i] = times_intervals[i:i+192].sum(0)
        std_intervals_48h[i] = times_intervals[i:i+192].std(0)
        
    # Compute and interpolate blood glucose
    init_time = get_floor_range(blood_glucose.times.iloc[0], 15)
    endt_time = get_ceil_range(blood_glucose.times.iloc[-1], 15)
    time_ranges_blood = get_ts_range(init_time, endt_time, 900)

    blood_glucose_interp = np.zeros(len(time_ranges_blood))
    blood_times = list(blood_glucose.times)
    for i_time in range(len(blood_times)):
        try:
            idx = time_ranges_blood.index(blood_times[i_time])
            blood_glucose_interp[idx] = blood_glucose.blood_glucose.iloc[i_time]
        except:
            pass

    idxs = np.where(blood_glucose_interp)[0]
    # TOImprove: better interpolation
    blood_glucose_interp = np.interp(range(len(blood_glucose_interp)), idxs,
                                     blood_glucose_interp[idxs])
    
    return time_ranges_blood, blood_glucose_interp
