class Facility:
    """
    Represents a single supply-chain node such as a refinery, fuel depot, or a gas station.

    A facility maintains:
    - inventory: product available to ship
    - backlog: unmet demand
    - pipeline: orders placed but still in transit
    """
    def __init__(self, name: str, initial: float, delay: int):
        """
        Create a new facility.

        Args:
            name (str): The name of the facility.
            initial (float): Initial inventory level.
            target (float): Target inventory level.
            delay (int): Number of time steps between placing an order
                and receiving it.
        """
        self.name = name
        self.inventory = initial
        self.backlog = 0.0

        # Store delay so step() can check whether orders arrive immediately.
        self.delay = delay

        # Pipeline of shipments in transit.
        # If delay = 0, this becomes an empty list, which is fine because
        # step() handles that case separately.
        self.pipeline = [0.0] * delay


    def step(self, demand: float, order: float) -> dict:
        """
        Advance the simulation by one time step.
        """
        # 1. Receive shipments from pipeline
        if self.delay == 0:
            # NOTE: orders arrive immediately (no transport delay)
            incoming = order
        else:
            # NOTE: FIFO fixed transport delay
            incoming = float(self.pipeline.pop(0))
        
        # update inventory
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

