def naive_policy(inventory: float, target: float = 20) -> float:
    """
    A simple policy that orders enough to reach the target inventory level.
    """
    order = max(0.0, target - inventory)
    return order