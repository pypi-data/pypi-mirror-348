"""A list of transforms."""

from .transform import Transform
from .transform_log import log_transform
from .transform_velocity import velocity_transform

TRANSFORMS = {
    str(Transform.NONE): lambda x: x,
    str(Transform.VELOCITY): velocity_transform,
    str(Transform.LOG): log_transform,
}
