from .helper import get_current_dir_path
from os.path import join
import numpy as np
from lmfit.models import LinearModel
import matplotlib.pyplot as plt


class Calibration:
    def __init__(self, spectral_lines, NIST_spectral_lines, **kwargs):
        self.get_spectral_calibration(spectral_lines, NIST_spectral_lines, **kwargs)

    def get_spectral_calibration(
        self,
        spectral_lines,
        NIST_spectral_lines,
        model=LinearModel(),
        name="calibration",
        unit="nm",
        show=False,
        save=True,
        savepath=get_current_dir_path(),
    ):
        """Calculate spectral lamp calibration using a linear function. Stores the lmfit fitted parameters additionally in self.fitted_p0s.

        Args:
            spectral_lines (list): measured spectral lines to calibrate
            NIST_spectral_lines (list): spectral lines from literature
            model (str, optional): lmfit model for calibration fitting. Defaults to LinearModel().
            name (str, optional): name of the saved file. Defaults to "calibration".
            unit (str, optional): Unit to display in the plot. Defaults to "nm".
            show (bool, optional): show plot after fitting. Defaults to False.
            save (bool, optional): save plot after fitting. Defaults to True
            savepath (str, optional): save path of the plot after fitting. Defaults to current script directory.

        Returns:
            lmfit model, lmfit parameters: Returns the used lmfit model and fitted parameters of the calibration
        """

        self.spectral_lines = spectral_lines
        self.NIST_spectral_lines = NIST_spectral_lines
        self.model = model
        self.unit = unit

        p0s = model.guess(NIST_spectral_lines, x=spectral_lines)
        out = model.fit(NIST_spectral_lines, x=spectral_lines, params=p0s)

        self.fitted_p0s = out.params

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

        if save:
            plt.savefig(join(savepath, f"{name}.pdf"), bbox_inches="tight")
        if show:
            plt.show()

        plt.close("all")

        print(out.fit_report())

        return model, out.params

    def calculate_calibration(self, x, model=None, params=None):
        """Calculate calibrated x value from fitted model of get_spectral_calibration

        Args:
            x (list): axis that needs to be calibrated
            model (lmfit model): lmfit model of get_spectral_calibration
            params (lmfit parameters): lmfit parameters of get_spectral_calibration

        Returns:
            np.ndarray: array of calibrated values
        """
        if model is None:
            model = self.model
        if params is None:
            params = self.fitted_p0s

        return model.eval(params, x=x)
