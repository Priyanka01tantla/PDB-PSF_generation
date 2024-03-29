import os
import sys

# This should specify the path to the install pyCHARMM library
pyCHARMM_LIB = '/home/priyanka/miniconda3/envs/charmm/lib'
if os.getenv('CHARMM_LIB_DIR') == None:
    os.environ['CHARMM_LIB_DIR'] = pyCHARMM_LIB
    print(os.getenv('CHARMM_LIB_DIR'))

# These are a subset of the pycharmm modules that were installed when
# pycharmm was installed in your python environment
import pycharmm
import pycharmm.generate as gen
import pycharmm.ic as ic
import pycharmm.coor as coor
import pycharmm.energy as energy
import pycharmm.dynamics as dyn
import pycharmm.nbonds as nbonds
import pycharmm.minimize as minimize
import pycharmm.crystal as crystal
import pycharmm.image as image
import pycharmm.psf as psf
import pycharmm.read as read
import pycharmm.write as write
import pycharmm.settings as settings
import pycharmm.cons_harm as cons_harm
import pycharmm.cons_fix as cons_fix
import pycharmm.select as select
import pycharmm.shake as shake

from pycharmm.lib import charmm as libcharmm
import argparse

import pandas as pa
import numpy as np

file = pa.read_csv('ic_atoms_930.csv')
read.rtf('top_all36_cgenff.rtf')
read.prm('nonbfix.prm', flex=True)
    
parser = argparse.ArgumentParser(prog='ProgramName')

parser.add_argument('-i', '--index',type= int, default=0) 
                    
# file['m1'] = file['m1'].astype("string")
# file['m2'] = file['m2'].astype("string")
# file['m3'] = file['m3'].astype("string")
# file['resp_special'] = file['resp_special'].astype("string")

# for i in range(len(file)):    
#     if i == 3:
#         break

args = parser.parse_args()

i = args.index
    
if (type(file.m1[i]) != type(np.nan)) and (type(file.m2[i]) != type(np.nan)) and (type(file.m3[i]) != type(np.nan)) and (type(file.resp_special[i]) != type(np.nan)):
    print(str(file.m1[i]),file.m2[i],file.m3[i],str(file.resp_special[i]),i)
   
    read.sequence_string(str(file.resp_special[i]))
    gen.new_segment(seg_name=str(file.resp_special[i]), setup_ic=True)

    # equivalent to the CHARMM scripting command: ic param
    ic.prm_fill(replace_all=False)
    # equivalent to the CHARMM scripting command: ic seed 1 CAY 1 CY 1 N
    #ic.seed(res1=1, atom1='CAY', res2=1, atom2='CY', res3=1, atom3='N')
    ic.seed(res1=1, atom1=str(file.m1[i]), res2=1, atom2=str(file.m2[i]), res3=1, atom3=str(file.m3[i]))
    
    # equivalent to the CHARMM scripting command: ic build
    ic.build()
    
    # The coor orie command is useful to expose since it allows one to
    # orient the system in preparation for other calculations
    # equivalent to the CHARMM scripting command: coor orient
    coor.orient(by_rms=False,by_mass=False,by_noro=False)
    # equivalent to the CHARMM scripting command: print coor
    #coor.show()
    # If pdb directory doesn't alrady exist make it here.
    if not os.path.isdir('pdb_03'): os.system('mkdir pdb_03')
    # equivalent to the CHARMM scripting command: write coor pdb name pdb/initial.pdb
    write.coor_pdb('pdb_03/'+str(file.resp_special[i])+'.pdb') 
    
    write.psf_card('pdb_03/'+str(file.resp_special[i])+'.psf')
    
