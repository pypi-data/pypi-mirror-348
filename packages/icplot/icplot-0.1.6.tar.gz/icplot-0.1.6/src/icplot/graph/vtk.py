from pathlib import Path

import numpy as np
import vtk
from vtk.util import numpy_support

from iccore.data.units import DateRange
from iccore.data import Series

from .plot_group import PlotGroup


def to_grid(series: Series, dates: DateRange | None):

    if not series.x:
        raise ValueError("Attempting to plot a series with no data")

    if not series.y:
        raise ValueError("Expected 2d series for grid plot.")

    grid = vtk.vtkStructuredGrid()
    grid.SetDimensions([len(series.x.data), len(series.y.data), 1])

    points = vtk.vtkPoints()
    count = 0

    x0 = series.x.data[0]
    for y_pt in series.y.data:
        for x_pt in series.x.data:
            delta_x = x_pt.timestamp() - x0.timestamp()
            points.InsertPoint(count, [delta_x, y_pt, 0])
            count += 1
    grid.SetPoints(points)

    for v in series.values:
        scalars = numpy_support.numpy_to_vtk(
            num_array=np.array(v.data[:]).flatten(order="F"),
            deep=True,
            array_type=vtk.VTK_FLOAT,
        )
        scalars.SetName(v.quantity.name)
        grid.GetPointData().AddArray(scalars)
    return grid


def save(path: Path, config: PlotGroup, series: Series, filename: str = "series"):

    grid = to_grid(series, config.date_range)

    writer = vtk.vtkStructuredGridWriter()
    writer.SetFileName(path / f"{filename}.vtk")
    writer.SetInputData(grid)
    writer.Update()
    writer.Write()
