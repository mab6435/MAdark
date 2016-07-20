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

print(len(RA))
