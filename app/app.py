#These are everything you need to run the shiny for python playground
import seaborn as sns # chart
from faicons import icon_svg # to display icons
from shinyswatch import theme # to change the visual style of ui
from shiny import reactive # to make the ui change based on components
from shiny.express import input, render, ui # the components and display window
import palmerpenguins # dataset 
import plotly.express as px

from shinywidgets import render_plotly

df = palmerpenguins.load_penguins() # loading the dataset and creating a reference

theme.sketchy() # bootswatch themes are premade and similar to microsoft themes

ui.page_opts(title="Brittany's Updated Penguins dashboard", window_title="Dowdle P7", fillable=True) # Page options include a title, window title, and how the ui is scaled to the screen being used


with ui.sidebar(title="Choose the mass and species of penguins", style= "font-weight: bold;"): # sidebars hold all of the input components that make the ui filtered
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr() # horizontal rule is just a line that providea a spacer line to separate areas of the sidebar
    ui.h6("Resource Links", style= "font-weight: bold;")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False): # this will determine how the output components are displayed and their scale to the screen being viewed on
    with ui.value_box(showcase=icon_svg("earlybirds"), style= "font-weight: bold;"): # value boxes make easy visuals for reactive calculations based on filters
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style= "font-weight: bold;"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), style= "font-weight: bold;"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns(): # creates a second set of columns for visuals, normally dataframes and charts
    with ui.card(full_screen=True):
        ui.card_header("Bill length compared to depth", style= "font-weight: bold;")

        @render_plotly
        def length_depth_plotly():
            return px.histogram(
                data_frame=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
            )

    with ui.card(full_screen=True): # cards keep your visual in a contained space and provides spacing between other visuals
        ui.card_header("Penguin data grid - input filters", style= "font-weight: bold;")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc # Function to calculate filtered dataframe based on input values
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
