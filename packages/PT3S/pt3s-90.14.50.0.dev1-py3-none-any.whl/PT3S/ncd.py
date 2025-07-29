# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:18:24 2024

@author: jablonski
"""

import logging
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as path_effects
import matplotlib.patches as mpatches
try:
    from PT3S import Rm
except:
    import Rm

logger = logging.getLogger('PT3S')

def pNcd_pipes(ax=None, gdf=None, attribute=None, colors=['darkgreen', 'magenta'], legend_fmt=None, legend_values=None, norm_min=None, norm_max=None, query=None, line_width_factor=10, zorder=None):
    """
    pNcd_pipes: Plots pipes on axis with customization options.

    :param ax: Matplotlib axis object. If None, a new axis is created.
    :type ax: matplotlib.axes.Axes, optional
    :param gdf: Geospatial DataFrame containing the data to plot.
    :type gdf: geopandas.GeoDataFrame
    :param attribute: Column name in gdf of the data that should be plotted.
    :type attribute: str
    :param colors: List of colors to use for the colormap. Default is ['darkgreen', 'magenta'].
    :type colors: list, optional
    :param legend_fmt: Legend text for attribute. Default is attribute + '{:.4f}'.
    :type legend_fmt: str, optional
    :param legend_values: Specific values to use for value steps in legend. Default is None.
    :type legend_values: list, optional
    :param norm_min: Minimum value for normalization. Default is None.
    :type norm_min: float, optional
    :param norm_max: Maximum value for normalization. Default is None.
    :type norm_max: float, optional
    :param query: Query string to filter the data. Default is None.
    :type query: str, optional
    :param line_width_factor: Factor to influence width of the lines in the plot. Default is 10.
    :type line_width_factor: float, optional
    :param zorder: Determines order of plotting when calling the function multilpe times. Default is None.
    :type zorder: float, optional
    
    :return: patches.
    :rtype: matplotlib.patches.Patch
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    try:
        if ax is None:
            fig, ax = plt.subplots(figsize=(11.7, 8.3))  # A3 size
            logger.debug("{0:s}{1:s}".format(logStr, 'Created new axis.'))

        if gdf is None or gdf.empty:
            logger.debug("{0:s}{1:s}".format(logStr, 'No plot data provided.'))
            return
        if isinstance(attribute, list):
            pass
        else:
            # Set default legend_fmt if not provided
            if legend_fmt is None:
                legend_fmt = attribute + ' {:4.0f}'
            logger.debug("Fine 1")
            # Create Colormap
            cmap = mcolors.LinearSegmentedColormap.from_list('cmap', colors, N=256)
            norm_min = norm_min if norm_min is not None else gdf[attribute].min()
            norm_max = norm_max if norm_max is not None else gdf[attribute].max()
            norm = plt.Normalize(vmin=norm_min, vmax=norm_max)
            logger.debug("{0:s}norm_min: {1:10.2f} norm_max: {2:10.2f}".format(logStr, norm_min, norm_max))
            # Filter and Sort Data if Query is Provided
            df = gdf.query(query) if query else gdf
            df = df.sort_values(by=[attribute], ascending=True)

            # Plotting Data with Lines
            sizes = norm(df[attribute].astype(float)) * line_width_factor  # Scale sizes appropriately
            
            df.plot(ax=ax,
                    linewidth=sizes,
                    color=cmap(norm(df[attribute].astype(float))),
                    path_effects=[path_effects.Stroke(capstyle="round")],
                    label=attribute,
                    #alpha=0.5,
                    zorder=zorder)  # Add label for legend
            logger.debug("{0:s}{1:s}".format(logStr, f'Plotted {attribute} data.'))

            plt.axis('off')
            # Create Legend Patches
            legend_values = legend_values if legend_values is not None else np.linspace(norm_min, norm_max, num=5)
            logger.debug("{0:s}legend_values: {1}".format(logStr, legend_values))
            patches = [mpatches.Patch(color=cmap(norm(value)), label=legend_fmt.format(value)) for value in legend_values]

            return patches
        
    except Exception as e:
        logger.error("{0:s}{1:s} - {2}".format(logStr, 'Error.', str(e)))

    logger.debug("{0:s}{1:s}".format(logStr, 'End.'))

def pNcd_nodes(ax=None, gdf=None, attribute=None, colors=['darkgreen', 'magenta'], legend_fmt=None, legend_values=None, norm_min=None, norm_max=None, query=None, marker_style='o', marker_size_factor=1000.0, zorder=None):
    """
    pNcd_nodes: Plots nodes on axis with customization options.

    :param ax: Matplotlib axis object. If None, a new axis is created.
    :type ax: matplotlib.axes.Axes, optional
    :param gdf: Geospatial DataFrame containing the data to plot.
    :type gdf: geopandas.GeoDataFrame
    :param attribute: Column name in gdf of the data that should be plotted.
    :type attribute: str
    :param colors: List of colors to use for the colormap. Default is ['darkgreen', 'magenta'].
    :type colors: list, optional
    :param legend_fmt: Legend text for attribute. Default is attribute + '{:.4f}'.
    :type legend_fmt: str, optional
    :param legend_values: Specific values to use for value steps in legend. Default is None.
    :type legend_values: list, optional
    :param norm_min: Minimum value for normalization. Default is None.
    :type norm_min: float, optional
    :param norm_max: Maximum value for normalization. Default is None.
    :type norm_max: float, optional
    :param query: Query string to filter the data. Default is None.
    :type query: str, optional
    :param marker_style: Style of the markers in the plot. Default is 'o'.
    :type marker_style: str, optional
    :param marker_size_factor: Factor to influence size of the markers in the plot. Default is 1000.0.
    :type marker_size_factor: float, optional
    :param zorder: Determines order of plotting when calling the function multilpe times. Default is None.
    :type zorder: float, optional
    
    :return: patches.
    :rtype: matplotlib.patches.Patch
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    try:
        if ax is None:
            fig, ax = plt.subplots(figsize=(11.7, 8.3))  # A3 size
            logger.debug("{0:s}{1:s}".format(logStr, 'Created new axis.'))

        if gdf is None or gdf.empty:
            logger.debug("{0:s}{1:s}".format(logStr, 'No plot data provided.'))
            return

        # Set default legend_fmt if not provided
        if legend_fmt is None:
            legend_fmt = attribute + ' {:4.0f}'

        # Create Colormap
        cmap = mcolors.LinearSegmentedColormap.from_list('cmap', colors, N=256)
        norm_min = norm_min if norm_min is not None else gdf[attribute].min()
        norm_max = norm_max if norm_max is not None else gdf[attribute].max()
        norm = plt.Normalize(vmin=norm_min, vmax=norm_max)
        logger.debug("{0:s}norm_min: {1:10.2f} norm_max: {2:10.2f}".format(logStr, norm_min, norm_max))

        # Filter and Sort Data if Query is Provided
        df = gdf.query(query) if query else gdf
        df = df.sort_values(by=[attribute], ascending=True)
        
        # Plotting Data with Markers
        sizes = norm(df[attribute].astype(float)) * marker_size_factor  # Scale sizes appropriately
        df.plot(ax=ax,
                marker=marker_style,
                markersize=sizes,
                linestyle='None',  # No lines, only markers
                color=cmap(norm(df[attribute].astype(float))),
                path_effects=[path_effects.Stroke(capstyle="round")],
                zorder=zorder)
        logger.debug("{0:s}{1:s}".format(logStr, f'Plotted {attribute} data.'))

        plt.axis('off')
        # Create Legend Patches
        legend_values = legend_values if legend_values is not None else np.linspace(norm_min, norm_max, num=5)
        logger.debug("{0:s}legend_values: {1}".format(logStr, legend_values))
        patches = [mpatches.Patch(color=cmap(norm(value)), label=legend_fmt.format(value)) for value in legend_values]

        return patches

    except Exception as e:
        logger.error("{0:s}{1:s} - {2}".format(logStr, 'Error.', str(e)))

    logger.debug("{0:s}{1:s}".format(logStr, 'End.'))

# Quellspektren
def mix_colors(vector, colors):
    """
    Mixes colors based on the provided vector.

    :param vector: A vector of weights for the colors.
    :type vector: np.ndarray
    :param colors: An array of colors to be mixed.
    :type colors: np.ndarray
    :return: The mixed color as an integer array.
    :rtype: np.ndarray
    """
    vector = np.array(vector, dtype=float)  # Ensure the vector is of type float
    vector /= vector.sum()  # Normalize the vector so that its elements sum to 1
    colors_array = np.array(colors, dtype=float)  # Ensure the colors are of type float
    mixed_color = np.dot(vector, colors_array)
    return mixed_color.astype(int)

def convert_to_hex(color_array):
    """
    Converts an RGB color array to a hexadecimal color string.

    :param color_array: An array with RGB values.
    :type color_array: np.ndarray
    :return: The hexadecimal color string.
    :rtype: str
    """
    hex_color = "#{:02x}{:02x}{:02x}".format(int(color_array[0]), int(color_array[1]), int(color_array[2]))
    logger.debug(f"Converted color: {hex_color}")
    return hex_color

def plot_src_spectrum(ax=None, gdf=None, attribute=None, colors=None, line_width=2):
    """
    Plots the source spectrum based on the provided GeoDataFrame and attributes.

    :param ax: The axis to plot on. If None, a new axis is created.
    :type ax: matplotlib.axes.Axes, optional
    :param gdf: The GeoDataFrame containing the data to plot.
    :type gdf: geopandas.GeoDataFrame
    :param attribute: The attribute column in the GeoDataFrame to use for color mixing.
    :type attribute: str
    :param colors: The colors to use for mixing.
    :type colors: list of np.ndarray
    :param line_width: The width of the lines in the plot.
    :type line_width: int, optional, default=2
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    try:
        if ax is None:
            fig, ax = plt.subplots(figsize=Rm.DINA3q)  # Adjusted to A3 size
            logger.debug("{0:s}{1:s}".format(logStr, 'Created new axis.'))

        if gdf is None or gdf.empty:
            logger.debug("{0:s}{1:s}".format(logStr, 'No plot data provided.'))
            return

        gdf['mixed_color'] = gdf[attribute].apply(lambda x: mix_colors(x, colors))
        gdf['mixed_color_hex'] = gdf['mixed_color'].apply(lambda x: convert_to_hex(np.array(x).clip(0, 255)))

        for idx, row in gdf.iterrows():
            x, y = row['geometry'].xy
            color = row['mixed_color_hex']
            ax.plot(x, y, color=color, linewidth=line_width)

        # Create a legend for the colors
        legend_handles = []
        for i, color in enumerate(colors):
            color_hex = convert_to_hex(color.clip(0, 255))
            legend_handles.append(plt.Line2D([0], [0], color=color_hex, lw=line_width, label=f"Source {i+1}"))

        ax.legend(handles=legend_handles, loc='best')
        plt.axis('off')

    except Exception as e:
        logger.error("{0:s}{1:s} - {2}".format(logStr, 'Error.', str(e)))