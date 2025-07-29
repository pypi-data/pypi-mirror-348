# -*- coding: utf-8 -*-
"""Probe analysis sub workflow."""

from imteksimfw.fireworks.user_objects.firetasks.cmd_tasks import CmdTask, PickledPyEnvTask
from imteksimfw.utils.serialize import serialize_module_obj

from jlhpy.utilities.wf.workflow_generator import (
    WorkflowGenerator, ChainWorkflowGenerator)
from jlhpy.utilities.wf.mixin.mixin_wf_storage import (
   DefaultPullMixin, DefaultPushMixin)

from jlhpy.utilities.analysis.forces import extract_summed_forces_from_netcdf
# def extract_summed_forces_from_netcdf(
#         force_keys=[
#             'forces',
#             'f_storeAnteSHAKEForces',
#             'f_storeAnteStatForces',
#             'f_storeUnconstrainedForces',
#             'f_storeAnteSHAKEForcesAve',
#             'f_storeAnteStatForcesAve',
#             'f_storeUnconstrainedForcesAve'],
#         forces_file_name={
#             'json': 'group_z_forces.json',
#             'txt': 'group_z_forces.txt'},
#         netcdf='default.nc',
#         dimension_of_interest=2,  # forces in z dir
#         output_formats=['json', 'txt'])


class ProbeAnalysisMain(WorkflowGenerator):
    """
    Filter group of interest from NetCDF and extract forces for that group.

    inputs:
    - metadata->step_specific->filter_netcdf->group
    - metadata->step_specific->extract_forces->dimension

    dynamic infiles:
    - joint_traj_file: default.nc
    - index_file:      default.ndx

    outfiles:
    - trajectory_file: filtered.nc
    - forces_file: default.txt
    """


    def main(self, fws_root=[]):

        fw_list = []

        # filter nectdf
        # -------------
        step_label = self.get_step_label('filter')

        files_in = {
            'joint_traj_file': 'default.nc',
            'index_file': 'default.ndx',
        }
        files_out = {
            'trajectory_file': 'filtered.nc',
        }

        fts_filter = [CmdTask(
            cmd='ncfilter',
            opt=['--debug', '--log',
                 'ncfilter.log', 'default.nc', 'filtered.nc', 'default.ndx',
                 {'key': 'metadata->step_specific->filter_netcdf->group'}],
            env='python',
            stderr_file='std.err',
            stdout_file='std.out',
            stdlog_file='std.log',
            store_stdout=True,
            store_stderr=True,
            fizzle_bad_rc=True)]

        fw_filter = self.build_fw(
            fts_filter, step_label,
            parents=fws_root,
            files_in=files_in,
            files_out=files_out,
            category=self.hpc_specs['fw_queue_category'],
            queueadapter=self.hpc_specs['single_node_job_queueadapter_defaults']
        )

        fw_list.append(fw_filter)

        # extract
        # -------
        step_label = self.get_step_label('extract')

        files_in = {
            'trajectory_file': 'default.nc',
        }
        files_out = {
            'forces_file': 'default.txt',
        }

        func_str = serialize_module_obj(extract_summed_forces_from_netcdf)

        fts_extract = [PickledPyEnvTask(
            func=func_str,
            kwargs={
                'force_keys': [
                    'forces',
                    'f_storeAnteShakeForces',
                    'f_storeAnteStatForces',
                    'f_storeAnteFreezeForces',
                    'f_storeUnconstrainedForces',
                    'f_storeForcesAve',
                    'f_storeAnteShakeForcesAve',
                    'f_storeAnteStatForcesAve',
                    'f_storeAnteFreezeForcesAve',
                    'f_storeUnconstrainedForcesAve'],
                'forces_file_name': {'txt': 'default.txt'},
                'output_formats': ['txt'],
                'netcdf': 'default.nc',
                'index_var': None,
                # see https://wiki.fysik.dtu.dk/ase/dev/_modules/ase/io/netcdftrajectory.html
                #  Name of variable containing the atom indices. Atoms are reordered
                #  by this index upon reading if this variable is present. Default
                #  value is for LAMMPS output. None switches atom indices off.
                # This is necessary as the previous filtering will likely leave atom indices
                # within the netcdf non-continuous or non-zero-indexed, which causes ASEto fail
                # when evaluating.
            },
            kwargs_inputs={
                'dimension_of_interest': 'metadata->step_specific->extract_forces->dimension',
            },
            env='imteksimpy',
            stderr_file='std.err',
            stdout_file='std.out',
            stdlog_file='std.log',
            store_stdout=True,
            store_stderr=True,
            store_stdlog=True,
            propagate=False,
        )]

        fw_extract = self.build_fw(
            fts_extract, step_label,
            parents=[fw_filter],
            files_in=files_in,
            files_out=files_out,
            category = self.hpc_specs['fw_queue_category'],
            queueadapter =self.hpc_specs['single_core_job_queueadapter_defaults']
        )

        fw_list.append(fw_extract)

        return fw_list, [fw_filter, fw_extract], [fw_filter]


class ProbeAnalysis(
        DefaultPullMixin, DefaultPushMixin,
        ProbeAnalysisMain,
        ):
    pass


class ProbeAnalysis3DMain(WorkflowGenerator):
    """
    Filter group of interest from NetCDF and extract forces for that group.

    inputs:
    - metadata->step_specific->filter_netcdf->group

    dynamic infiles:
    - joint_traj_file: default.nc
    - index_file:      default.ndx

    outfiles:
    - trajectory_file: filtered.nc
    - forces_file_x: fx.txt
    - forces_file_y: fy.txt
    - forces_file_z: fz.txt
    """

    def main(self, fws_root=[]):

        fw_list = []

        # filter nectdf
        # -------------
        step_label = self.get_step_label('filter')

        files_in = {
            'joint_traj_file': 'default.nc',
            'index_file': 'default.ndx',
        }
        files_out = {
            'trajectory_file': 'filtered.nc',
        }

        fts_filter = [CmdTask(
            cmd='ncfilter',
            opt=['--debug', '--log',
                 'ncfilter.log', 'default.nc', 'filtered.nc', 'default.ndx',
                 {'key': 'metadata->step_specific->filter_netcdf->group'}],
            env='python',
            stderr_file='std.err',
            stdout_file='std.out',
            stdlog_file='std.log',
            store_stdout=True,
            store_stderr=True,
            fizzle_bad_rc=True)]

        fw_filter = self.build_fw(
            fts_filter, step_label,
            parents=fws_root,
            files_in=files_in,
            files_out=files_out,
            category=self.hpc_specs['fw_queue_category'],
            queueadapter=self.hpc_specs['single_node_job_queueadapter_defaults']
        )

        fw_list.append(fw_filter)

        # extract
        # -------
        step_label = self.get_step_label('extract')

        files_in = {
            'trajectory_file': 'default.nc',
        }
        files_out = {
            'forces_file_x': 'fx.txt',
            'forces_file_y': 'fy.txt',
            'forces_file_z': 'fz.txt',
        }

        func_str = serialize_module_obj(extract_summed_forces_from_netcdf)

        fts_extract = [
            PickledPyEnvTask(
                func=func_str,
                kwargs={
                    'force_keys': [
                        'forces',
                        'f_storeAnteShakeForces',
                        'f_storeAnteStatForces',
                        'f_storeAnteFreezeForces',
                        'f_storeUnconstrainedForces',
                        'f_storeForcesAve',
                        'f_storeAnteShakeForcesAve',
                        'f_storeAnteStatForcesAve',
                        'f_storeAnteFreezeForcesAve',
                        'f_storeUnconstrainedForcesAve'],
                    'forces_file_name': {'txt': 'fx.txt'},
                    'output_formats': ['txt'],
                    'netcdf': 'default.nc',
                    'index_var': None,
                    'dimension_of_interest': 0,
                    # see https://wiki.fysik.dtu.dk/ase/dev/_modules/ase/io/netcdftrajectory.html
                    #  Name of variable containing the atom indices. Atoms are reordered
                    #  by this index upon reading if this variable is present. Default
                    #  value is for LAMMPS output. None switches atom indices off.
                    # This is necessary as the previous filtering will likely leave atom indices
                    # within the netcdf non-continuous or non-zero-indexed, which causes ASEto fail
                    # when evaluating.
                },
                env='imteksimpy',
                stderr_file='std_x.err',
                stdout_file='std_x.out',
                stdlog_file='std_x.log',
                store_stdout=True,
                store_stderr=True,
                store_stdlog=True,
                propagate=False,
            ),
            PickledPyEnvTask(
                func=func_str,
                kwargs={
                    'force_keys': [
                        'forces',
                        'f_storeAnteShakeForces',
                        'f_storeAnteStatForces',
                        'f_storeAnteFreezeForces',
                        'f_storeUnconstrainedForces',
                        'f_storeForcesAve',
                        'f_storeAnteShakeForcesAve',
                        'f_storeAnteStatForcesAve',
                        'f_storeAnteFreezeForcesAve',
                        'f_storeUnconstrainedForcesAve'],
                    'forces_file_name': {'txt': 'fy.txt'},
                    'output_formats': ['txt'],
                    'netcdf': 'default.nc',
                    'index_var': None,
                    'dimension_of_interest': 1,
                    # see https://wiki.fysik.dtu.dk/ase/dev/_modules/ase/io/netcdftrajectory.html
                    #  Name of variable containing the atom indices. Atoms are reordered
                    #  by this index upon reading if this variable is present. Default
                    #  value is for LAMMPS output. None switches atom indices off.
                    # This is necessary as the previous filtering will likely leave atom indices
                    # within the netcdf non-continuous or non-zero-indexed, which causes ASEto fail
                    # when evaluating.
                },
                env='imteksimpy',
                stderr_file='std_y.err',
                stdout_file='std_y.out',
                stdlog_file='std_y.log',
                store_stdout=True,
                store_stderr=True,
                store_stdlog=True,
                propagate=False,
            ),
            PickledPyEnvTask(
                func=func_str,
                kwargs={
                    'force_keys': [
                        'forces',
                        'f_storeAnteShakeForces',
                        'f_storeAnteStatForces',
                        'f_storeAnteFreezeForces',
                        'f_storeUnconstrainedForces',
                        'f_storeForcesAve',
                        'f_storeAnteShakeForcesAve',
                        'f_storeAnteStatForcesAve',
                        'f_storeAnteFreezeForcesAve',
                        'f_storeUnconstrainedForcesAve'],
                    'forces_file_name': {'txt': 'fz.txt'},
                    'output_formats': ['txt'],
                    'netcdf': 'default.nc',
                    'index_var': None,
                    'dimension_of_interest': 2,
                    # see https://wiki.fysik.dtu.dk/ase/dev/_modules/ase/io/netcdftrajectory.html
                    #  Name of variable containing the atom indices. Atoms are reordered
                    #  by this index upon reading if this variable is present. Default
                    #  value is for LAMMPS output. None switches atom indices off.
                    # This is necessary as the previous filtering will likely leave atom indices
                    # within the netcdf non-continuous or non-zero-indexed, which causes ASEto fail
                    # when evaluating.
                },
                env='imteksimpy',
                stderr_file='std_z.err',
                stdout_file='std_z.out',
                stdlog_file='std_z.log',
                store_stdout=True,
                store_stderr=True,
                store_stdlog=True,
                propagate=False,
            )
        ]

        fw_extract = self.build_fw(
            fts_extract, step_label,
            parents=[fw_filter],
            files_in=files_in,
            files_out=files_out,
            category = self.hpc_specs['fw_queue_category'],
            queueadapter =self.hpc_specs['single_core_job_queueadapter_defaults']
        )

        fw_list.append(fw_extract)

        return fw_list, [fw_filter, fw_extract], [fw_filter]


class ProbeAnalysis3D(
        DefaultPullMixin, DefaultPushMixin,
        ProbeAnalysis3DMain,
        ):
    pass