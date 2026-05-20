from math import exp

from facility import Facility
from policies import naive_policy


class Simulation:
    """
    Runs the simulation experiment and provides reporting functions.

    Pricing models:
        - linear:
            The entire gasoline price responds proportionally to inventory
            shortfall.
        - exponential:
            The entire gasoline price responds exponentially to scarcity.
        - hybrid:
            Only the refining/distribution/retail component responds
            exponentially to scarcity, while crude oil is added separately
            as a direct input cost.
    """
    def __init__(self, delay: int = 1, pricing: str = "hybrid"):
        self.depot = Facility(
            name="Fuel Depot",
            initial_inventory=20.0,
            delay=delay
        )

        # Selected pricing model
        self.pricing = pricing

        # Pricing parameters
        # Normal gasoline price = $5.00/gal
        #   - $3.00 refining + distribution + retail
        #   - $2.00 crude oil input cost
        self.base_price = 3.00          # scarcity-sensitive component ($/gal)
        self.target_inventory = 20.0    # desired inventory level
        self.k = 0.05                   # exponential scarcity sensitivity
        self.beta = 0.05                # linear price slope ($/unit shortfall)

        self.history = []


    def run(self, duration: int = 52) -> None:
        """
        Run the simulation for a given number of time steps.
        """
        self.history = []  # reset history

        # Constant customer demand (you can later introduce shocks)
        demand = 5.0

        # Record initial conditions
        initial_order = naive_policy(
            self.depot.inventory,
            self.target_inventory
        )

        self.history.append({
            "timestep": 0,
            "demand": demand,
            "inventory": self.depot.inventory,
            "backlog": self.depot.backlog,
            "order": initial_order,
            "price": self.compute_price(0)
        })

        for t in range(1, duration + 1):
            # Example demand shock:
            # demand = 5.0 if t < 10 else 10.0

            order = naive_policy(
                self.depot.inventory,
                self.target_inventory
            )

            result = self.depot.step(demand, order)
            price = self.compute_price(t)

            self.history.append({
                "timestep": t,
                "demand": demand,
                "inventory": result["inventory"],
                "backlog": result["backlog"],
                "order": order,
                "price": price
            })


    def crude_price(self, t: int) -> float:
        """
        Direct crude oil input cost ($/gal).
        This is treated as a fixed additive component in the hybrid model.
        """
        return 2.00


    def baseline_price(self, t: int) -> float:
        """
        Total normal gasoline price ($/gal).
        Under typical conditions:
            $3.00 refining/distribution/retail
          + $2.00 crude oil
          = $5.00 total
        """
        return self.base_price + self.crude_price(t)


    def compute_price(self, t: int) -> float:
        """
        Dispatch to the selected pricing model.
        """
        match self.pricing:
            case "linear":
                return self._price_linear(t)
            case "exponential":
                return self._price_exponential(t)
            case "hybrid":
                return self._price_hybrid(t)
            case _:
                raise ValueError(f"Unknown pricing model: {self.pricing}")


    def _inventory_shortfall(self) -> float:
        """
        Positive when inventory is below target.
        Negative when inventory is above target.
        """
        return self.target_inventory - self.depot.inventory


    def _price_linear(self, t: int) -> float:
        """
        Linear pricing model:
            P = P0 + beta * (I* - I)

        where:
            P0 = total baseline gasoline price ($5.00), including crude.

        The entire gasoline price responds proportionally to inventory
        shortfall.
        """
        shortfall = self._inventory_shortfall()

        return (
            self.baseline_price(t) +
            self.beta * shortfall
        )


    def _price_exponential(self, t: int) -> float:
        """
        Exponential scarcity model:
            P = P0 * exp(k * (I* - I))

        where:
            P0 = total baseline gasoline price ($5.00), including crude.

        The entire gasoline price is amplified exponentially when
        inventory becomes scarce.
        """
        shortfall = self._inventory_shortfall()

        return (
            self.baseline_price(t) *
            exp(self.k * shortfall)
        )

    def _price_hybrid(self, t: int) -> float:
        """
        Hybrid pricing model:
            P = P_distribution * exp(k * (I* - I)) + C_crude

        where:
            P_distribution = $3.00 refining/distribution/retail component
            C_crude       = $2.00 crude oil input cost

        Only the non-crude portion is amplified by scarcity.

        At target inventory:
            3.00 * exp(0) + 2.00 = 5.00
        """
        shortfall = self._inventory_shortfall()

        return (
            self.base_price *
            exp(self.k * shortfall) +
            self.crude_price(t)
        )