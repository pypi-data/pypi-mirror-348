# !/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT
# Copyright (c) 2024, Fiore J.Manuel.
# All rights reserved.

"""Provides the functions to read and extract the info from .tiff files."""

# =============================================================================
# IMPORTS
# =============================================================================
import numpy as np
import pandas as pd
import rasterio
import cv2
import os
import json
from shapely.geometry import MultiPolygon, Polygon
from rasterio import mask
from Pynomic.core import core
import re
from PIL import Image
import zarr
import io
import pandas_geojson as pdg
import geopandas as gdp
import shapely

# =============================================================================
# FUNCTIONS
# =============================================================================


def _read_grid(gpath, col_id: str):
    """Reads a geojson file.

    Args:
        gpath: grid path to a geojson file.

    Returns
    -------
        coordinate system of the grid.
        dict-like object with id and coords of each plot.
    """
    dics = {}
    if gpath.split(".")[1] == "geojson":
        plotgrids = open(gpath)
        plotgrids = json.load(plotgrids)
        crs_coords = plotgrids["crs"]["properties"]["name"]

        for p in plotgrids["features"]:
            dics[str(p["properties"][col_id])] = p["geometry"]["coordinates"][
                0
            ]

        return crs_coords, dics

    else:
        raise ValueError("Grid is not a geojson file")


def _read_grid2(gpath, col_id: str):
    """Reads a geojson and shape files.

    Parameters
    ----------
        gpath:str
            grid path to a geojson or shape file.

    Returns
    -------
        geodataframe form the grid.
        dict-like object with id and coords of each plot.
    """
    df = gdp.read_file(gpath)
    df[col_id] = df[col_id].astype(str)
    geodf = df.copy()
    poligons_dict = df.copy().set_index(col_id).loc[:, "geometry"].to_dict()

    return geodf, poligons_dict


def _read_grids(gpath, col_id: str):
    """Reads a geojson file or shape file.

    Parameters
    ----------
        gpath:str
            grid path to a geojson file.

    Returns
    -------
        coordinate system of the grid.
        dict-like object with id and coords of each plot.
    """
    data = gdp.read_file(gpath)
    data_dic = data.loc[:, [col_id, "geometry"]].copy().to_dict(index=False)


def _get_dataframe_from_json(path_gjson):
    data = pdg.read_geojson(path_gjson)
    collist = data.get_properties()
    dfg = data.to_dataframe()
    keep = []
    for c in dfg.columns:
        for m in collist:
            if len(c.split("." + m)) > 1:
                keep.append(c)
    dfa = dfg.loc[:, keep].copy()
    dfa.columns = collist
    return dfa


def _get_tiff_files(fold_path):
    """Makes a list of tiff files of a folder path.

    Parameters
    ----------
        fold_path:str
            folder path with the tiff files.

    Returns
    -------
        list
    """
    tiff_list = []
    for file in os.listdir(fold_path):

        if os.path.basename(file).split(".", 1)[1] == "tif":
            tiff_list.append(file)

    return tiff_list


def auto_fit_image(mtx, hbuffer=2, wbuffer=2):
    """Takes an array and returns the crooping and angle parameters.

    Parameters
    ----------
        mtx:np.array
        hbuffer:int
            height buffer
        wbuffer:int
            with buffer

    Returns
    -------
        tuple with croping parameters. Angle value.
    """
    gray = np.where(mtx <= 0, mtx, 255)

    gray = np.uint8(np.where(gray > 0, gray, 0))
    gray = np.array(gray)

    # edges = cv2.Canny(gray,150,150*2)

    contours, hierarchy = cv2.findContours(
        gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    rect = cv2.minAreaRect(contours[-1])

    if rect[1][0] < rect[1][1]:
        angle = rect[2]
        gry = np.array(Image.fromarray(gray).rotate(angle, expand=True))
    else:
        angle = rect[2] + 90
        gry = np.array(Image.fromarray(gray).rotate(angle, expand=True))

    blur = cv2.GaussianBlur(gry, (3, 3), 0)
    th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    coords = cv2.findNonZero(th)
    x, y, w, h = cv2.boundingRect(coords)

    h1 = y + hbuffer
    h2 = y + (h - hbuffer)
    w1 = x + wbuffer
    w2 = x + (w - wbuffer)
    return (h1, h2, w1, w2), angle


def _extract_bands_from_raster(raster_data, multiplot, alpha_idx=-1):
    """Separates the bands for the maks.

    Parameters
    ----------
        raster_data:np.array
            a masked area of intrest(aoi).
        multiplot:Multiplot
            a multiplot obj form sapely.

    Returns
    -------
        list with the bands array and an array from the mask.
    """
    masked_rast, aff = rasterio.mask.mask(
        raster_data, multiplot.geoms, crop=True
    )

    if alpha_idx == -1:
        true_bands = masked_rast.copy()
        masked_band = masked_rast[-1]
    else:
        true_bands = list(masked_rast)
        masked_band = true_bands.pop(alpha_idx)

    return true_bands, masked_band


def extract_raster_data(raster_path, grid_path, col_id: str, bands_n=None):
    """Extracts the values from the raster file segregating each band and plot.

    Parameters
    ----------
        raster_path:str
            path to raster file.
        grid_path:str
            path to gird.
        bands_n:list
            a list of the bands names and order.

    Returns
    -------
        dict with array of each band and plot.
        DataFrame with date, mean band for each plot.
        list bands name.
    """
    geodf, grids = _read_grid2(grid_path, col_id)
    bands_mean = []
    array_dict = {}
    bands_name = []
    with rasterio.open(raster_path) as src:
        for pos, g in enumerate(grids.keys()):
            if int(pos) == 0:
                coords = src.meta["crs"]
                print(f"Raster Coords system: {coords}")
                print(f"Grid Coords system: {geodf.crs}")

            # Check if contains alpha band
            contains_alpha_band = -1
            for idx, interp in enumerate(src.colorinterp, start=1):
                if interp == rasterio.enums.ColorInterp.alpha:
                    contains_alpha_band = idx - 1

            if grids[g].geom_type == "MultiPolygon":
                figure = grids[g]
            else:
                figure = MultiPolygon([grids[g]])

            if contains_alpha_band != -1:
                # Diferentiate the true bands form the mask band.
                true_bands, masked_band = _extract_bands_from_raster(
                    src, figure, contains_alpha_band
                )
            else:
                # Returns the las band for fiting.
                true_bands, masked_band = _extract_bands_from_raster(
                    src, figure
                )

            # Get the fitting parameters.
            cpv, rangle = auto_fit_image(masked_band)

            # Enumerate the bands and name them.
            if bands_n:
                bands_name = bands_n
            else:
                n_band = np.array(range(0, len(true_bands))) + 1
                bands_name = ["band" + "_" + str(x) for x in n_band]

            # Fit the bands array with the parameters.
            fitted_bands = [
                np.array(Image.fromarray(band).rotate(rangle, expand=True))[
                    cpv[0] : cpv[1], cpv[2] : cpv[3]
                ]
                for band in true_bands
            ]

            # Save the mean for each band
            plot_fitted_bands = [
                np.mean(band.astype(float)) for band in fitted_bands
            ]
            mp_bands = []
            # Numerical id for project.
            id_str = "A" + str(pos + 1)
            mp_bands.append(id_str)
            # Original id from the grid can be numerical or text or both.
            mp_bands.append(g)
            # gets the date
            mp_bands.append(os.path.basename(raster_path).split("_")[0])
            for band in plot_fitted_bands:
                mp_bands.append(band)
            bands_mean.append(mp_bands)

            # Save the values in a dictionary.
            array_dict[pos + 1] = dict(zip(bands_name, fitted_bands))

    df1 = pd.DataFrame(bands_mean, columns=["id", col_id, "date", *bands_name])
    geodat = geodf
    geodat[col_id] = geodat[col_id].astype(str)

    df = geodat.merge(df1, on=col_id)
    df = df.loc[
        :, [*df1.columns.values, *geodat.drop(columns=col_id).columns.values]
    ]
    return array_dict, bands_name, df


def process_stack_tiff(folder_path, grid_path, col_id: str, bands_n=None):
    """Process all the .tiff files in a folder.

    Parameters
    ----------
        folder_path:str
            folder that contains the .tiff files.
        grid_path:str
            path of the geojson grid.
        col_id:str
            unique column name identifier from the grid.
        bands_n:str
            list like with the bands names ordered.


    Returns
    -------
        PynomicsProject object.
    """
    tif_list = _get_tiff_files(folder_path)
    raw_data = zarr.group()
    raw_data.create_group("dates")
    dates = []
    ldata = []
    date_key = ""
    for tiff_pos, tiff_file in enumerate(tif_list):
        print(f"{tiff_pos + 1}/{len(tif_list)} : {tiff_file}")
        if re.search(r"_", tiff_file):
            date_key = tiff_file.split("_")[0]
            dates.append(date_key)

        to_raw_data, bands_n, ldata_bands = extract_raster_data(
            folder_path + "/" + tiff_file, grid_path, col_id, bands_n
        )

        raw_data["dates"].create_group(date_key)

        for plot_id in to_raw_data.keys():
            c = "A" + str(plot_id)
            raw_data["dates"][date_key].create_group(c)
            for band in to_raw_data[plot_id].keys():
                raw_data["dates"][date_key][c].create_group(band)
                raw_data["dates"][date_key][c][band] = to_raw_data[plot_id][
                    band
                ]
        # ldata_bands = ldata_bands.reset_index().drop(columns= 'index', axis = 1)
        ldata.append(ldata_bands)

    df_data = pd.concat(ldata, axis=0).reset_index().drop(columns="index")

    return core.Pynomicproject(
        raw_data=raw_data,
        ldata=df_data,
        dates=dates,
        n_dates=len(dates),
        bands_name=bands_n,
        n_bands=len(bands_n),
    )


def read_zarr(path):
    """Reads a zarr project previously saved from pynomics.

    Parameters
    ----------
        path:str
            a path to the directory
    Returns
    -------
        Pynomicproject object
    """
    store = zarr.open_group(path + "/" + "raw_data", mode="a")

    data1 = gdp.read_file(path + "/" + "ldata.shp")

    with open(path + "/" + "obj_properties.json", "r") as file:
        prop = dict(json.load(file))

    return core.Pynomicproject(
        raw_data=store,
        ldata=data1.copy(),
        n_dates=len(prop["dates"]),
        dates=prop["dates"],
        n_bands=len(prop["bands"]),
        bands_name=prop["bands"],
    )
