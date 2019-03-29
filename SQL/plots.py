import matplotlib.pyplot as plt 

# Basic plotting functions for visualising MWATS data. 
# Martin.Bell@uts.edu.au

# Generic function for plotting light-curves and stats.
def plot_lc(source):
    all = filtered_raw_data[filtered_raw_data.source_id == source]
    all = all.sort_values(by='jd')
    plt.figure(figsize=(7, 8))
    plt.subplot(2,1,1)
    f = list(all.raw_peak_flux)
    s_stats = stats[stats.source_id == source]
    plt.title(str(source)+' RA='+str(s_stats.ra)+' DEC='+str(s_stats.dec))
    #plt.title('Source = '+str(source)+' (GLEAM '+all.ra_str[0]+' '+all.dec_str[0]+')')
    plt.plot(list(f), 'k.', label='Flux')
    plt.xlabel('Observation Number')
    #plt.ylim(np.mean(f)*0.8, np.mean(f)*1.2)
    plt.ylabel('Flux (Jy)')
    
    # Non-averaged
    plt.subplot(2,1,2)
    plt.plot(all.jd, all.raw_peak_flux, 'k.', label='Flux')
    ts = []
    ys = []
    for t in all.jd:
        sli = stats[stats.source_id == source]
        y = (sli.grad * t) + sli.y_int
        ts.append(float(t))
        ys.append(float(y))
    plt.plot(ts,ys,'k-.', label='$\\nabla_{S} = $'+str( round(float(sli.sig),2) ))
    
    # Averaged 
    avg = filtered_raw_avg_data[filtered_raw_avg_data.source_id == source]
    plt.errorbar(avg.mean_jd, avg.median_flux, avg.std_flux, fmt='ro', label="Median flux", markersize=10)
    ts = []
    ys = []
    for t in avg.mean_jd:
        sli = stats[stats.source_id == source]
        y = (sli.avg_grad * t) + sli.avg_y_int
        ts.append(float(t))
        ys.append(float(y))
    plt.plot(ts,ys,'r-.', label='Median $\\nabla_{S} = $'+str( round(float(sli.avg_sig),2) ))
    #plt.ylim(np.mean(f)*0.8, np.mean(f)*1.2)
    plt.xlabel('Time (JD)')
    plt.ylabel('Flux (Jy)')
    plt.legend()
    plt.close

################################################
# Function to plot modulation versus location. 
def plot_mod_set(set, label):
    fig, ax = plt.subplots(figsize=(14, 7))
    plt.scatter(set.ra, set.dec, alpha=0.2, edgecolors='k', lw=1, s=set.avg_Mod, color='red', label=label)
    #plt.scatter(set_neg.ra, set_neg.dec, alpha=0.2, edgecolors='k', lw=1, s=set_neg_mod*10, color='blue', label='Negative sig grad')
    
    # Show the locations of the drift scan centres
    plt.plot([0, 360],[-55, -55], 'k--', linewidth=2, label='Drift scan centre')
    plt.plot([0, 360],[-27, -27], 'k--', linewidth=2)
    plt.plot([0, 360],[3.6, 3.6], 'k--', linewidth=2)
    # Show the cross over regions of the drift scan centres. 
    plt.plot([0, 360],[-41, -41], 'k-.', linewidth=1, label='Drift scan edge')
    plt.plot([0, 360],[-13, -13], 'k--', linewidth=1)
    
    # Plot the Galactic-Plane
    ra_G  = []
    dec_G = []

    for l_in in range(1, 360):
        c = SkyCoord(b=10*u.degree, l=l_in*u.degree, frame='galactic')
        ra_G.append(c.icrs.ra.degree),
        dec_G.append(c.icrs.dec.degree)
    plt.plot(ra_G, dec_G, 'b-')

    ra_G  = []
    dec_G = []

    for l_in in range(1, 360):
        c = SkyCoord(b=-10*u.degree, l=l_in*u.degree, frame='galactic')
        ra_G.append(c.icrs.ra.degree),
        dec_G.append(c.icrs.dec.degree)
    plt.plot(ra_G, dec_G, 'b-')   
    
    plt.xlim(0, 360)
    plt.ylim(-90, 30)
    plt.legend()
    
    ### Plot the A-Team ###
    plt.plot(139.5236, -12.095543, 'k+', markersize=20, label='Hydra A')
    plt.plot(79.957171, -45.778828, 'k+', markersize=20, label='Pic A')
    plt.plot(50.673825, -37.208227, 'k+', markersize=20, label='For A')
    plt.plot(252.783945, 4.992588, 'k+', markersize=20, label='Her A')
    plt.plot(201.365063, -43.019, 'k+', markersize=20, label='Cen A')
    plt.plot(300, -42, 'k+', markersize=20, label='Cyg A alias')
    plt.plot(80.893860, -69.756126, 'k+', markersize=20, label='LMC')
    plt.plot(187.7059, 12.39, 'k+', markersize=20, label='Vir A')
    
    plt.title(label)
    plt.xlabel('RA')
    plt.ylabel('DEC')

#################################################
# Function to plot gradient sources
def plot_grad_set(set_pos, set_neg, set_neg_mod, label):
    fig, ax = plt.subplots(figsize=(14, 7))
    plt.scatter(set_pos.ra, set_pos.dec, alpha=0.2, edgecolors='k', lw=1, s=set_pos.sig*10, color='red', label='Positive sig grad')
    plt.scatter(set_neg.ra, set_neg.dec, alpha=0.2, edgecolors='k', lw=1, s=set_neg_mod*10, color='blue', label='Negative sig grad')
    
    # Show the locations of the drift scan centres
    plt.plot([0, 360],[-55, -55], 'k--', linewidth=2, label='Drift scan centre')
    plt.plot([0, 360],[-27, -27], 'k--', linewidth=2)
    plt.plot([0, 360],[3.6, 3.6], 'k--', linewidth=2)

    # Show the cross over regions of the drift scan centres. 
    plt.plot([0, 360],[-41, -41], 'k-.', linewidth=1, label='Drift scan edge')
    plt.plot([0, 360],[-13, -13], 'k--', linewidth=1)
    
    plt.legend()
    
    # Plot the Galactic-Plane
    ra_G  = []
    dec_G = []

    for l_in in range(1, 360):
        c = SkyCoord(b=10*u.degree, l=l_in*u.degree, frame='galactic')
        ra_G.append(c.icrs.ra.degree),
        dec_G.append(c.icrs.dec.degree)
    plt.plot(ra_G, dec_G, 'b-')

    ra_G  = []
    dec_G = []

    for l_in in range(1, 360):
        c = SkyCoord(b=-10*u.degree, l=l_in*u.degree, frame='galactic')
        ra_G.append(c.icrs.ra.degree),
        dec_G.append(c.icrs.dec.degree)
    plt.plot(ra_G, dec_G, 'b-')   
    
    plt.xlim(0, 360)
    plt.ylim(-90, 30)
    
    plt.title(label)
    plt.xlabel('RA')
    plt.ylabel('DEC')
    
