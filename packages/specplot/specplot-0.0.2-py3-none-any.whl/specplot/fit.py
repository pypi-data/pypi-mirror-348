import numpy as np
from lmfit.models import LinearModel
import matplotlib.pyplot as plt


def get_spectral_calibration(
    spectral_lines,
    NIST_spectral_lines=None,
    model=LinearModel(),
    unit="nm",
    show=False,
    savepath=None,
):
    """Calculate spectral lamp calibration using a linear function

    Args:
        spectral_lines (list): measured spectral lines to calibrate
        NIST_spectral_lines (list, optional): spectral lines from literature. Defaults to None.
        model (str, optional): lmfit model for calibration fitting. Defaults to LinearModel().
        unit (str, optional): Unit to display in the plot. Defaults to "nm".
        show (bool, optional): show plot after fitting. Defaults to False.
        savepath (str, optional): save plot after fitting. Defaults to None.

    Returns:
        lmfit model, lmfit parameters: Returns the used lmfit model and fitted parameters of the calibration
    """

    p0s = model.guess(NIST_spectral_lines, x=spectral_lines)
    out = model.fit(NIST_spectral_lines, x=spectral_lines, params=p0s)
    x_fine = np.linspace(
        min(spectral_lines),
        max(spectral_lines),
        endpoint=True,
        num=1000,
    )
    y_fine = model.eval(out.params, x=x_fine)
    plt.plot(spectral_lines, NIST_spectral_lines, "x")
    plt.plot(
        x_fine,
        y_fine,
    )
    plt.xlabel(f"Measured spectral line positions [{unit}]")
    plt.ylabel(f"NIST spectral line positions [{unit}]")
    if savepath is not None:
        plt.savefig(savepath, bbox_inches="tight")
    if show:
        plt.show()
    plt.close("all")

    print(out.fit_report())

    return model, out.params


def calculate_calibration(x, model, params):
    """Calculate calibrated x value from fitted model of get_spectral_calibration

    Args:
        x (list): axis that needs to be calibrated
        model (lmfit model): lmfit model of get_spectral_calibration
        params (lmfit parameters): lmfit parameters of get_spectral_calibration

    Returns:
        np.ndarray: array of calibrated values
    """
    return model.eval(params, x=x)
