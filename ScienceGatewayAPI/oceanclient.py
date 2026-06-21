def Chart(s, n):
    '''oceanclient.Chart(s, n) is hardwired into a demonstration data API. The source data is
    from the Regional Cabled Array program, Oregon Slope Base shallow profiler. The function
    returns two pandas Dataframes: one for temperature and one for salinity. It also creates 
    a matplotlib chart of the data. Argument 's' is a date in January 2022 formatted as '2022-01-03'. 
    Argument 'n' is an integer from 1 to 9 inclusive which is the profile index for that day.'''
    
    import requests, time, pandas as pd
    from numpy import datetime64 as dt64, timedelta64 as td64
    from matplotlib import pyplot as plt

    toc = time.time()

    # convert Chart() arguments to API-format strings
    day=str(int(s[8:10]))
    index=str(n)

    # Step 1: Look up the time range for the chosen profile
    profile_request = 'https://oceanography.azurewebsites.net/api/profile?day=' + day + '&index=' + index
    profile_response = requests.get(profile_request)
    if not profile_response.status_code == 200: print('uh oh profile response was not 200')
    r = profile_response.json()
    starttime = r['ascent start time'].replace(' ', '%20')
    stoptime  = r['descent start time'].replace(' ', '%20')

    # Step 2: Retrieve temp and salinity data for that time range
    sensors_request = 'https://oceansensors.azurewebsites.net/api/sensors?start=' + starttime + '&stop=' + stoptime
    sensors_response = requests.get(sensors_request)
    if not sensors_response.status_code == 200: print('uh oh sensors response was not 200')
    r = sensors_response.json()
    print('data query result type:', type(r), 'with', len(r), 'elements')
    
    # Step 3: Translate the data to simple lists: sensor, depth and timestamp
    T, Tz, Tt, S, Sz, St = [], [], [], [], [], []
    for d in r:
        if 'temp' in d:       T.append(d['temp']);     Tz.append(d['depth']); Tt.append(d['id'])
        elif 'salinity' in d: S.append(d['salinity']); Sz.append(d['depth']); St.append(d['id'])
    
    tic = time.time()
    print('prep time', str(round(tic - toc,2)), 'seconds; data vector length:', len(T))

    # Step 4: Create a matplotlib chart of this data
    Trng, Srng     = [7,11], [32,34]                     # expected data ranges
    Tlbl, Slbl     = 'Temp deg C', 'Salinity ppt'        # sensor labels
    Tcolor, Scolor = 'red', 'blue'                       # plot colors
    wid, hgt       = 7, 5.5                                # chart size
    z0, z1         = 200, 0                              # profile depth range
    
    fig, ax = plt.subplots(1, 1, figsize=(wid, hgt), tight_layout=True); axtwin = ax.twiny()
    ax.plot(    T, Tz, ms = 4., color=Tcolor, mfc=Tcolor)
    axtwin.plot(S, Sz, ms = 4., color=Scolor, mfc=Scolor)
    
    ax.set(title = Tlbl + ' (' + Tcolor + ', lower x-axis) and ' + Slbl + ' (' + Scolor + ', upper x-axis)')
    ax.set(    xlim = (Trng[0], Trng[1]), ylim = (z0, z1))
    axtwin.set(xlim = (Srng[0], Srng[1]), ylim = (z0, z1))

    # of nine daily profiles: one is intentionally at midnight, one is at noon
    # the expected time ranges are hardcoded to annotate this in the chart
    midn0 = td64( 7*60 + 10, 'm')        # 7 hours 10 minutes
    midn1 = td64( 7*60 + 34, 'm')        # 7 hours 34 minutes
    noon0 = td64(20*60 + 30, 'm')        # 20 hours 30 minutes
    noon1 = td64(20*60 + 54, 'm')        # 20 hours 54 minutes
    startMsg = 'Start UTC: ' + Tt[0][0:21]
    data_start = dt64(Tt[0])
    date_start = dt64(Tt[0][0:10])
    delta_t = data_start - date_start
    if delta_t > midn0 and delta_t < midn1: startMsg += " MIDNIGHT local"
    if delta_t > noon0 and delta_t < noon1: startMsg += " NOON local"
    xlabel = Trng[0] + 0.2*(Trng[1] - Trng[0])
    ylabel = 10
    ax.text(xlabel, ylabel, startMsg)

    # Step 5: Return the two dataframes
    return pd.DataFrame({'Timestamp': Tt, 'depth': Tz, 'temp': T}), \
           pd.DataFrame({'Timestamp': St, 'depth': Sz, 'salinity': S})