import plotnine as p9
import polars as pl
from plotnine.data import mtcars, penguins

from p9customtheme import custom_discrete, custom_theme


def test_simple_plot():
    p = p9.ggplot(mtcars, p9.aes("wt", "mpg")) + p9.geom_point()
    assert p == "test_simple_plot"


def test_boxplot():
    p = (
        p9.ggplot(penguins, p9.aes("species", "bill_length_mm", fill="island"))
        + p9.geom_boxplot()
        + custom_discrete()
        + p9.labs(
            title="Penguin bill length by species and island".title(),
            subtitle="A comparison based on example data",
            x="species",
            y="bill length [mm]",
            fill="Island",
        )
    )

    assert p == "boxplot_simple"


def test_colors():
    colors_n = 7
    df = pl.DataFrame(
        {"y": list(range(1, colors_n + 1)), "x": [f"{i}" for i in range(colors_n)]}
    )
    p = (
        p9.ggplot(df, p9.aes("x", "y", fill="x"))
        + p9.geom_col()
        + custom_discrete()
        + p9.scale_y_continuous(expand=(0, 0))
    )
    assert p == f"colors_{colors_n}"


def test_scatter_colors():
    p = (
        p9.ggplot(penguins, p9.aes("bill_depth_mm", "bill_length_mm", fill="species"))
        + p9.geom_point()
        + p9.labs(
            title="Penguin Bill Length vs Depth",
            x="Bill Depth [mm]",
            y="Bill Length [mm]",
            fill="Species",
        )
        + custom_discrete()
    )
    assert p == "scatter_colors"


def test_grid():
    p = (
        p9.ggplot(penguins, p9.aes("bill_depth_mm", "bill_length_mm", fill="sex"))
        + p9.geom_point()
        + p9.labs(
            title="Penguin Bill Length vs Depth",
            x="Bill Depth [mm]",
            y="Bill Length [mm]",
            fill="Sex",
        )
        + p9.facet_grid("species ~ island")
        + custom_discrete()
        + p9.theme(panel_border=p9.element_rect(color="black"))
        + custom_theme(base_size=9.5)
    )
    assert p == "grid_plot"


def test_complex_grid():
    p = (
        p9.ggplot(
            (
                pl.DataFrame(penguins.dropna())
                .with_columns(pl.col("body_mass_g") / 1000)
                .group_by(["species", "year", "sex"])
                .agg(pl.col("body_mass_g").mean())
                .with_columns(pl.col("year").cast(pl.String))
            ),
            mapping=p9.aes(x="year", y="sex", size="body_mass_g", fill="species"),
        )
        + p9.geom_point()
        + p9.facet_wrap("~species", ncol=1)
        + p9.labs(
            title="Penguin Mean Weight",
            x="Year",
            y="Sex",
            size="Body Mass [kg]",
            fill="Species",
        )
        + custom_theme(rotate_label=90)
        + p9.theme(
            figure_size=(3, 4),
            plot_title=p9.element_text(ha="center"),
        )
        + custom_discrete(reverse=True)
    )
    assert p == "grid_complex_plot"
