import os.path
# python package-internal paths and file names are to be defined here

# TODO: looks through modules and replace hard-coded surfactant-specific names

# GROMACS-related
GMX_MDP_SUBDIR = os.path.join('gmx_input', 'mdp')
GMX_EM_MDP = 'em.mdp'
GMX_PULL_MDP_TEMPLATE = 'pull.mdp.template'
GMX_EM_SOLVATED_MDP = 'em_solvated.mdp'
GMX_NVT_MDP = 'nvt.mdp'
GMX_NPT_MDP = 'npt.mdp'
GMX_NPT_Z_ONLY_MDP = 'npt_z_only.mdp'  # barostatting only in z direction
GMX_RELAX_MDP = 'relax.mdp'
GMX_RELAX_Z_ONLY_MDP = 'relax_z_only.mdp'

GMX_TOP_SUBDIR = os.path.join('gmx_input', 'top')
GMX_TOP_TEMPLATE = 'sys.top.template'
GMX_PULL_TOP_TEMPLATE = 'sys.top.template'

# LAMMPS-related
LMP_INPUT_SUBDIR = 'lmp_input'
LMP_INPUT_TEMPLATE_SUBDIR = os.path.join(LMP_INPUT_SUBDIR, 'template')
LMP_CONVERT_XYZ_INPUT_TEMPLATE = 'lmp_convert_xyz.input.template'
LMP_INPUT_TEMPLATE = 'lmp.input.template'
LMP_HEADER_INPUT_TEMPLATE = 'lmp_header.input.template'
LMP_MINIMIZATION_INPUT_TEMPLATE = 'lmp_minimization.input.template'
LMP_PRODUCTION_INPUT_TEMPLATE = 'lmp_production.input.template'
LMP_SPLIT_DATAFILE_INPUT_TEMPLATE = 'lmp.input.template'


LMP_FF_SUBDIR = 'ff'
LMP_MASS_INPUT = 'SDS_in_H2O_on_AU_masses.input'
LMP_COEFF_HYBRID_NONEWALD_NONBONDED_INPUT_PATTERN = '{name:s}_in_H2O_on_AU_coeff_hybrid_lj_charmmfsw_coul_charmmfsh_nonbonded.input'
LMP_COEFF_HYBRID_INPUT_PATTERN = '{name:s}_in_H2O_on_AU_coeff_hybrid_lj_charmmfsw_coul_long.input'

# LMP_COEFF_INPUT = 'SDS_in_H2O_on_AU_masses.input'
LMP_EAM_ALLOY = 'Au-Grochola-JCP05-units-real.eam.alloy'

# CHARMM-related
CHARMM_FF_SUBDIR = 'ff'
CHARMM36_PRM = 'par_all36_lipid_extended_stripped.prm'
CHARMM36_RTF = 'top_all36_lipid_extended_stripped.rtf'

PDB_SUBDIR     = 'pdb'
SURFACTANT_PDB_PATTERN = '1_{name:s}.pdb'
COUNTERION_PDB_PATTERN = '1_{name:s}.pdb'

DAT_SUBDIR      = 'dat'
INDENTER_SUBDIR = os.path.join(DAT_SUBDIR, 'indenter')
INDENTER_PDB    = 'AU_111_r_25.pdb'

PACKMOL_SUBDIR  = 'packmol'
PACKMOL_SPHERES_TEMPLATE = 'sphere.inp.template'
PACKMOL_FLAT_TEMPLATE = 'flat.inp.template'

VMD_SUBDIR  = 'vmd'
VMD_MERGE_TEMPLATE = 'merge.tcl.template'
VMD_PSFGEN_TEMPLATE = 'psfgen.tcl.template'

VMD_JLHVMD = 'jlhvmd.tcl'
VMD_WRAP_JOIN_TEMPLATE ='wrap-join.tcl.template'

# visualization-related

PML_SUBDIR = 'pymol'
PML_MOVIE_TEMPLATE = 'movie.pml.template'
PML_VIEW_TEMPLATE = 'view.pml.template'  # similar to PML_MOVIE_TEMPLATE, but only setting up the view, not rendering movie

BASH_SCRIPT_SUBDIR = 'bash'
BASH_RENUMBER_PNG = 'renumber_png.sh'
BASH_GMX2PDB_TEMPLATE = 'gmx2pdb.sh.template'
