import glob
import numpy as np
import os
from astropy.table import Table

#location of data
home_base = '/bulk/finnegan1/jtrump/data/hstgrism/gdn_g102/'

#potential emission lines (all)
potential_lines = ['OIII','OIIIx','HeI','HeII','SII','SIII','Ha','Hb','Hg','Hd','OII']

#master arrays to be built
master_IDs = np.array([])
master_flux = np.zeros([2, len(potential_lines)])
master_error = np.zeros([2, len(potential_lines)])

#number of pointings for outermost loop
pointings = np.arange(1, 29)

for num in pointings:

    print(num)
    
    #working directory to be looped through
    working_dir = 'GDN' + str(num) + '_extractions'

    os.chdir(home_base + working_dir)

    #okay, so I’m randy
    #list of all linefit files in a given directory
    file_list = glob.glob('*.linefit.dat')

    #arrays to be filled with values
    flux_values  = np.zeros([len(file_list),len(potential_lines)])
    error_values = np.zeros([len(file_list),len(potential_lines)])
    ID_nums = np.array([])

    for k in range(0, len(file_list)):
        obj_linefit = Table.read(file_list[k], format = 'ascii')
    
        #IF-ELSE TO CORRECT FOR FILE NAMES
        if num < 10:
            ID_temp = int(file_list[k][10:15])
        elif num >= 10:
            ID_temp = int(file_list[k][11:16])
            
        ID_nums = np.append(ID_nums, ID_temp)
    
        for i in range(0, len(obj_linefit)):
            for j in range(0, len(potential_lines)):
                if obj_linefit['line'][i] == potential_lines[j]:
                    flux_values[k][j] = obj_linefit['flux'][i]
                    error_values[k][j] = obj_linefit['error'][i]

    #Append or concatenate data to master arrays
    master_IDs = np.append(master_IDs, ID_nums)
    master_flux = np.concatenate((master_flux, flux_values), axis = 0)
    master_error = np.concatenate((master_error, error_values), axis = 0)

master_flux = np.delete(master_flux, 0, axis = 0)
master_flux = np.delete(master_flux, 0, axis = 0)
master_error = np.delete(master_error, 0, axis = 0)
master_error = np.delete(master_error, 0, axis = 0)

'''
print(len(master_IDs))
print(master_flux.shape)
print(master_error.shape)
'''

#get RAs and DECs

os.chdir(home_base)

Candel_id_comp, RA_comp, DEC_comp, z_G102_comp, z_flag_comp = np.loadtxt('gdn.candels.grismonly.cat', dtype = 'float32', unpack = True, usecols = [0, 1, 2, 3, 5])

RA = np.array([])
DEC = np.array([])
z_G102 = np.array([])
z_flag = np.array([])

for i in range(0, len(master_IDs)):
    idx = np.abs(Candel_id_comp - master_IDs[i]).argmin()

    if Candel_id_comp[idx] != master_IDs[i]:
        print('HOLLLLLY FUGGGGGGGGGG!!!!!!')

    RA = np.append(RA, RA_comp[idx])
    DEC = np.append(DEC, DEC_comp[idx])
    z_G102 = np.append(z_G102, z_G102_comp[idx])
    z_flag = np.append(z_flag, z_flag_comp[idx])
    
master_flux = np.transpose(master_flux)
OIII_f = master_flux[0]
OIIIx_f = master_flux[1]
HeI_f = master_flux[2]
HeII_f = master_flux[3]
SII_f = master_flux[4]
SIII_f = master_flux[5]
Ha_f = master_flux[6]
Hb_f = master_flux[7]
Hg_f = master_flux[8]
Hd_f = master_flux[9]
OII_f = master_flux[10]

master_error = np.transpose(master_error)
OIII_e = master_error[0]
OIIIx_e = master_error[1]
HeI_e = master_error[2]
HeII_e = master_error[3]
SII_e = master_error[4]
SIII_e = master_error[5]
Ha_e = master_error[6]
Hb_e = master_error[7]
Hg_e = master_error[8]
Hd_e = master_error[9]
OII_e = master_error[10]

t = Table([master_IDs,RA,DEC,z_G102,z_flag,
           OIII_f,OIII_e,
           OIIIx_f,OIIIx_e,
           HeI_f,HeI_e,
           HeII_f,HeII_e,
           SII_f,SII_e,
           SIII_f,SIII_e,
           Ha_f,Ha_e,
           Hb_f,Hb_e,
           Hg_f,Hg_e,
           Hd_f,Hd_e,
           OII_f,OII_e],
    names=('Candels ID','RA','DEC','Z_G102','z_flag',
           'OIII_f','OIII_e',
           'OIIIx_f','OIIIx_e',
           'HeI_f','HeI_e',
           'HeII_f','HeII_e',
           'SII_f','SII_e',
           'SIII_f','SIII_e',
           'Ha_f','Ha_e',
           'Hb_f','Hb_e',
           'Hg_f','Hg_e',
           'Hd_f','Hd_e',
           'OII_f','OII_e'))
os.chdir('/astro/ugrads/apm5587/research')
t.write('Master_Catalog',format='ascii')
