#!/usr/bin/env python3
import argparse

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


class Arc:

    __slots__ = (
        "_cx",
        "_cy",
        "_r",
        "_a1",
        "_a2",
        "_theta",
        "_x_theta",
        "_y_theta",
        "t_vals",
        "theta_vals",
        "x_vals",
        "y_vals",
    )

    def __init__(self, cx=0, cy=0, r=1, angle_start_deg=0, angle_end_deg=180):
        # Convert degrees to radians
        self._a1 = np.radians(angle_start_deg)
        self._a2 = np.radians(angle_end_deg)

        # Symbolic setup
        self._theta = sp.Symbol("theta")

        # Create arc equations
        self._cx = cx
        self._cy = cy
        self._r = r
        self._x_theta = self._cx + self._r * sp.cos(self._theta)
        self._y_theta = self._cy + self._r * sp.sin(self._theta)

        # Create theta vector
        self.theta_vals = np.linspace(self._a1, self._a2, 1000)

        # Create symbolic function
        x_func = sp.lambdify(self._theta, self._x_theta, "numpy")
        y_func = sp.lambdify(self._theta, self._y_theta, "numpy")

        # Value symbolic functions
        self.x_vals = x_func(self.theta_vals)
        self.y_vals = y_func(self.theta_vals)


def draw_jpj_symbol(
    cx=0.0,
    cy=0.0,
    radius=1.0,
    alpha=15.0,
    colored=False,
    show_plot=True,
    save_fig=True,
    show_support_points=False,
    show_support_circles=False,
    verbose=False,
    LW=15,  # LineWidth
    MS=30,  # MarkerSize
):
    def _print(x):
        if verbose:
            print(x)

    def point_on_circle(center, radius, angle_deg):
        angle_rad = np.radians(angle_deg)
        return np.array(
            [
                center[0] + radius * np.cos(angle_rad),
                center[1] + radius * np.sin(angle_rad),
            ]
        )

    def find_circle_centers(A, B, r):
        mid = (A + B) / 2
        d = np.linalg.norm(B - A)

        if d > 2 * r:
            raise ValueError(
                "No circle can pass through the points with the given radius."
            )

        h = np.sqrt(r**2 - (d / 2) ** 2)

        # Perpendicular direction
        dir = B - A
        perp = np.array([-dir[1], dir[0]]) / d

        center1 = mid + h * perp
        center2 = mid - h * perp

        return center1, center2

    def plot_circle(ax, center, radius, **kwargs):
        circle = plt.Circle(center, radius, fill=False, **kwargs)
        ax.add_artist(circle)

    def find_circumcircle(A, B, C):
        # From: https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_2
        z1 = A[0] + 1j * A[1]
        z2 = B[0] + 1j * B[1]
        z3 = C[0] + 1j * C[1]

        w = (z3 - z1) / (z2 - z1)

        if abs(w.imag) <= 0:
            raise ValueError(f"Points are collinear: {z1}, {z2}, {z3}")

        c = (z2 - z1) * (w - abs(w) ** 2) / (2j * w.imag) + z1
        r = abs(z1 - c)

        return np.array([c.real, c.imag]), r

    # Step 0: Define properties
    alpha_rad = np.radians(alpha)
    angle_B = 90 + alpha
    angle_C = 90 - alpha
    angle_3 = 180 - alpha

    # Step 1: Define circle 1
    centerB = np.array([cx, cy])

    # Step 2: Compute points on Circle 1
    point_2 = point_on_circle(centerB, radius, alpha)  # Point A at alpha°
    point_B = point_on_circle(
        centerB, radius, angle_B
    )  # Point B at (90 + alpha)° on Circle 1

    # Step 3: Find center(s) of circle passing through A and B
    _, centerA = find_circle_centers(point_2, point_B, radius)

    # Step 4: Compute points for the third circle
    point_C = point_on_circle(
        centerB, radius, angle_C
    )  # Point C at (90 - alpha)° on C1
    point_3 = point_on_circle(
        centerB, radius, angle_3
    )  # Point D at (180 - alpha)° on C1

    # Step 5: Find center(s) of the third circle passing through C and D
    _, centerC = find_circle_centers(point_C, point_3, radius)

    # Step 6: Find points on C2
    angle_E = np.degrees(
        np.arccos(np.sin(alpha_rad) - np.cos(alpha_rad) - centerB[0] / radius)
    )
    point_1 = point_on_circle(centerA, radius, angle_E)

    # Step 7: Get arcs
    arcA = Arc(*centerA, radius, angle_E, 270 + alpha)  # See calculations
    arcB = Arc(*centerB, radius, alpha, angle_3)
    arcC = Arc(*centerC, radius, -90 - alpha, 180 - angle_E)  # See calculations

    # Step 9: Find circumcircle
    circumcenter, circumradius = find_circumcircle(centerB, centerA, centerC)

    # Step 8: Plot everything
    _, ax = plt.subplots()
    plt.get_current_fig_manager().full_screen_toggle()
    ax.set_aspect("equal")
    ax.grid(False)
    ax.set_ylim(centerB[1] - 0.125 * radius, centerB[1] + 2 * radius)
    if not (show_support_circles or show_support_points):
        ax.axis("off")
        ax.set_xticks([])
        ax.set_yticks([])

    # Plot circles
    if show_support_circles:
        ax.set_xlim(centerB[0] - 2 * radius, centerB[0] + 2 * radius)
        ax.set_ylim(centerB[1] - 1.25 * radius, centerB[1] + 2.5 * radius)
        plot_circle(
            ax,
            centerA,
            radius,
            color="red" if colored else "black",
            linestyle="-.",
            label="Circle A",
        )
        plot_circle(
            ax,
            centerB,
            radius,
            color="green" if colored else "black",
            linestyle="--",
            label="Circle B",
        )
        plot_circle(
            ax,
            centerC,
            radius,
            color="blue" if colored else "black",
            linestyle=":",
            label="Circle C",
        )

    # Plot arcs
    ax.plot(
        arcA.x_vals,
        arcA.y_vals,
        color="red" if colored else "black",
        linestyle="-",
        linewidth=LW,
        label="Arc A",
    )
    ax.plot(
        arcB.x_vals,
        arcB.y_vals,
        color="green" if colored else "black",
        linestyle="-",
        linewidth=LW,
        label="Arc B",
    )
    ax.plot(
        arcC.x_vals,
        arcC.y_vals,
        color="blue" if colored else "black",
        linestyle="-",
        linewidth=LW,
        label="Arc C",
    )
    plot_circle(
        ax,
        circumcenter,
        0.9 * circumradius,
        color="black",
        linestyle="-",
        linewidth=LW,
        label="Circle",
    )

    # Plot points
    if colored:
        ax.plot(
            *point_1,
            "v",
            color="red" if colored else "black",
            markersize=MS,
            label=f"Point 1 ({angle_E:.2f}° on Circle B)",
        )
        ax.plot(
            *point_2,
            "<",
            color="green" if colored else "black",
            markersize=MS,
            label=f"Point 2 ({alpha}° on Circle A)",
        )
        ax.plot(
            *point_3,
            ">",
            color="blue" if colored else "black",
            markersize=MS,
            label=f"Point 3 ({angle_3}° on Circle A)",
        )

    if show_support_points:
        ax.plot(
            *point_B,
            "o",
            color="silver" if colored else "black",
            fillstyle="none",
            markersize=MS,
            linewidth=LW,
            label=f"Point B ({angle_B}° on Circle A)",
        )
        ax.plot(
            *point_C,
            "o",
            color="silver" if colored else "black",
            fillstyle="none",
            markersize=MS,
            linewidth=LW,
            label=f"Point C ({angle_C}° on Circle A)",
        )

    # Plot centers
    if show_support_circles:
        ax.plot(
            *centerA,
            "o",
            color="red" if colored else "black",
            markersize=MS,
            label="Center of Circle A",
        )
        ax.plot(
            *centerB,
            "o",
            color="green" if colored else "black",
            markersize=MS,
            label="Center of Circle B",
        )
        ax.plot(
            *centerC,
            "o",
            color="blue" if colored else "black",
            markersize=MS,
            label="Center of Circle C",
        )
        ax.plot(*circumcenter, "o", color="black", markersize=MS, label="Circumcenter")

    # Show the plot
    if colored:
        leg = ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
        for legend_handle in leg.legend_handles:
            try:
                legend_handle.set_linewidth(1)
                legend_handle.set_markersize(7)
            except AttributeError:
                pass

    if save_fig:
        FIGURE_NAME = "jpj_symbol.svg"
        plt.savefig(FIGURE_NAME, bbox_inches="tight")
        print(f"Figure saved as {FIGURE_NAME}")
    if show_plot:
        ax.set_title("Led Zeppelin's John Paul Jones' symbol")
        plt.show()
    elif save_fig:
        plt.close()

    _print(
        f"""
---------------
>>> CIRCLES <<<
---------------
Circle 1:
    x: {centerB[0]}
    y: {centerB[1]}
Circle 2:
    x: {centerA[0]}
    y: {centerA[1]}  
Circle 3:
    x: {centerC[0]}
    y: {centerC[1]}

--------------
>>> POINTS <<<
--------------
Point A:
    x: {point_2[0]}
    y: {point_2[1]}
Point B:
    x: {point_B[0]}
    y: {point_B[1]}
Point C:
    x: {point_C[0]}
    y: {point_C[1]}
Point D:
    x: {point_3[0]}
    y: {point_3[1]}
Point E:
    x: {point_1[0]}
    y: {point_1[1]}
"""
    )

    return arcA, arcB, arcC


def main():
    parser = argparse.ArgumentParser(
        prog="JPJ",
        description="Draw Led Zeppelin's John Paul Jones' symbol.",
        epilog="\N{COPYRIGHT SIGN} 2025 Vincenzo Petrone",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
        default=1.0,
        help="radius of the circles [m]",
    )
    parser.add_argument(
        "-a",
        "--angle",
        metavar="A",
        type=float,
        default=15,
        help="Angle [°]",
    )
    parser.add_argument(
        "-c", "--colored", action="store_true", help="The symbol is plotted as colored"
    )
    parser.add_argument(
        "-n",
        "--no-plot",
        dest="show_plot",
        action="store_false",
        help="Do not show the plot window",
    )
    parser.add_argument(
        "-o", "--save-fig", dest="save_fig", action="store_true", help="Save the figure"
    )
    parser.add_argument(
        "-p",
        "--show-support-points",
        action="store_true",
        help="Show support points",
    )
    parser.add_argument(
        "-s",
        "--show-support-circles",
        action="store_true",
        help="Show support circles",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show debug prints"
    )

    args = parser.parse_args()

    draw_jpj_symbol(
        cx=args.offset_x,
        cy=args.offset_y,
        radius=args.radius,
        alpha=args.angle,
        colored=args.colored,
        show_plot=args.show_plot,
        save_fig=args.save_fig,
        show_support_points=args.show_support_points,
        show_support_circles=args.show_support_circles,
        verbose=args.verbose,
        LW=15,
        MS=30,
    )


if __name__ == "__main__":
    main()
