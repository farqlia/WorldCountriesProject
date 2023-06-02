import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
from src.data_preprocessing.utils import get_continents


def cut_names(df):
    values = df.index.values
    return [val[:20] for val in values]


# Annotate Median Age for each country
def plot_age_structure(age_structure_df, index_order):
    n_countries = len(index_order)
    age_structure_df = age_structure_df.loc[index_order]
    n_cols_per_plot = 4
    n_countries_per_row = 12

    n_rows = n_countries // n_countries_per_row
    n_cols = 3
    i = 1
    for row in range(0, n_rows):
        for col in range(0, n_cols):
            plt.subplot(n_rows, n_cols, i)
            i += 1
            curr_rows = age_structure_df.iloc[row * n_countries_per_row + col * n_cols_per_plot:
                                              min(n_countries, row * n_countries_per_row + (col + 1) * n_cols_per_plot)]
            spc = np.arange(len(curr_rows))
            plt.bar(spc, curr_rows['0-14 years'], width=0.3, label='0-14 years', edgecolor='k')
            plt.bar(spc + 0.3, curr_rows['15-64 years'], width=0.3, label='15-64 years', edgecolor='k')
            plt.bar(spc + 0.6, curr_rows['65 years and over'], width=0.3, label='65 years and over', edgecolor='k')
            plt.xticks(spc + 0.45 / 2, cut_names(curr_rows))
        plt.legend(bbox_to_anchor=(1.25, 0.6), loc='center right')


def plot_x_vs_y(x_series, y_series, x_name, y_name, ax, color='#f653a6'):
    ax.scatter(x=x_series, y=y_series, color=color, alpha=0.7)
    ax.set_title(f"{x_name.capitalize()} VS {y_name.capitalize()}")
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)


def plot_metric_distribution(metric_series, metric_name, ax, color='#14b0ff', scale=None):
    ax.set_title(f"Distribution of {metric_name}")
    ax.set_xlabel(metric_name)
    if scale:
        ax.set_xscale(scale)
    ax.hist(metric_series, density=True, color=color, edgecolor="white")


def plot_data_distributions(countries_data_df, metrics_to_plot):
    n_rows = (len(metrics_to_plot) + 1) // 2
    n_cols = 4
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 80), layout='constrained')

    colors = colormaps['Accent'](np.random.rand(len(metrics_to_plot)))[:, :3]

    # Add transparency to better see the density
    for i in range(n_rows):
        for j in range(2):
            index = 2 * i + j
            if index < len(metrics_to_plot):
                idx = 2 * i + j
                metric_name = metrics_to_plot[idx]
                plot_metric_distribution(countries_data_df[metric_name], metric_name, ax=axes[i, 2 * j],
                                         color=colors[idx]) 
                plot_metric_distribution(countries_data_df[metric_name], 'Log10 of ' + metric_name, ax=axes[i, 2 * j + 1],
                                         color=colors[idx], scale='symlog') 
                



def create_grid_dist_and_scatter_plots(median_age_series, countries_data_df, metrics_to_plot, 
                                       transformation_function=None, figsize=(20, 80)):
    n_rows = (len(metrics_to_plot) + 1) // 2
    n_cols = 4
    _, axes = plt.subplots(n_rows, n_cols, figsize=figsize, layout='constrained')

    axes = axes.flatten()

    colors = colormaps['PuRd'](np.random.rand(len(metrics_to_plot)))[:, :3]

    # Add transparency to better see the density

    for index, metric_name in enumerate(metrics_to_plot):
        metric_series = transformation_function(countries_data_df[metric_name]) if transformation_function else countries_data_df[metric_name]

        plot_x_vs_y(median_age_series, metric_series, 'Median Age', metric_name,
                                        ax=axes[2 * index], color=colors[index])
        plot_metric_distribution(metric_series, metric_name, ax=axes[2 * index + 1],
                                    color=colors[index])
        


def plot_by_continent(x_series, y_series, continents_series, x_name, y_name):

    continents = get_continents()
    _, axes = plt.subplots(2, (len(continents) + 1) // 2, 
                           figsize=(20, 12))
    axes = axes.flatten() 

    cmap = colormaps['winter'](np.linspace(0, 1, len(continents)))[:, :3]

    for i, continent in enumerate(continents):
        idx = np.flatnonzero(continents_series == continent)
        plot_x_vs_y(x_series[idx], y_series[idx], x_name, y_name, axes[i],
                    color=cmap[i])
        axes[i].set_title(continent)

