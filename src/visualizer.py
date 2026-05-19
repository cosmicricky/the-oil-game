import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class Visualizer:
    def __init__(self, history: list):
        self.history = history
        self.current_step = 0
    

    def show(self):
        self._create_figure()
        self._create_controls()
        self._draw_step()
        plt.show()


    def _create_figure(self):
        """
        Create a single combined plot using the same layout as the static plot.
        """
        # Create figure and primary axis
        self.fig, self.ax1 = plt.subplots(figsize=(12, 6))

        # Secondary axis for price
        self.ax2 = self.ax1.twinx()

        # Extract data from simulation history
        self.t = [h["timestep"] for h in self.history]
        self.inventory = [h["inventory"] for h in self.history]
        self.demand = [h["demand"] for h in self.history]
        self.order = [h["order"] for h in self.history]
        self.price = [h["price"] for h in self.history]

        # ------------------------------------------------------------------
        # Plot Inventory as a filled area (to emphasize that it is a stock)
        # ------------------------------------------------------------------
        self.ax1.fill_between(
            self.t,
            self.inventory,
            alpha=0.25,
            label="Inventory"
        )

        self.ax1.plot(
            self.t,
            self.inventory,
            linewidth=2.5
        )

        # Demand (dashed line)
        self.ax1.plot(
            self.t,
            self.demand,
            color="orange",
            linestyle="--",
            linewidth=2,
            label="Demand"
        )

        # Orders
        self.ax1.plot(
            self.t,
            self.order,
            color="orange",
            linewidth=2.5,
            label="Orders"
        )

        # Price on secondary axis
        self.ax2.plot(
            self.t,
            self.price,
            color="red",
            linewidth=2.5,
            label="Fuel Price"
        )

        # ------------------------------------------------------------------
        # Axis labels and formatting
        # ------------------------------------------------------------------
        self.ax1.set_xlabel("Week")
        self.ax1.set_ylabel("Units")
        self.ax2.set_ylabel("Price ($/gal)")

        self.ax1.set_title("Oil Game: Inventory, Orders, Demand, and Dynamic Pricing")

        self.ax1.grid(True, alpha=0.3)

        # ------------------------------------------------------------------
        # Combined legend from both axes
        # ------------------------------------------------------------------
        lines1, labels1 = self.ax1.get_legend_handles_labels()
        lines2, labels2 = self.ax2.get_legend_handles_labels()

        self.ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            loc="center right",
            frameon=True,
            facecolor="white",
            framealpha=1.0,
            edgecolor="lightgray"
        )

        # Improve layout
        self.fig.tight_layout()


    def _create_controls(self):
        """
        Create Previous and Next buttons for stepping through the simulation.
        """
        # Make room at the bottom of the figure for the buttons
        self.fig.subplots_adjust(bottom=0.18)

        # Define button positions as [left, bottom, width, height]
        ax_prev = self.fig.add_axes([0.35, 0.05, 0.12, 0.06])
        ax_next = self.fig.add_axes([0.53, 0.05, 0.12, 0.06])

        # Create buttons
        self.btn_prev = Button(ax_prev, "◀ Prev")
        self.btn_next = Button(ax_next, "Next ▶")

        # Connect button clicks to event handlers
        self.btn_prev.on_clicked(self._prev)
        self.btn_next.on_clicked(self._next)


    def _draw_step(self):
        """
        Draw (or update) the visualization for the current timestep.

        This method:
        1. Creates the vertical cursor lines the first time it is called.
        2. Moves the cursor to the selected timestep on subsequent calls.
        3. Updates a status text box showing the current values.
        4. Redraws the figure.
        """
        # Current timestep and history record
        t = self.t[self.current_step]
        h = self.history[self.current_step]

        # ------------------------------------------------------------------
        # Create cursor lines the first time this method is called
        # ------------------------------------------------------------------
        if not hasattr(self, "cursor1"):
            # Vertical cursor on primary axis
            self.cursor1 = self.ax1.axvline(
                x=t,
                color="black",
                linestyle="--",
                linewidth=1.5,
                alpha=0.8
            )

            # Matching cursor on secondary axis
            self.cursor2 = self.ax2.axvline(
                x=t,
                color="black",
                linestyle="--",
                linewidth=1.5,
                alpha=0.8
            )

            # Status text box in upper-left corner
            self.status_text = self.ax1.text(
                0.02, 0.98,
                "",
                transform=self.ax1.transAxes,
                va="top",
                ha="left",
                fontsize=10,
                bbox=dict(
                    boxstyle="round",
                    facecolor="white",
                    alpha=0.9,
                    edgecolor="lightgray"
                )
            )

        # ------------------------------------------------------------------
        # Move cursors to current timestep
        # ------------------------------------------------------------------
        self.cursor1.set_xdata([t, t])
        self.cursor2.set_xdata([t, t])

        # ------------------------------------------------------------------
        # Update status text
        # ------------------------------------------------------------------
        self.status_text.set_text(
            f"Week {h['timestep']}\n"
            f"Inventory: {h['inventory']:.1f}\n"
            f"Demand: {h['demand']:.1f}\n"
            f"Orders: {h['order']:.1f}\n"
            f"Price: ${h['price']:.2f}/gal"
        )

        # ------------------------------------------------------------------
        # Redraw the figure
        # ------------------------------------------------------------------
        self.fig.canvas.draw_idle()


    def _next(self, event):
        """
        Advance to the next timestep.
        """
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self._draw_step()


    def _prev(self, event):
        """
        Move back to the previous timestep.
        """
        if self.current_step > 0:
            self.current_step -= 1
            self._draw_step()


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