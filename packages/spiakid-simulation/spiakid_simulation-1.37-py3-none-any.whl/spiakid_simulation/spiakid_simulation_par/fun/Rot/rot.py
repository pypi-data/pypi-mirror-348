import numpy as np
from scipy import interpolate
from astropy.coordinates import SkyCoord, EarthLocation, Angle, ICRS, FK5
from astropy.timeseries import TimeSeries
from astropy.time import Time
from astropy import units as u


def Rotation(rotation, altguide, azguide, latitude, posx, posy, exptime, pxnbr, pxsize):
               
  if rotation == True:
    guide_alt_az = [altguide,azguide]
    coo_star=[posx, posy]
    rot, evalt, alt_az_t, pos, star_ra_dec_t = rot_with_pixel_scale(latitude, guide_alt_az, coo_star, exptime, pxsize)
   
  else:
    t = np.linspace(0,exptime,exptime+1 )
    pos = [posx, posy]
    rot = [interpolate.interp1d([0,exptime],[posx,posy]),interpolate.interp1d([0,exptime],[t,t])]
    evalt = interpolate.interp1d([0,exptime],[np.pi/2,np.pi/2])
    alt_az_t =[altguide,azguide,0]
    star_ra_dec_t = [0,0,0]
  return(rot, evalt, alt_az_t, pos, star_ra_dec_t)


def rot_with_pixel_scale(telescope_latitude_rad, 
        guide_star_altaz,
        offset_star_xy,
        duration_sec,
        pixel_scale_arcsec=0.45):
    
    earth_rotation_rate = -7.292115*10**-5 # rad/s
    
    observer_location = EarthLocation(lon=17.89 * u.deg, 
                                      lat=telescope_latitude_rad * u.rad, 
                                      height=2200 * u.m)
    
    times = np.linspace(0, duration_sec, duration_sec + 1)
    observation_times = Time("2020-01-01 20:00:00", scale = 'utc', location = observer_location) + times * u.s

    alt, az = guide_star_altaz
    Xg, Yg, Zg = np.cos(alt) * np.cos(az), -np.cos(alt) * np.sin(az), np.sin(alt)
   
    guide_vector = np.array([Xg, Yg, Zg])
   
    S1_prime = np.array([offset_star_xy[0],offset_star_xy[1],0])*(pixel_scale_arcsec/3600*np.pi/180)

    R = np.array([
            [-np.sin(alt)*np.cos(az), np.sin(alt)*np.sin(az),np.cos(alt)],
            [-np.sin(az), -np.cos(az), 0],
            [np.cos(alt)*np.sin(az), -np.cos(alt)*np.sin(az),np.sin(alt)]
        ])
    
    # Coordonnées XYZ de S1
    S1 = guide_vector + np.transpose(R) @ S1_prime
  
    altaz_guide_history = [] 
    current_alt = []
    current_az = []
    pos_guide = []
    pos_star = []
    
    current_alt_star = []
    current_az_star = []
    for i, t in enumerate(times):
        theta = earth_rotation_rate * t
        
        
        # Rotation de la planete
        up = np.array([
                [np.cos(telescope_latitude_rad)**2 + np.sin(telescope_latitude_rad)**2 * np.cos(theta), -np.sin(telescope_latitude_rad) * np.sin(theta), (1 - np.cos(theta)) * np.cos(telescope_latitude_rad) * np.sin(telescope_latitude_rad)],
                [np.sin(telescope_latitude_rad) * np.sin(theta), np.cos(theta), -np.cos(telescope_latitude_rad) * np.sin(theta)],
                [(1 - np.cos(theta)) * np.cos(telescope_latitude_rad) * np.sin(telescope_latitude_rad), np.cos(telescope_latitude_rad) * np.sin(theta), np.sin(telescope_latitude_rad)**2 + np.cos(telescope_latitude_rad)**2 * np.cos(theta)]
            ])
        Sg_dt = up @ guide_vector
     
        Xg, Yg, Zg = Sg_dt
        current_alt.append(np.arcsin(Zg))
        current_az.append(-np.arctan2(Yg, Xg))
        
        S1_dt = up @ S1 
        X1, Y1, Z1 = S1_dt
    
   
        current_alt_star.append(np.arcsin(Z1))
        current_az_star.append(-np.arctan2(Y1, X1))

        r1_dt = S1_dt - Sg_dt
        
        R_dt =[
            [-Xg*Zg/np.sqrt((Xg**2+Yg**2)*(Xg**2+Yg**2+Zg**2)), -Yg*Zg/np.sqrt((Xg**2+Yg**2)*(Xg**2+Yg**2+Zg**2)), np.sqrt(Xg**2+Yg**2) / np.sqrt(Xg**2+Yg**2+Zg**2)],
            [Yg / np.sqrt(Xg**2 + Yg**2), -Xg / np.sqrt(Xg**2 + Yg**2), 0],
            [Xg / np.sqrt(Xg**2 + Yg**2 + Zg**2), Yg / np.sqrt(Xg**2 + Yg**2 + Zg**2), Zg / np.sqrt(Xg**2 + Yg**2 + Zg**2)]
        ]

        r1_prime_dt = R_dt @ r1_dt
        Sg_dt_prime = R_dt @ Sg_dt
        pos_guide.append(Sg_dt_prime)
        
        S1_dt_prime = R_dt @ S1_dt
        pos_star.append([S1_dt_prime[0]/(pixel_scale_arcsec/3600*np.pi/180), S1_dt_prime[1]/(pixel_scale_arcsec/3600*np.pi/180)])

    pos_star = np.array(pos_star)
    altaz_guide_history = np.array(altaz_guide_history)
    
    ev_alt = interpolate.interp1d(times, current_alt_star)
    ev_x = interpolate.interp1d(times, pos_star[:,0])
    ev_y = interpolate.interp1d(times, pos_star[:,1])

    ra_dec_history = []
    altaz_history = []

    ra_dec_star_history = []
    altaz_star_history = []

    ang = []
    meridian_alt = list(current_alt).index(np.max(current_alt))
    meridian_alt_star = list(current_alt_star).index(np.max(current_alt_star))

    for i in range(len(current_alt)):
        
        altaz_history.append([current_alt[i], current_az[i], i])
        altaz_star_history.append([current_alt_star[i], current_az_star[i]])

        dec = np.arcsin(np.sin(telescope_latitude_rad) * np.sin(current_alt[i]) + np.cos(telescope_latitude_rad)*np.cos(current_alt[i])*np.cos(current_az[i]))
        HA = np.arccos((np.sin(current_alt[i]) - np.sin(telescope_latitude_rad)*np.sin(dec))/(np.cos(telescope_latitude_rad)*np.cos(dec))) 
        
        dec_star = np.arcsin(np.sin(telescope_latitude_rad) * np.sin(current_alt_star[i]) + np.cos(telescope_latitude_rad)*np.cos(current_alt_star[i])*np.cos(current_az_star[i]))
        HA_star = np.arccos((np.sin(current_alt_star[i]) - np.sin(telescope_latitude_rad)*np.sin(dec_star))/(np.cos(telescope_latitude_rad)*np.cos(dec_star))) 
       
        ang.append(observation_times[i].sidereal_time(kind = 'apparent'))
        if i >= meridian_alt:
            ra = ang[i].to(u.rad) - HA  * u.rad
        else:
            ra = ang[i].to(u.rad)  + HA * u.rad
        
        
        if current_alt_star[0] < np.max(current_alt_star) and current_alt_star[-1] < np.max(current_alt_star):
            meridian_alt_star = list(current_alt_star).index(np.max(current_alt_star))
            if i >= meridian_alt_star:
                ra_star = ang[i].to(u.rad) - HA_star *u.rad
            else:
                ra_star = ang[i].to(u.rad)  + HA_star *u.rad
        else:
           ra_star = ang[i].to(u.rad)  + HA_star *u.rad
        ra_dec_history.append([ra.value, dec])
        ra_dec_star_history.append([ra_star.value, dec_star])
    
    return ([ev_x, ev_y], ev_alt,altaz_star_history, pos_star, ra_dec_star_history)