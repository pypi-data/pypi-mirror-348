import numpy as np
import math
from typing import Tuple
from colav_unsafe_set.objects import (
    Agent,
    DynamicObstacle
)

def quaternion_to_yaw(q):
    """Convert quaternion (w, x, y, z) to yaw (heading) angle in radians."""
    w, x, y, z = q
    return np.arctan2(2 * (w * z + x * y), 1 - 2 * (y ** 2 + z ** 2))

def normalize_angle(angle):
    """Normalize angle to the range [-π, π]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def calc_cpa(
    agent_object: Agent, target_object: DynamicObstacle
) -> Tuple[float, float]:
    """
    Calculate the Distance at Closest Point of Approach (DCPA) and
    Time to Closest Point of Approach (TCPA) between two dynamic objects.

    The calculation is performed only if TCPA > 0; otherwise,
    DCPA and TCPA are set to NaN (or TCPA to infinity in the case of identical positions).

    Parameters:
        agent_object (DynamicObject): The dynamic object representing the agent.
        target_object (DynamicObject): The dynamic object representing the target.

    Returns:
        Tuple[float, float]: A tuple containing (DCPA, TCPA)
    """

    # Extract 2D positions from agent and target objects.
    p1 = np.array([
        agent_object.position[0],
        agent_object.position[1]
    ])
    p2 = np.array([
        target_object.position[0],
        target_object.position[1]
    ])

    # Calculate heading angles (theta) using quaternion components.
    theta1 = normalize_angle(quaternion_to_yaw(agent_object.orientation))
    theta2 = normalize_angle(quaternion_to_yaw(target_object.orientation))


    # Compute the velocity vectors based on speed and heading angle.
    v1 = np.array([
        agent_object.velocity * np.cos(theta1),
        agent_object.velocity * np.sin(theta1),
    ])
    v2 = np.array([
        target_object.velocity * np.cos(theta2),
        target_object.velocity * np.sin(theta2),
    ])

    # Calculate the relative position and velocity.
    p_rel = p1 - p2
    v_rel = v1 - v2
    v_rel_norm_sq = np.dot(v_rel, v_rel)

    # Handle near-parallel or nearly stationary relative motion.
    if v_rel_norm_sq < 1e-6:
        # When objects are nearly stationary relative to each other.
        if np.allclose(p_rel, [0, 0]):
            # Identical positions: DCPA is undefined, TCPA is infinite.
            dcpa = float('nan')
            tcpa = float('inf')
        else:
            # Constant separation: TCPA is the time required to cover the gap at the agent's speed.
            distance = np.linalg.norm(p_rel)
            speed = np.linalg.norm(v1)
            tcpa = distance / speed if speed > 0 else float('inf')
            dcpa = distance
    else:
        # Standard CPA calculations.
        tcpa = -np.dot(p_rel, v_rel) / v_rel_norm_sq
        
        # Only consider future encounters where TCPA > 0.
        if tcpa > 0:
            closest_position = p_rel + tcpa * v_rel
            dcpa = np.linalg.norm(closest_position)
        else:
            dcpa = float('nan')
            tcpa = float('nan')

    return dcpa, tcpa
