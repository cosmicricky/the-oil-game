from facility import Facility
from policies import naive_policy

class Simulation:
    """
    Runs the simulation experiment and provides reporting functions.
    """
    def __init__(self):
        self.depot = Facility(
            name="Fuel Depot",
            initial_inventory=20.0,
            delay=2
        )
        self.base_price = 3.00 # dollars per gallon
        self.target_inventory = 20.0 # desired inventory level
        self.alpha = 0.05 # backlog sensitivity
        self.beta = 0.02 # inventory shortfall sensitivity
        self.history = []
    

    def run(self, duration: int = 52) -> None:
        """
        Run the simulation for a given number of time steps.
        """
        self.history = [] # reset history

        # record initial conditions
        initial_order = naive_policy(self.depot.inventory, self.target_inventory)
        demand = 5.0 # constant demand for initial step
        self.history.append({
            "timestep": 0,
            "demand": demand,
            "inventory": self.depot.inventory,
            "backlog": self.depot.backlog,
            "order": initial_order,
            "price": self.compute_price(0)
        })

        for t in range(1, duration + 1):
            # demand = float(5 if t < 10 else 10) # demand spikes after week 10

            order = naive_policy(self.depot.inventory, self.target_inventory)

            result = self.depot.step(demand, order)
            price = self.compute_price(t)

            # record history
            self.history.append({
                "timestep": t,
                "demand": demand,
                "inventory": result["inventory"],
                "backlog": result["backlog"],
                "order": order,
                "price": price
            })

    
    def crude_price(self, t: int) -> float:
        # simple shock scenario
        if t < 20:
            return 2.0
        elif t < 35:
            return 2.5
        else:
            return 2.1


    def compute_price(self, t: int) -> float:
        """
        Compute the price based on inventory and backlog.

        Price increases when:
        - baclklog grows (unmet demand)
        - inventory falls below target level (scarcity)
        """
        # crude = self.crude_price(t)
        crude = 2.0 # assume constant crude price for now at $2/gal
        inventory_shortfall = max(0.0, self.target_inventory - self.depot.inventory)
        distribution = (
            self.base_price +
            self.alpha * self.depot.backlog +
            self.beta * inventory_shortfall
        )
        return crude + distribution