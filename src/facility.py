class Facility:
    """
    Represents a single supply-chain node such as a refinery, fuel depot, or a gas station.

    A facility maintains:
    - inventory: product available to ship
    - backlog: unmet demand
    - pipeline: orders placed but still in transit
    """
    def __init__(self, name: str, initial_inventory: int, delay: int):
        """
        Create a new facility.
        Args:
            name (str): The name of the facility.
            initial_inventory (int): Product available at start of simulation.
            delay (int): Number of time steps between placing an order and receiving it.
        """
        self.name = name
        self.inventory = initial_inventory
        self.backlog = 0 # if customers request more than inventory, excess demand is stored here
        self.pipeline = [0] * delay # queue of orders in transit