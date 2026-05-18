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
        self.inventory = float(initial_inventory)
        self.backlog = 0.0 # if customers request more than inventory, excess demand is stored here
        self.pipeline = [0.0] * delay # queue of orders in transit


    def step(self, demand: float, order: float) -> dict:
        """
        Advance the simulation by one time step.
        """
        # 1. Receive shipments from pipeline (FIFO)
        incoming = float(self.pipeline.pop(0)) # NOTE: fixed transport delay (like conveyor belt)
        self.inventory += incoming

        # 2. Add new demand to backlog
        total_demand = demand + self.backlog # NOTE: demand accumulates!

        # 3. Fulfill demand using available inventory
        shipped = min(self.inventory, total_demand) # NOTE: can only ship what we have
        self.inventory -= shipped

        # 4. Update backlog with unmet demand
        self.backlog = total_demand - shipped

        # 5. Place a new order upstream
        self.pipeline.append(order)

        return {
            "inventory": self.inventory,
            "backlog": self.backlog,
            "order": order
        }

