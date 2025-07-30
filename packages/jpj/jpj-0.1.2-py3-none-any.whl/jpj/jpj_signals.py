import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import argparse

from .jpj import Arc, draw_jpj_symbol


class ArcSignals(Arc):

    __slots__ = ["dx_vals", "dy_vals", "ddx_vals", "ddy_vals"]

    def __init__(self, arc: Arc, max_speed: float, frequency: float):
        # Create arc
        super().__init__(
            arc._cx, arc._cy, arc._r, np.degrees(arc._a1), np.degrees(arc._a2)
        )

        # Compute final time
        final_time = 2 * (self._a2 - self._a1) / max_speed

        # Define velocity profile
        t = sp.Symbol("t")
        norm = np.pi / final_time  # Normalization factor
        t_norm = norm * t  # Normalized time
        theta_t = (
            max_speed / 2 / norm * (t_norm - sp.sin(t_norm) * sp.cos(t_norm)) + self._a1
        )  # θ(t)
        dtheta_t = max_speed * sp.sin(t_norm) ** 2  # dθ/dt
        ddtheta_t = 2 * max_speed * norm * sp.sin(t_norm) * sp.cos(t_norm)  # d2θ/dt2

        # Define parametric derivatives
        dx_theta = sp.simplify(sp.diff(self._x_theta, self._theta))  # dx/dθ
        dy_theta = sp.simplify(sp.diff(self._y_theta, self._theta))  # dy/dθ
        ddx_theta = sp.simplify(sp.diff(dx_theta, self._theta))  # d2x/dθ2
        ddy_theta = sp.simplify(sp.diff(dy_theta, self._theta))  # d2y/dθ2

        # Define expressions (they will depend on both θ and t)
        dx_t = sp.simplify(dx_theta * dtheta_t)  # dx/dt = dx/dθ * dθ/dt
        dy_t = sp.simplify(dy_theta * dtheta_t)  # dy/dt = dy/dθ * dθ/dt
        ddx_t = sp.simplify(
            dx_theta * ddtheta_t + ddx_theta * dtheta_t**2
        )  # d2x/dt2 = dx/dθ * d2θ/dt2 + d2x/dθ2 * dθ/dt^2
        ddy_t = sp.simplify(
            dy_theta * ddtheta_t + ddy_theta * dtheta_t**2
        )  # d2y/dt2 = dy/dθ * d2θ/dt2 + d2y/dθ2 * dθ/dt^2

        # Substitute theta with t
        x_t = sp.simplify(self._x_theta.subs(self._theta, theta_t))  # x(t)
        y_t = sp.simplify(self._y_theta.subs(self._theta, theta_t))  # y(t)
        dx_t = sp.simplify(dx_t.subs(self._theta, theta_t))  # dx(t)
        dy_t = sp.simplify(dy_t.subs(self._theta, theta_t))  # dy(t)
        ddx_t = sp.simplify(ddx_t.subs(self._theta, theta_t))  # ddx(t)
        ddy_t = sp.simplify(ddy_t.subs(self._theta, theta_t))  # ddy(t)

        # Create symbolic functions
        theta_func = sp.lambdify(t, theta_t, "numpy")
        x_func = sp.lambdify(t, x_t, "numpy")
        y_func = sp.lambdify(t, y_t, "numpy")
        dx_func = sp.lambdify(t, dx_t, "numpy")
        dy_func = sp.lambdify(t, dy_t, "numpy")
        ddx_func = sp.lambdify(t, ddx_t, "numpy")
        ddy_func = sp.lambdify(t, ddy_t, "numpy")

        # Value symbolic functions
        self.t_vals = np.arange(0, final_time, 1 / frequency)
        self.theta_vals = theta_func(self.t_vals)
        self.x_vals = x_func(self.t_vals)
        self.y_vals = y_func(self.t_vals)
        self.dx_vals = dx_func(self.t_vals)
        self.dy_vals = dy_func(self.t_vals)
        self.ddx_vals = ddx_func(self.t_vals)
        self.ddy_vals = ddy_func(self.t_vals)


def jpj_signals(
    frequency: float = 1000,
    radius: float = 0.2,
    max_speed: float = 0.1,
    show_plot: bool = True,
):
    # Compute arcs
    arc1, arc2, arc3 = draw_jpj_symbol(
        radius=radius,
        alpha=15,
        colored=True,
        show_plot=show_plot,
        save_fig=False,
        show_support_points=False,
        show_support_circles=True,
        verbose=False,
    )

    # Compute x-y velocities and accelerations
    max_speed /= radius
    arc1 = ArcSignals(arc1, max_speed, frequency)
    arc2 = ArcSignals(arc2, max_speed, frequency)
    arc3 = ArcSignals(arc3, max_speed, frequency)

    # Compose signals
    t = arc1.t_vals - arc1.t_vals[0]
    t = np.concatenate((t, t[-1] + arc2.t_vals - arc2.t_vals[0]))
    t = np.concatenate((t, t[-1] + arc3.t_vals - arc3.t_vals[0]))
    x = np.concatenate((arc1.x_vals, arc2.x_vals, arc3.x_vals))
    y = np.concatenate((arc1.y_vals, arc2.y_vals, arc3.y_vals))
    dx = np.concatenate((arc1.dx_vals, arc2.dx_vals, arc3.dx_vals))
    dy = np.concatenate((arc1.dy_vals, arc2.dy_vals, arc3.dy_vals))
    ddx = np.concatenate((arc1.ddx_vals, arc2.ddx_vals, arc3.ddx_vals))
    ddy = np.concatenate((arc1.ddy_vals, arc2.ddy_vals, arc3.ddy_vals))
    v = np.sqrt(dx**2 + dy**2)

    # Create plots
    if show_plot:
        # Plot time history
        plt.figure(figsize=(10, 4))
        nrows = 3
        ncols = 2

        # x history
        plt.subplot(nrows, ncols, 1)
        plt.title("x(t)")
        plt.plot(t, x, label="x(t)")
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.xlim(0, t[-1])
        plt.xlabel("t [s]")
        plt.ylabel("x [m]")
        plt.legend()
        plt.grid(False)

        # y history
        plt.subplot(nrows, ncols, 2)
        plt.title("y(t)")
        plt.plot(t, y, label="y(t)")
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.xlim(0, t[-1])
        plt.xlabel("t [s]")
        plt.ylabel("y [m]")
        plt.legend()
        plt.grid(False)

        # dx history
        plt.subplot(nrows, ncols, 3)
        plt.title("dx(t)")
        plt.plot(t, dx, label="dx(t)")
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.axhline(y=0, linewidth=0.5, linestyle="--", color="grey")
        plt.xlim(0, t[-1])
        plt.xlabel("t [s]")
        plt.ylabel("dx [m/s]")
        plt.legend()
        plt.grid(False)

        # dy history
        plt.subplot(nrows, ncols, 4)
        plt.title("dy(t)")
        plt.plot(t, dy, label="dy(t)")
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.axhline(y=0, linewidth=0.5, linestyle="--", color="grey")
        plt.xlim(0, t[-1])
        plt.xlabel("t [s]")
        plt.ylabel("dy [m/s]")
        plt.legend()
        plt.grid(False)

        # ddx history
        plt.subplot(nrows, ncols, 5)
        plt.title("ddx(t)")
        plt.plot(t, ddx, label="ddx(t)")
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.axhline(y=0, linewidth=0.5, linestyle="--", color="grey")
        plt.xlim(0, t[-1])
        plt.xlabel("t [s]")
        plt.ylabel("ddx [m/s2]")
        plt.legend()
        plt.grid(False)

        # ddy history
        plt.subplot(nrows, ncols, 6)
        plt.xlabel("t [s]")
        plt.plot(t, ddy, label="ddy(t)")
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.axhline(y=0, linewidth=0.5, linestyle="--", color="grey")
        plt.xlim(0, t[-1])
        plt.title("ddy(t)")
        plt.ylabel("ddy [m/s2]")
        plt.legend()
        plt.grid(False)

        # Plot the 3 arcs
        plt.figure(figsize=(10, 4))
        nrows = 3
        ncols = 2

        # Arc1: x
        plt.subplot(nrows, ncols, 1)
        plt.plot(np.degrees(arc1.theta_vals), arc1.x_vals)
        plt.title("x_1(θ)")
        plt.xlabel("θ [°]")
        plt.ylabel("x [m]")
        plt.grid(True)

        # Arc1: y
        plt.subplot(nrows, ncols, 2)
        plt.plot(np.degrees(arc1.theta_vals), arc1.y_vals)
        plt.title("y_1(θ)")
        plt.xlabel("θ [°]")
        plt.ylabel("y [m]")
        plt.grid(True)

        # Arc2: x
        plt.subplot(nrows, ncols, 3)
        plt.plot(np.degrees(arc2.theta_vals), arc2.x_vals)
        plt.title("x_2(θ)")
        plt.xlabel("θ [°]")
        plt.ylabel("x [m]")
        plt.grid(True)

        # Arc2: y
        plt.subplot(nrows, ncols, 4)
        plt.plot(np.degrees(arc2.theta_vals), arc2.y_vals)
        plt.title("y_2(θ)")
        plt.xlabel("θ [°]")
        plt.ylabel("y [m]")
        plt.grid(True)

        # Arc3: x
        plt.subplot(nrows, ncols, 5)
        plt.plot(np.degrees(arc3.theta_vals), arc3.x_vals)
        plt.title("x_3(θ)")
        plt.xlabel("θ [°]")
        plt.ylabel("x [m]")
        plt.grid(True)

        # Arc3: y
        plt.subplot(nrows, ncols, 6)
        plt.plot(np.degrees(arc3.theta_vals), arc3.y_vals)
        plt.title("y_3(θ)")
        plt.xlabel("θ [°]")
        plt.ylabel("y [m]")
        plt.grid(True)

        # Plot tangential velocity
        plt.figure()
        plt.plot(t, v)
        plt.axvline(
            x=arc2.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
            label="New stroke",
        )
        plt.axvline(
            x=arc2.t_vals[-1] + arc1.t_vals[-1],
            linewidth=0.5,
            linestyle="--",
            color="k",
        )
        plt.title("Tangential velocity")
        plt.xlim(0, t[-1])
        plt.xlabel("t [s]")
        plt.ylabel("v [m/s]")
        plt.grid(False)

        # Show plot
        plt.show()

    return t, x, y, dx, dy, ddx, ddy


def main():
    parser = argparse.ArgumentParser(
        prog="JPJ signals",
        description="Generate JPJ symbol arcs' velocity/acceleration signals.",
        epilog="\N{COPYRIGHT SIGN} 2025 Vincenzo Petrone",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--frequency",
        metavar="F",
        type=float,
        default=1000,
        help="The frequency at which signals are generated [Hz]",
    )
    parser.add_argument(
        "-x",
        "--offset-x",
        metavar="X",
        type=float,
        default=0.0,
        help="x-offset [m]",
    )
    parser.add_argument(
        "-y",
        "--offset-y",
        metavar="Y",
        type=float,
        default=0.0,
        help="y-offset [m]",
    )
    parser.add_argument(
        "-r",
        "--radius",
        metavar="R",
        type=float,
        default=0.2,
        help="Radius of the arcs",
    )
    parser.add_argument(
        "-s",
        "--max_speed",
        metavar="S",
        type=float,
        default=0.1,
        help="Maximum tangential speed [m/s]",
    )
    parser.add_argument(
        "-n",
        "--no-plot",
        dest="show_plot",
        action="store_false",
        help="Do not show the plot window",
    )
    args = parser.parse_args()

    jpj_signals(
        frequency=args.frequency,
        radius=args.radius,
        max_speed=args.max_speed,
        show_plot=args.show_plot,
    )


if __name__ == "__main__":
    main()
