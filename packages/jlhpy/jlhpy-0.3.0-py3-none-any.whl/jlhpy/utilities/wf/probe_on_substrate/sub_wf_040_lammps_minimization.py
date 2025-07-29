# -*- coding: utf-8 -*-
"""Probe on substrate minimization sub workflow."""

import datetime
import glob
import os
import pymongo
import warnings

from fireworks.user_objects.firetasks.filepad_tasks import GetFilesByQueryTask
from fireworks.user_objects.firetasks.templatewriter_task import TemplateWriterTask
from imteksimfw.fireworks.user_objects.firetasks.cmd_tasks import CmdTask

from jlhpy.utilities.wf.workflow_generator import (
    WorkflowGenerator, ProcessAnalyzeAndVisualize)
from jlhpy.utilities.wf.mixin.mixin_wf_storage import (
   DefaultPullMixin, DefaultPushMixin)
from jlhpy.utilities.wf.building_blocks.sub_wf_lammps_analysis import LAMMPSTrajectoryAnalysis
import jlhpy.utilities.wf.file_config as file_config
import jlhpy.utilities.wf.phys_config as phys_config


class LAMMPSMinimizationMain(WorkflowGenerator):
    """
    Fixed box minimization with LAMMPS.

    inputs:
    - metadata->step_specific->minimization->fixed_box->ftol
    - metadata->step_specific->minimization->fixed_box->maxiter
    - metadata->step_specific->minimization->fixed_box->maxeval

    - metadata->system->substrate->element
    - metadata->system->substrate->lmp->type

    - metadata->step_specific->lmp->ewald_accuracy
    - metadata->step_specific->lmp->coulomb_cutoff
    - metadata->step_specific->lmp->neigh_delay
    - metadata->step_specific->lmp->neigh_every
    - metadata->step_specific->lmp->neigh_check
    - metadata->step_specific->lmp->skin_distance

    - metadata->step_specific->minimization->ftol
    - metadata->step_specific->minimization->maxiter
    - metadata->step_specific->minimization->maxeval

    dynamic infiles:
        only queried in pull stub, otherwise expected through data flow

    - data_file:       default.lammps

    static infiles:
        always queried within main

    - input_template: lmp.input.template
    - mass_file:  mass.input
    - coeff_file: coeff.input
    - eam_file:   default.eam.alloy

    outfiles:
    - coeff_file:      coeff.input  # untouched
    - data_file:       default.lammps
    - eam_file:        default.eam.alloy  # untouched
    - index_file:      groups.ndx
    - input_file:      default.input  # untouched
    - log_file:        log.lammps
    - mass_file:       mass.input  # untouched
    - trajectory_file: default.nc
    """
    def push_infiles(self, fp):

        # static infiles for main
        # -----------------------
        step_label = self.get_step_label('push_infiles')

        # try to get surfactant pdb file from kwargs
        try:
            surfactant = self.kwargs["system"]["surfactant"]["name"]
        except:
            surfactant = phys_config.DEFAULT_SURFACTANT
            warnings.warn("No surfactant specified, falling back to {:s}.".format(surfactant))

        lmp_coeff_input = file_config.LMP_COEFF_HYBRID_INPUT_PATTERN.format(name=surfactant)

        glob_patterns = [
            os.path.join(
                self.infile_prefix,
                file_config.LMP_INPUT_TEMPLATE_SUBDIR,
                file_config.LMP_INPUT_TEMPLATE),
            os.path.join(
                self.infile_prefix,
                file_config.LMP_FF_SUBDIR,
                lmp_coeff_input),
            os.path.join(
                self.infile_prefix,
                file_config.LMP_FF_SUBDIR,
                file_config.LMP_MASS_INPUT),
            os.path.join(
                self.infile_prefix,
                file_config.LMP_FF_SUBDIR,
                file_config.LMP_EAM_ALLOY)
        ]

        infiles = sorted([
            file for pattern in glob_patterns for file in glob.glob(pattern)])

        files = {os.path.basename(f): f for f in infiles}

        # metadata common to all these files
        metadata = {
            'project': self.project_id,
            'type': 'input',
            'step': step_label,
        }

        fp_files = []

        # insert these input files into data base
        for name, file_path in files.items():
            identifier = '/'.join((self.project_id, name))
            metadata['name'] = name
            fp_files.append(
                fp.add_file(
                    file_path,
                    identifier=identifier,
                    metadata=metadata))

        return fp_files

    def main(self, fws_root=[]):
        # try to get surfactant pdb file from kwargs
        try:
            surfactant = self.kwargs["system"]["surfactant"]["name"]
        except:
            surfactant = phys_config.DEFAULT_SURFACTANT
            warnings.warn("No surfactant specified, falling back to {:s}.".format(surfactant))

        lmp_coeff_input = file_config.LMP_COEFF_HYBRID_INPUT_PATTERN.format(name=surfactant)

        fw_list = []

        # query input files
        # -----------------
        step_label = self.get_step_label('input_files_pull')

        files_in = {}
        files_out = {
            'input_template': 'lmp.input.template',
            'mass_file':      'mass.input',
            'coeff_file':     'coeff.input',
            'eam_file':       'default.eam.alloy'
        }

        fts_pull = [
            GetFilesByQueryTask(
                query={
                    'metadata->project': self.project_id,
                    'metadata->name':    file_config.LMP_INPUT_TEMPLATE,
                },
                sort_key='metadata.datetime',
                sort_direction=pymongo.DESCENDING,
                limit=1,
                new_file_names=['lmp.input.template']),
            GetFilesByQueryTask(
                query={
                    'metadata->project': self.project_id,
                    'metadata->name':    lmp_coeff_input,
                },
                sort_key='metadata.datetime',
                sort_direction=pymongo.DESCENDING,
                limit=1,
                new_file_names=['coeff.input']),
            GetFilesByQueryTask(
                query={
                    'metadata->project': self.project_id,
                    'metadata->name':    file_config.LMP_MASS_INPUT,
                },
                sort_key='metadata.datetime',
                sort_direction=pymongo.DESCENDING,
                limit=1,
                new_file_names=['mass.input']),
            GetFilesByQueryTask(
                query={
                    'metadata->project': self.project_id,
                    'metadata->name':    file_config.LMP_EAM_ALLOY,
                },
                sort_key='metadata.datetime',
                sort_direction=pymongo.DESCENDING,
                limit=1,
                new_file_names=['default.eam.alloy']),
        ]

        fw_pull = self.build_fw(
            fts_pull, step_label,
            files_in=files_in,
            files_out=files_out,
            category=self.hpc_specs['fw_noqueue_category'])

        fw_list.append(fw_pull)

        # fill input file template
        # -------------------
        step_label = self.get_step_label('fill_template')

        files_in = {
            'input_template': 'default.input.template',
        }
        files_out = {
            'input_file': 'default.input',
        }

        # Jinja2 context:
        static_template_context = {
            'mode':                     'minimization',
            'coeff_infile':             'coeff.input',
            'data_file':                'datafile.lammps',
            'freeze_substrate':         True,
            'has_indenter':             True,
            'mpiio':                    True,
            'relax_box':                False,
            'rigid_h_bonds':            False,
            'robust_minimization':      False,
            'store_forces':             False,
            'use_eam':                  True,
            'use_ewald':                True,
            'write_coeff_to_datafile':  False,
        }

        dynamic_template_context = {
            'minimization_ftol': 'metadata->step_specific->minimization->ftol',
            'minimization_maxiter': 'metadata->step_specific->minimization->maxiter',
            'minimization_maxeval': 'metadata->step_specific->minimization->maxeval',

            'ewald_accuracy': 'metadata->step_specific->minimization->ewald_accuracy',
            'coulomb_cutoff': 'metadata->step_specific->minimization->coulomb_cutoff',
            'neigh_delay': 'metadata->step_specific->minimization->neigh_delay',
            'neigh_every': 'metadata->step_specific->minimization->neigh_every',
            'neigh_check': 'metadata->step_specific->minimization->neigh_check',
            'skin_distance': 'metadata->step_specific->minimization->skin_distance',

            'substrate_element': 'metadata->system->substrate->element',
            'substrate_type': 'metadata->system->substrate->lmp->type',
        }

        fts_template = [TemplateWriterTask({
            'context_inputs': dynamic_template_context,
            'context': static_template_context,
            'template_file': 'default.input.template',
            'template_dir': '.',
            'output_file': 'default.input'})]

        fw_template = self.build_fw(
            fts_template, step_label,
            parents=[fw_pull, *fws_root],
            files_in=files_in,
            files_out=files_out,
            category=self.hpc_specs['fw_noqueue_category'])

        fw_list.append(fw_template)

        # LAMMPS run
        # ----------
        step_label = self.get_step_label('lmp_run')

        files_in = {
            'data_file':  'datafile.lammps',
            'input_file': 'default.input',
            'mass_file':  'mass.input',
            'coeff_file': 'coeff.input',
            'eam_file':   'default.eam.alloy',
        }
        files_out = {
            'data_file':       'default.lammps',
            'trajectory_file': 'default.nc',
            'index_file':      'groups.ndx',  # generated
            'conserved_input_file':      'default.input',  # untouched
            'mass_file':       'mass.input',  # untouched
            'log_file':        'log.lammps',
            'coeff_file':      'coeff.input',  # untouched
            'eam_file':        'default.eam.alloy',  # untouched
        }
        fts_lmp_run = [CmdTask(
            cmd='lmp',
            opt=['-in', 'default.input'],
            env='python',
            stderr_file='std.err',
            stdout_file='std.out',
            stdlog_file='std.log',
            store_stdout=True,
            store_stderr=True,
            fizzle_bad_rc=True)]

        fw_lmp_run = self.build_fw(
            fts_lmp_run, step_label,
            parents=[fw_template, fw_pull, *fws_root],
            files_in=files_in,
            files_out=files_out,
            category=self.hpc_specs['fw_queue_category'],
            queueadapter=self.hpc_specs['single_node_job_queueadapter_defaults']
        )

        fw_list.append(fw_lmp_run)

        return fw_list, [fw_lmp_run], [fw_lmp_run, fw_template]


class LAMMPSMinimization(
        DefaultPullMixin, DefaultPushMixin,
        ProcessAnalyzeAndVisualize,
        ):
    def __init__(self, *args, **kwargs):
        super().__init__(
            main_sub_wf=LAMMPSMinimizationMain,
            analysis_sub_wf=LAMMPSTrajectoryAnalysis,
            *args, **kwargs)