import matplotlib.pyplot as plt

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
        for t in range(duration):
            demand = float(4 if t < 10 else 8) # demand spikes after week 10
            order = naive_policy(self.depot.inventory, self.target_inventory)
            result = self.depot.step(demand, order)

            price = self.compute_price(t)

            self.history.append({
                "timestep": t,
                "demand": demand,
                "inventory": result["inventory"],
                "backlog": result["backlog"],
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


    def plot(self):
        """
        Plot results and visualization.
        """
        t = [h["timestep"] for h in self.history]
        demand = [h["demand"] for h in self.history]
        inventory = [h["inventory"] for h in self.history]
        backlog = [h["backlog"] for h in self.history]
        price = [h["price"] for h in self.history]

        fig, ax1 = plt.subplots(figsize=(10, 5))

        # system state
        ax1.plot(t, inventory, label="Inventory")
        ax1.plot(t, backlog, label="Backlog")
        ax1.plot(t, demand, label="Demand")

        ax1.set_xlabel("Week")
        ax1.set_ylabel("Units")
        ax1.legend(loc="upper left")

        # price (secondary axis)
        ax2 = ax1.twinx()
        ax2.plot(t, price, label="Fuel Price", color="red")
        ax2.set_ylabel("Price ($/gal)")

        plt.title("Oil Game: Simulation Results")
        plt.show()