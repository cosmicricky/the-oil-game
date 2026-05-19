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


    def plot(self):
        """
        Plot results and visualization.
        """
        # extract history
        t = [h["timestep"] for h in self.history]
        demand = [h["demand"] for h in self.history]
        inventory = [h["inventory"] for h in self.history]
        backlog = [h["backlog"] for h in self.history]
        order = [h["order"] for h in self.history]
        price = [h["price"] for h in self.history]

        fig, ax1 = plt.subplots(figsize=(10, 5))
        
        # inventory
        ax1.fill_between(t, inventory, label="Inventory", alpha=0.25)
        ax1.plot(t, inventory)

        # demand
        ax1.plot(t, demand, label="Demand", color="orange", linestyle="--")

        # backlog
        # ax1.plot(t, backlog, label="Backlog", color="purple")

        # orders
        ax1.plot(t, order, label="Orders")

        # primary axis
        ax1.set_xlabel("Week")
        ax1.set_ylabel("Units")
        ax1.grid(True, alpha=0.3)

        # price (secondary axis)
        ax2 = ax1.twinx()
        ax2.plot(t, price, label="Fuel Price", color="red")
        ax2.set_ylabel("Price ($/gal)")
        
        # Get legend entries from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        # combine legends
        legend = ax1.legend(
            lines1 + lines2, 
            labels1 + labels2, 
            loc="upper left",
            frameon=True, 
            facecolor="white", 
            framealpha=1.0
        )
        legend.set_zorder(2)

        plt.title("Oil Game: Simulation Results")
        fig.tight_layout()
        plt.show()