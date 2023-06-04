import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
from src.data_preprocessing.utils import get_continents
import seaborn as sns
import pandas as pd

def plot_x_vs_y(x_series, y_series, x_name, y_name, ax, color='#f653a6', yscale=None):
    ax.scatter(x=x_series, y=y_series, color=color, alpha=0.7)
    ax.set_title(f"{x_name.capitalize()} VS {y_name.capitalize()}")
    if yscale:
        ax.set_yscale(yscale)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)


def plot_metric_distribution(metric_series, metric_name, ax, color='#14b0ff', scale=None):
    ax.set_title(f"Distribution of {metric_name}")
    ax.set_xlabel(metric_name)
    if scale:
        ax.set_xscale(scale)
    ax.hist(metric_series, density=True, color=color, edgecolor="white")


def plot_data_distributions(countries_data_df, metrics_to_plot, log_scales=None,
                            n_cols=2):
    
    n_rows = (len(metrics_to_plot) + (n_cols - 1)) // n_cols
    figsize = (n_cols * 5, n_rows * 5)
    _, axes = plt.subplots(n_rows, n_cols, figsize=figsize, layout='constrained')
    axes = axes.flatten()

    colors = colormaps['Accent'](np.random.rand(len(metrics_to_plot)))

    for i, ax in enumerate(axes):
        sns.histplot(data=countries_data_df, x=metrics_to_plot[i],
                     log_scale=metrics_to_plot[i] in log_scales, ax=ax)
                

def plot_joyplot(series, hue_series):

      df = pd.DataFrame(dict(x=series, g=hue_series))

      sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

      # Initialize the FacetGrid object
      pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
      g = sns.FacetGrid(df, row="g", 
                        hue="g", aspect=15, height=.5, palette=pal)

      # Draw the densities in a few steps
      g.map(sns.kdeplot, "x",
            bw_adjust=.5, clip_on=False,
            fill=True, alpha=1, linewidth=1.5)
      g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5)

      # passing color=None to refline() uses the hue mapping
      g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


      # Define and use a simple function to label the plot in axes coordinates
      def label(x, color, label):
            ax = plt.gca()
            ax.text(-0.22, 0.2, label, fontweight="bold", color=color,
                  ha="left", va="center", transform=ax.transAxes)


      g.map(label, "x")

      # Set the subplots to overlap
      # g.figure.subplots_adjust(hspace=)

      # Remove axes details that don't play well with overlap
      g.set_titles("")
      g.set(yticks=[], ylabel="")
      g.despine(bottom=True, left=True)
      

def create_grid_dist_and_scatter_plots(median_age_series, countries_data_df, metrics_to_plot, 
                                       transformation_function=None, n_cols=4):
    
    n_rows = (len(metrics_to_plot) + (n_cols - 1)) // n_cols
    figsize = (n_cols * 5, n_rows * 6)
    _, axes = plt.subplots(n_rows, n_cols, figsize=figsize, layout='constrained')
    axes = axes.flatten()

    axes = axes.flatten()

    if len(metrics_to_plot) % 2 == 1:
        axes[-1].set_visible(False)
        axes[-2].set_visible(False)

    colors = colormaps['PuRd'](np.random.rand(len(metrics_to_plot)))[:, :3]

    # Add transparency to better see the density

    for index, metric_name in enumerate(metrics_to_plot):
        metric_series = transformation_function(countries_data_df[metric_name]) if transformation_function else countries_data_df[metric_name]

        plot_x_vs_y(median_age_series, metric_series, 'Median Age', metric_name,
                                        ax=axes[2 * index], color=colors[index])
        plot_metric_distribution(metric_series, metric_name, ax=axes[2 * index + 1],
                                    color=colors[index])
        

def create_scatter_plots(median_age_series, countries_data_df, metrics_to_plot,
                         log_scales=None, n_cols=2):

    n_rows = (len(metrics_to_plot) + (n_cols - 1)) // n_cols
    figsize = (n_cols * 5, n_rows * 5)
    _, axes = plt.subplots(n_rows, n_cols, figsize=figsize, layout='constrained')
    axes = axes.flatten()

    vals = np.linspace(0, 1, len(metrics_to_plot))

    c1 = colormaps['winter']

    if not log_scales:
        log_scales = []

    for i, ax in enumerate(axes):
        sns.scatterplot(data=countries_data_df, x=metrics_to_plot[i], 
                    y=median_age_series,
                    color=c1(vals[i]), alpha=0.7, ax=ax)
        if metrics_to_plot[i] in log_scales:
            ax.set_xscale('log')

