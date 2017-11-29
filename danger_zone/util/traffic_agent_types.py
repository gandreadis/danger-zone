from danger_zone.models.bicycle import Bicycle
from danger_zone.models.car import Car
from danger_zone.models.pedestrian import Pedestrian

TRAFFIC_AGENT_TYPES = {
    "pedestrian": Pedestrian,
    "bicycle": Bicycle,
    "car": Car,
}
