# In[20]:
import os.path
import datetime
# FireWorks functionality
from fireworks import LaunchPad
from fireworks.utilities.filepad import FilePad

from fireworks.utilities.dagflow import DAGFlow, plot_wf
# sample for plotting fraph:
#    plot_wf(wf_list[0], view='combined', labels=True, target='wf.png', bbox=(2400,2400))


timestamp = datetime.datetime.now()
yyyymmdd = timestamp.strftime('%Y%m%d')
yyyy_mm_dd = timestamp.strftime('%Y-%m-%d')

# plotting defaults
visual_style = {}

# generic plotting defaults
visual_style["layout"] = 'kamada_kawai'
visual_style["bbox"] = (1600, 1200)
visual_style["margin"] = [400, 100, 400, 200]

visual_style["vertex_label_angle"] = -3.14/4.0
visual_style["vertex_size"] = 8
visual_style["vertex_shape"] = 'rectangle'
visual_style["vertex_label_size"] = 10
visual_style["vertex_label_dist"] = 4

# edge defaults
visual_style["edge_color"] = 'black'
visual_style["edge_width"] = 1
visual_style["edge_arrow_size"] = 1
visual_style["edge_arrow_width"] = 1
visual_style["edge_label_size"] = 8

# In[22]:

# prefix = '/mnt/dat/work/testuser/indenter/sandbox/20191110_packmol'
prefix = '/home/jotelha/git/jlhphd'
work_prefix = '/home/jotelha/tmp/{date:s}_fw/'.format(date=yyyymmdd)
try:
    os.makedirs(work_prefix)
except:
    pass
os.chdir(work_prefix)

# the FireWorks LaunchPad
lp = LaunchPad.auto_load() #Define the server and database
# FilePad behaves analogous to LaunchPad
fp = FilePad.auto_load()

# In[010]

# from '2021-02-26-sds-on-au-111-probe-and-substrate-conversion'
probe_on_substrate_input_datasets = [
     {'concentration': 0.03,
      'shape': 'hemicylinders',
      'uri': 'file:///p/project/hfr21/hoermann4/dtool/PRODUCTION/2021-10-07-sds-on-au-111-probe-and-substrate-merge-and-approach/2021-10-07-21-45-08-080980-probeonsubst--ionminimizationequilibrationandapproach',
      'uuid': '809780c7-cf24-42b6-ab1d-96d839a9fae3',
      "x_shift": -50,
      "y_shift": 25,
     }
     {'concentration': 0.03,
      'shape': 'hemicylinders',
      "uri": "file://jwlogin04.juwels/p/project/hfr21/hoermann4/dtool/PRODUCTION/2021-10-07-sds-on-au-111-probe-and-substrate-merge-and-approach/2021-10-07-21-44-54-616918-probeonsubst--ionminimizationequilibrationandapproach",
      "uuid": "e419da6c-23ec-4d3b-bf33-0754fda8c5a2"
      "x_shift": -50,
      "y_shift": -25,
     }

]

    
# parameters

parameter_sets = [
    # {
    #     'constant_indenter_velocity': -1.0e-4, # 10 m / s
    #     'steps': 250000,
    #     'netcdf_frequency': 100,
    #     'thermo_frequency': 100,
    #     'thermo_average_frequency': 100,
    #     'restart_frequency': 100,
    # },
    {
        'constant_indenter_velocity': -1.0e-5, # 1 m / s
        'steps': 2500000,
        'netcdf_frequency': 1000,
        'thermo_frequency': 1000,
        'thermo_average_frequency': 1000,
        'restart_frequency': 1000,
    }
]

parameter_dict_list = [{**d, **p} for p in parameter_sets for d in probe_on_substrate_input_datasets]

# In[020]


from jlhpy.utilities.wf.probe_on_substrate.chain_wf_probe_on_substrate_insertion import ProbeOnSubstrateNormalApproach


project_id = '2021-10-07-sds-on-au-111-probe-and-substrate-approach'

wf_list = []

for p in parameter_dict_list:
    wfg = ProbeOnSubstrateNormalApproach(
        project_id=project_id,
        
        files_in_info={
            'data_file': {
                #'query': {'uuid': p['uuid']},
                'uri': p['uri'],
                'file_name': 'default.lammps',
                'metadata_dtool_source_key': 'system',
                'metadata_fw_dest_key': 'metadata->system',
                'metadata_fw_source_key': 'metadata->system',
            },
        },
    
        integrate_push=True,
        description="SDS on Au(111) substrate and probe trial",
        owners=[{
            'name': 'Johannes Laurin Hörmann',
            'email': 'johannes.hoermann@imtek.uni-freiburg.de',
            'username': 'fr_jh1130',
            'orcid': '0000-0001-5867-695X'
        }],
        infile_prefix=prefix,
        machine='juwels',
        mode='trial',
        system = {
            'concentration': p['concentration'],
            'shape': p['shape'],
        },
        step_specific={
            'probe_normal_approach': {
                'constant_indenter_velocity': p['constant_indenter_velocity'],
                'freeze_substrate_layer': 14.0,  # freeze that slab at the substrate's bottom
                'rigid_indenter_core_radius': 12.0,  # freeze that sphere at the ore of the indenter
                'temperature': 298.0,
                'steps': p['steps'],
                'netcdf_frequency': p['netcdf_frequency'],
                'thermo_frequency': p['thermo_frequency'],
                'thermo_average_frequency': p['thermo_average_frequency'],
                'restart_frequency': p['restart_frequency'],
                
                'ewald_accuracy': 1.0e-4,
                'coulomb_cutoff': 8.0,
                'neigh_delay': 2,
                'neigh_every': 1,
                'neigh_check': True,
                'skin_distance': 3.0,
            },
            'filter_netcdf': {
                'group': 'indenter',
            },
            'extract_forces': {
                'dimension': 2, # z-direction
            },
            'dtool_push': {
                'dtool_target': '/p/project/hfr21/hoermann4/dtool/TRIAL_DATASETS',
                'remote_dataset': None,
            }
        }
    )
    
    fp_files = wfg.push_infiles(fp)
    wf = wfg.build_wf()
    wf_list.append(wf)
