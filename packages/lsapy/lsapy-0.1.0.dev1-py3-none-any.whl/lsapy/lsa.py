"""Land Suitability definition."""

from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import mapping

from lsapy.criteria import SuitabilityCriteria
from lsapy.statistics import spatial_statistics_summary, statistics_summary

__all__ = ["LandSuitability"]


class LandSuitability:
    def __init__(
        self,
        name: str,
        criteria: dict[str, SuitabilityCriteria],
        short_name: str | None = None,
        long_name: str | None = None,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.criteria = criteria
        self.short_name = short_name
        self.long_name = long_name
        self.description = description

        self._sort_criteria_by_weight()  # important if suitability as limited factor
        self._criteria_name_list = [sc.name for sc in self.criteria.values()]
        self._category_list = list(set([sc.category for sc in self.criteria.values()]))
        self._get_params_by_category()

    def __repr__(self) -> str:
        if hasattr(self, "data"):
            return self.data.__repr__()
        else:
            attrs = []
            for k, v in self.attrs.items():
                if isinstance(v, str):
                    v_ = f"'{v}'"
                else:
                    v_ = v
                attrs.append(f"{k}={v_}")
            return f"{self.__class__.__name__}({', '.join(attrs) if attrs else ''})"

    @property
    def attrs(self):
        return {
            k: v
            for k, v in {
                "name": self.name,
                "criteria": self._criteria_name_list,
                "short_name": self.short_name,
                "long_name": self.long_name,
                "description": self.description,
            }.items()
            if v is not None
        }

    # def __getitem__(self, key: str) -> SuitabilityCriteria:
    #     return self.criteria[key]

    def compute_criteria_suitability(self, inplace: bool | None = False) -> None | xr.Dataset:
        sc_list = []
        for _, sc in self.criteria.items():
            print(f"Computing {sc.name}...")
            if sc.indicator.attrs.get("compute", "") == "done":
                sc_list.append(sc.indicator.rename(sc.name))
            else:
                sc_list.append(sc.compute())
        ls = xr.merge(sc_list, compat="override", combine_attrs="drop")
        for sc in sc_list:
            ls[sc.name].attrs = sc.attrs
        ls.attrs = self.attrs
        if inplace:
            self.data = ls
        else:
            return ls

    def compute_category_suitability(
        self,
        method: str,
        keep_criteria: bool | None = False,
        inplace: bool | None = False,
        limit_var: bool | None = False,
    ) -> xr.Dataset:
        if not hasattr(self, "data"):
            ds = self.compute_criteria_suitability()
        else:
            ds = self.data

        out = []
        out_attrs = []
        for category in self._category_list:
            print(f"Computing {category}...")
            sc_list = [sc for sc in self.criteria.values() if sc.category == category]
            res = _aggregate_vars(
                ds[self._criteria_by_category[category]],
                method=method,
                weights=[sc.weight for sc in sc_list],
                limit_var=limit_var,
            )
            if isinstance(res, xr.Dataset):
                res = res.rename({"limiting_factor": f"{category}", "limiting_var": f"{category}_var"})
            else:
                res = res.rename(f"{category}_suitability")
            res.attrs.update({"long_name": f"{category.capitalize()} Suitability"})
            out.append(res)
            out_attrs.append(res.attrs)
        out = xr.merge(out, compat="override", combine_attrs="drop")
        if keep_criteria:
            out = xr.merge([ds, out], compat="override", combine_attrs="drop")
            for sc in ds.data_vars:  # add attributes of criteria
                out[sc].attrs = ds[sc].attrs
        for i, category in enumerate(self._category_list):  # add attributes of category suitability
            out[f"{category}_suitability"].attrs = out_attrs[i]

        out.attrs.update(self.attrs)
        if inplace:
            self.data = out
        else:
            return out

    def compute_suitability(
        self,
        method: str | dict[str, str] = "mean",
        by_category: bool | None = False,
        keep_all: bool | None = False,
        inplace: bool | None = False,
        limit_var: bool | None = False,
    ) -> xr.Dataset:
        if isinstance(method, str):
            cat_method, suit_method = method, method
        elif isinstance(method, dict):
            cat_method = method.get("category", "mean")
            suit_method = method.get("overall", "mean")
        else:
            raise ValueError("Method must be a string or a dictionary.")

        if not hasattr(self, "data"):
            if by_category:
                ds = self.compute_category_suitability(
                    method=cat_method, keep_criteria=True, inplace=False, limit_var=limit_var
                )
            else:
                ds = self.compute_criteria_suitability(inplace=False)
        else:
            ds = self.data

        if by_category:
            weights = [self.weights_by_category[category] for category in self._category_list]
            on_vars = [f"{category}_suitability" for category in self._category_list]
        else:
            weights = [sc.weight for sc in self.criteria.values()]
            on_vars = self._criteria_name_list

        print("Computing suitability...")
        out = _aggregate_vars(ds[on_vars], method=suit_method, weights=weights, limit_var=limit_var).rename(
            "suitability"
        )
        out.attrs.update({"long_name": "Suitability"})
        out_attrs = out.attrs

        if keep_all:
            out = xr.merge([ds, out], compat="override", combine_attrs="drop")
            for sc in ds.data_vars:  # add attributes of criteria
                out[sc].attrs = ds[sc].attrs
            out["suitability"].attrs = out_attrs

        out.attrs.update(self.attrs)
        if inplace:
            self.data = out
        else:
            return out

    def _sort_criteria_by_weight(self) -> dict[str, SuitabilityCriteria]:
        self.criteria = dict(sorted(self.criteria.items(), key=lambda item: item[1].weight, reverse=True))

    def _get_params_by_category(self):
        self._get_criteria_by_category()
        self._get_weights_by_category()

    def _get_criteria_by_category(self) -> dict[str, list[str]]:
        self._criteria_by_category = {category: [] for category in self._category_list}
        for sc in self.criteria.values():
            self._criteria_by_category[sc.category].append(sc.name)

    def _get_weights_by_category(self) -> dict[str, float | int]:
        self.weights_by_category = {category: [] for category in self._category_list}
        for category in self._category_list:
            self.weights_by_category[category] = sum(
                [sc.weight for sc in self.criteria.values() if sc.category == category]
            )

    def mask(
        self,
        mask: xr.DataArray | gpd.GeoDataFrame,
        inplace: bool | None = False,
        spatial_dims: tuple[str, str] | None = None,
        crs: str | None = None,
        invert: bool = False,
        **kwargs,
    ) -> xr.DataArray | xr.Dataset:
        if not hasattr(self, "data"):
            raise ValueError("Suitability must be computed first.")

        if inplace:
            self.data = _mask_data(self.data, mask, spatial_dims=spatial_dims, crs=crs, invert=invert, **kwargs)
        else:
            return _mask_data(self.data, mask, spatial_dims=spatial_dims, crs=crs, invert=invert, **kwargs)

    def statistics(
        self,
        on_vars: list | None = None,
        on_dims: list | None = None,
        on_dim_values: dict[str, Any] | None = None,
        bins: list | np.ndarray | None = None,
        bins_labels: list | None = None,
        all_bins: bool | None = False,
        cell_area: tuple[float | str, str] | None = None,
        dropna: bool | None = False,
        **kwargs,
    ) -> pd.DataFrame:
        if not hasattr(self, "data"):
            raise ValueError("Suitability must be computed first.")

        return statistics_summary(
            self.data,
            on_vars=on_vars,
            on_dims=on_dims,
            on_dim_values=on_dim_values,
            bins=bins,
            bins_labels=bins_labels,
            all_bins=all_bins,
            cell_area=cell_area,
            dropna=dropna**kwargs,
        )

    def spatial_statistics(
        self,
        areas: gpd.GeoDataFrame,
        name: str | None = "area",
        on_vars: list | None = None,
        on_dims: list | None = None,
        on_dim_values: dict[str, Any] | None = None,
        bins: np.ndarray | None = None,
        all_bins: bool | None = False,
        cell_area: tuple[float | str, str] | None = None,
        mask_kwargs: dict = None,
        stats_kwargs: dict = None,
    ) -> pd.DataFrame:
        if not hasattr(self, "data"):
            raise ValueError("Suitability must be computed first.")

        return spatial_statistics_summary(
            self.data,
            areas,
            name=name,
            on_vars=on_vars,
            on_dims=on_dims,
            on_dim_values=on_dim_values,
            bins=bins,
            all_bins=all_bins,
            cell_area=cell_area,
            mask_kwargs=mask_kwargs,
            stats_kwargs=stats_kwargs,
        )


def _mask_data(
    data: xr.DataArray | xr.Dataset,
    mask: xr.DataArray | gpd.GeoDataFrame,
    spatial_dims: tuple[str, str] | None = None,
    crs: str | None = None,
    invert: bool = False,
    **kwargs,
) -> xr.DataArray | xr.Dataset:
    if isinstance(mask, gpd.GeoDataFrame):
        mask = mask.to_crs(crs)
        data = data.rio.set_spatial_dims(*spatial_dims).rio.write_crs(crs)
        return data.rio.clip(mask.geometry.apply(mapping), invert=invert, **kwargs)
    elif isinstance(mask, xr.DataArray):
        if invert:
            mask = ~mask
        return data.where(mask, **kwargs)
    else:
        raise ValueError("mask must be a GeoDataFrame or DataArray")


####################################################################################################
# VARIABLES AGGREGATION FUNCTIONS
####################################################################################################


def vars_weighted_mean(ds: xr.Dataset, vars=None, weights=None) -> xr.DataArray:
    if vars is None:
        vars = list(ds.data_vars)
    if weights is None:
        weights = np.ones(len(vars))

    s = sum([ds[v] * w for v, w in zip(vars, weights, strict=False)])
    da: xr.DataArray = s / sum(weights)
    return da.assign_attrs(
        {
            "method": "Weighted Mean",
            "descritpion": (
                "Weighted Mean of variables: "
                f"{', '.join([f'{v} ({w})' for v, w in zip(vars, weights, strict=False)])}."
            )
        }
    ).rename("weighted_mean")


def vars_mean(ds: xr.Dataset, vars=None) -> xr.DataArray:
    if vars is None:
        vars = list(ds.data_vars)
    da = vars_weighted_mean(ds, vars=vars)
    return da.assign_attrs({"method": "Mean", "description": f"Mean of variables: {', '.join(vars)}."}).rename("mean")


def vars_weighted_geomean(ds: xr.Dataset, vars=None, weights=None) -> xr.DataArray:
    if vars is None:
        vars = list(ds.data_vars)
    if weights is None:
        weights = np.ones(len(vars))

    s = sum([np.log(ds[v]) * w for v, w in zip(vars, weights, strict=False)])
    da: xr.DataArray = np.exp(s / sum(weights))
    return da.assign_attrs(
        {
            "method": "Weighted Geometric Mean",
            "description": (
                "Weighted Geometric Mean of variables: "
                f"{', '.join([f'{v} ({w})' for v, w in zip(vars, weights, strict=False)])}."
            )
        }
    ).rename("weighted_geometric_mean")


def vars_geomean(ds: xr.Dataset, vars=None) -> xr.DataArray:
    if vars is None:
        vars = list(ds.data_vars)
    da = vars_weighted_geomean(ds, vars=vars)
    return da.assign_attrs(
        {"method": "Geometric Mean", "description": f"Geometric Mean of variables: {', '.join(vars)}."}
    ).rename("geometric_mean")


def limiting_factor(ds: xr.Dataset, vars=None, limiting_var: bool | None = True) -> xr.DataArray | xr.Dataset:
    if vars is None:
        vars = list(ds.data_vars)

    da = ds[vars].to_array()
    mask = da.notnull().all(dim="variable")

    lim = da.min(dim="variable", skipna=True).where(mask).rename("limiting_factor")
    lim = lim.assign_attrs(
        {"method": "Limiting Factor", "description": f"Value of limiting factor among variables: {', '.join(vars)}."}
    )
    if limiting_var:
        lim_var = da.fillna(9999).argmin(dim="variable", skipna=True).where(mask).rename("limiting_var")
        lim_var.attrs = {
            "method": "Limiting Factor",
            "description": f"Limiting factor among: {', '.join(vars)}.",
            "legend": {f"{i}": v for i, v in enumerate(vars)},
        }
        return xr.merge([lim, lim_var])
    return lim.to_dataset()


def _aggregate_vars(
    ds: xr.Dataset, method: str = "mean", vars=None, weights=None, **kwargs
) -> xr.DataArray | xr.Dataset:
    if method.lower() == "mean":
        return vars_mean(ds, vars=vars)
    elif method.lower() == "weighted_mean":
        return vars_weighted_mean(ds, vars=vars, weights=weights)
    elif method.lower() == "geomean":
        return vars_geomean(ds, vars=vars)
    elif method.lower() == "weighted_geomean":
        return vars_weighted_geomean(ds, vars=vars, weights=weights)
    elif method.lower() == "limit_factor":
        return limiting_factor(ds, vars=vars, **kwargs)
    else:
        raise ValueError(f"Method '{method}' not recognized.")
