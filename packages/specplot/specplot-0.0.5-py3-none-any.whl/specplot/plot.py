from .helper import get_current_dir_path
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

cmap_fepydas = LinearSegmentedColormap.from_list(
    "fepydas",
    ["black", "red", "orange", "yellow", "green", "blue", "white"],
    1000,  # see https://pypi.org/project/fepydas/
)


def plot_xy(
    x,
    y,
    title=None,
    xlabel="Wavelength [nm]",
    ylabel="Counts [#]",
    scale_norm="linear",
    name="xy_plot",
    show=False,
    save=True,
    savepath=get_current_dir_path(),
    savetype="pdf",
    **kwargs,
):
    """XY plot using matplotlib

    Args:
        x (list): x value list or nested list
        y (list): y value list or nested list
        title (str, optional): title of the plot. Defaults to None.
        xlabel (str, optional): xlabel of the plot. Defaults to "Wavelength [nm]".
        ylabel (str, optional): ylabel of the plot. Defaults to "Counts [#]".
        scale_norm (str, optional): scale norm of the plot (e.g. 'linear' or 'log'). Defaults to "linear".
        name (str, optional): name of the saved file. Defaults to "xy_plot".
        show (bool, optional): show plot after fitting. Defaults to False.
        save (bool, optional): save plot after fitting. Defaults to True.
        savepath (str, optional): save path of the plot after fitting. Defaults to get_current_dir_path().
        savetype (str, optional): filetype of the save. Defaults to "pdf".
    """
    xnested = isinstance(x[0], (list, tuple, np.ndarray))
    ynested = isinstance(y[0], (list, tuple, np.ndarray))
    if xnested and ynested:
        for i in range(len(y)):
            plt.plot(x[i], y[i], **kwargs)
    elif not xnested and ynested:
        for i in range(len(y)):
            plt.plot(x, y[i], **kwargs)
    else:
        plt.plot(x, y, **kwargs)

    plt.yscale(scale_norm)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)

    if save:
        plt.savefig(join(savepath, f"{name}.{savetype}"), bbox_inches="tight")
    if show:
        plt.show()

    plt.close("all")


def plot_xyz(
    x,
    y,
    z,
    cmap=cmap_fepydas,
    title=None,
    xlabel="Wavelength [nm]",
    ylabel="Temperature [K]",
    scale_norm="linear",
    name="xyz_plot",
    show=False,
    save=True,
    savepath=get_current_dir_path(),
    savetype="pdf",
    **kwargs,
):
    """XYZ plot using matplotlib pcolor

    Args:
        x (list): x value list
        y (list): y value list
        z (list): z value nested list
        cmap (_type_, optional): colormap of the xyz plot. Defaults to cmap_fepydas.
        title (str, optional): title of the plot. Defaults to None.
        xlabel (str, optional): xlabel of the plot. Defaults to "Wavelength [nm]".
        ylabel (str, optional): ylabel of the plot. Defaults to "Temperature [K]".
        scale_norm (str, optional): scale norm of the plot (e.g. 'linear' or 'log'). Defaults to "linear".
        name (str, optional): name of the saved file. Defaults to "xyz_plot".
        show (bool, optional): show plot after fitting. Defaults to False.
        save (bool, optional): save plot after fitting. Defaults to True.
        savepath (str, optional): save path of the plot after fitting. Defaults to get_current_dir_path().
        savetype (str, optional): filetype of the save. Defaults to "pdf".
    """
    plt.pcolor(x, y, z, cmap=cmap, norm=scale_norm, **kwargs)

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)

    if save:
        plt.savefig(join(savepath, f"{name}.{savetype}"), bbox_inches="tight")
    if show:
        plt.show()

    plt.close("all")
