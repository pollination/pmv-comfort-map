from pollination_dsl.dag import Inputs, DAG, task
from dataclasses import dataclass
from typing import Dict, List

from pollination.path.read import ReadJSONList

from ._radcontrib import RadianceContribEntryPoint
from ._dynbehavior import DynamicBehaviorEntryPoint


@dataclass
class DynamicContributionEntryPoint(DAG):
    """Entry point for computing the contributions from dynamic windows."""

    # inputs
    radiance_parameters = Inputs.str(
        description='Radiance parameters for ray tracing.',
        default='-ab 2 -ad 5000 -lw 2e-05',
    )

    result_sql = Inputs.file(
        description='A SQLite file that was generated by EnergyPlus and contains '
        'window transmittance results.',
        extensions=['sql', 'db', 'sqlite']
    )

    octree_file_spec = Inputs.file(
        description='A Radiance octree file with a specular version of the '
        'window group.', extensions=['oct']
    )

    octree_file_diff = Inputs.file(
        description='A Radiance octree file with a diffuse version of the window group.',
        extensions=['oct']
    )

    octree_file_with_suns = Inputs.file(
        description='A Radiance octree file with sun modifiers.',
        extensions=['oct']
    )

    group_name = Inputs.str(
        description='Name for the dynamic aperture group being simulated.'
    )

    sensor_grid_folder = Inputs.folder(
        description='A folder containing all of the split sensor grids in the model.'
    )

    sensor_grids = Inputs.file(
        description='A JSON file with information about sensor grids to loop over.'
    )

    sky_dome = Inputs.file(
        description='Path to sky dome file.'
    )

    sky_matrix = Inputs.file(
        description='Path to total sky matrix file.'
    )

    sky_matrix_direct = Inputs.file(
        description='Path to direct skymtx file (gendaymtx -d).'
    )

    sun_modifiers = Inputs.file(
        description='A file with sun modifiers.'
    )

    sun_up_hours = Inputs.file(
        description='A sun-up-hours.txt file output by Radiance and aligns with the '
        'input irradiance files.'
    )

    @task(template=ReadJSONList)
    def read_grids(self, src=sensor_grids) -> List[Dict]:
        return [
            {
                'from': ReadJSONList()._outputs.data,
                'description': 'Sensor grids information.'
            }
        ]

    @task(
        template=RadianceContribEntryPoint,
        needs=[read_grids],
        loop=read_grids._outputs.data,
        sub_folder='shortwave',
        sub_paths={
            'sensor_grid': '{{item.full_id}}.pts',
            'ref_sensor_grid': '{{item.full_id}}_ref.pts',
        }
    )
    def run_radiance_window_contrib(
        self,
        radiance_parameters=radiance_parameters,
        octree_file_spec=octree_file_spec,
        octree_file_diff=octree_file_diff,
        octree_file_with_suns=octree_file_with_suns,
        group_name=group_name,
        grid_name='{{item.full_id}}',
        sensor_grid=sensor_grid_folder,
        ref_sensor_grid=sensor_grid_folder,
        sensor_count='{{item.count}}',
        sky_dome=sky_dome,
        sky_matrix=sky_matrix,
        sky_matrix_direct=sky_matrix,
        sun_modifiers=sun_modifiers
    ) -> List[Dict]:
        pass

    @task(
        template=DynamicBehaviorEntryPoint,
        needs=[read_grids, run_radiance_window_contrib],
        loop=read_grids._outputs.data,
        sub_folder='shortwave',
        sub_paths={
            'direct_specular': '{{item.full_id}}.ill',
            'indirect_specular': '{{item.full_id}}.ill',
            'ref_specular': '{{item.full_id}}.ill',
            'indirect_diffuse': '{{item.full_id}}.ill',
            'ref_diffuse': '{{item.full_id}}.ill'
        }
    )
    def run_dynamic_behavior_contrib(
        self,
        result_sql=result_sql,
        direct_specular='shortwave/dynamic/initial/{{group_name}}/direct_spec',
        indirect_specular='shortwave/dynamic/initial/{{group_name}}/indirect_spec',
        ref_specular='shortwave/dynamic/initial/{{group_name}}/reflected_spec',
        indirect_diffuse='shortwave/dynamic/initial/{{group_name}}/total_diff',
        ref_diffuse='shortwave/dynamic/initial/{{group_name}}/reflected_diff',
        sun_up_hours=sun_up_hours,
        aperture_id=group_name,
        grid_name='{{item.full_id}}'
    ) -> List[Dict]:
        pass
