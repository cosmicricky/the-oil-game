from facility import Facility

class Simulation:
    """
    Runs the simulation experiment and provides reporting functions.
    """
    def __init__(self):
        self.depot = Facility(
            name="Fuel Depot",
            initial_inventory=20,
            delay=2
        )
        self.history = []
    

    def run(self, duration=52):
        """
        Run the simulation for a given number of time steps.
        """
        for timestep in range(duration):
            demand = 4 if timestep < 10 else 8 # demand spikes after week 10
            self.history.append({
                "timestep": timestep,
                "demand": demand,
                "inventory": self.depot.inventory,
                "backlog": self.depot.backlog
            })

    
    def plot_results(self):
        """
        Plot results and visualization.
        """
        pass