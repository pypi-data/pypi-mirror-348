# In[20]:
import os, os.path
import datetime
# FireWorks functionality
from fireworks.utilities.dagflow import DAGFlow, plot_wf
from fireworks import Firework, LaunchPad, Workflow
from fireworks.utilities.filepad import FilePad


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

# In[25]:

parameter_values = [ {'c': 0, 'n': 0, 'm': 0, 's': 'monolayer' } ]

# In[20]:

# SDS on Au(111)
from jlhpy.utilities.wf.flat_packing.chain_wf_flat_substrate_passivation import SubstratePassivation
from jlhpy.utilities.wf.phys_config import TOLERANCE, SURFACTANTS

project_id = '2020-10-13-none-on-au-111-substrate-preparation-trial'

# remove all project files from filepad:
#     fp.delete_file_by_query({'metadata.project': project_id})

# In[25]
wfg = SubstratePassivation(
    project_id=project_id,

    files_in_info={ 
        'data_file': {  # smb://jh1130/b5774404-e151-4398-bda9-36eb523a0ae7
            #'query': {'uuid': 'b5774404-e151-4398-bda9-36eb523a0ae7'},
            'uri': 'smb://jh1130/b5774404-e151-4398-bda9-36eb523a0ae7',
            'file_name': 'default.lammps',
            'metadata_dtool_source_key': 'system->substrate',
            'metadata_fw_dest_key': 'metadata->system->substrate',
            'metadata_fw_source_key': 'metadata->system->substrate',
        },
    },
    integrate_push=True,
    description="Bare Au(111) substrate preparation trial",
    owners=[{
        'name': 'Johannes Laurin Hörmann',
        'email': 'johannes.hoermann@imtek.uni-freiburg.de',
        'username': 'fr_jh1130',
        'orcid': '0000-0001-5867-695X'
    }],
    infile_prefix=prefix,
    machine='juwels',
    mode='trial',
    parameter_label_key_dict={
        'c': 'system->surfactant->surface_concentration',
        'n': 'system->surfactant->nmolecules',
        'm': 'system->counterion->nmolecules',
        's': 'system->surfactant->aggregates->shape'},
    parameter_values=parameter_values,
    system = {
        'counterion': {
            'name': 'NA',
            'resname': 'NA',
            'nmolecules': None,
            'reference_atom': {
                'name': 'NA',
            },
        },
        'surfactant': {
            'name': 'SDS',
            'resname': 'SDS',
            'nmolecules': None,
            'connector_atom': {
                'index': 2,
            },
            'head_atom': {
                'name': 'S',
                'index': 1,
            },
            'tail_atom': {
                'name': 'C12',
                'index': 39,
            },
            'aggregates': {
                'shape': None,
            },
            'surface_concentration': None,

        },
        'substrate': {
            'name': 'AUM',
            'resname': 'AUM',
            'reference_atom': {
                'name': 'AU',
            },
        },
        'solvent': {
            'name': 'H2O',
            'resname': 'SOL',
            'reference_atom': {
                'name': 'OW',
            },
            'height': 180.0,
        }
    },
    step_specific={
        'conversion': {
            'lmp_type_to_element_mapping': {
                '11': 'Au',
            },
            'element_to_pdb_atom_name_mapping': {
                'Au': 'AU',
            },
            'element_to_pdb_residue_name_mapping': {
                'Au': 'AUM',
            },
        },
        'packing' : {
            'surfactant_substrate': {
                'tolerance': 1.0  # intead of 1.5 or 2
            },
        },
        'dtool_push': {
            'dtool_target': '/p/project/hfr21/hoermann4/dtool/TRIAL_DATASETS',
            'remote_dataset': None,
        }
    },
)

fp_files = wfg.push_infiles(fp)

wf = wfg.build_wf()
