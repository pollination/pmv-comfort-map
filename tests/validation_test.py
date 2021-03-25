from pollination.pmv_comfort_map.entry import PmvComfortMapEntryPoint
from queenbee.recipe.dag import DAG


def test_pmv_comfort_map():
    recipe = PmvComfortMapEntryPoint().queenbee
    assert recipe.name == 'pmv-comfort-map-entry-point'
    assert isinstance(recipe, DAG)
