import importlib.util
from typing import List, Union

import numpy as np

from oafuncs.oa_tool import PEx

# 检查pyinterp是否可用
pyinterp_available = importlib.util.find_spec("pyinterp") is not None

if pyinterp_available:
    import pyinterp
    import pyinterp.backends.xarray as pyxr
    import xarray as xr


def _fill_nan_with_nearest(data: np.ndarray, source_lons: np.ndarray, source_lats: np.ndarray) -> np.ndarray:
    """
    使用最近邻方法填充NaN值，适合地理数据。
    """
    if not np.isnan(data).any():
        return data

    # 创建掩码，区分有效值和NaN值
    mask = ~np.isnan(data)
    if not np.any(mask):
        return data  # 全是NaN，无法填充

    # 使用pyinterp的RTree进行最近邻插值填充NaN
    try:
        if not pyinterp_available:
            raise ImportError("pyinterp not available")

        # 获取有效数据点的位置和值
        valid_points = np.column_stack((source_lons[mask].ravel(), source_lats[mask].ravel()))
        valid_values = data[mask].ravel()

        # 创建RTree
        tree = pyinterp.RTree()
        tree.insert(valid_points.astype(np.float64), valid_values.astype(np.float64))

        # 获取所有点的坐标
        all_points = np.column_stack((source_lons.ravel(), source_lats.ravel()))

        # 最近邻插值
        filled_values = tree.query(all_points[:, 0], all_points[:, 1], k=1)

        return filled_values.reshape(data.shape)

    except Exception:
        # 备选方案：使用scipy的最近邻
        from scipy.interpolate import NearestNDInterpolator

        points = np.column_stack((source_lons[mask].ravel(), source_lats[mask].ravel()))
        values = data[mask].ravel()

        if len(values) > 0:
            interp = NearestNDInterpolator(points, values)
            return interp(source_lons.ravel(), source_lats.ravel()).reshape(data.shape)
        else:
            return data  # 无有效值可用于填充


def _interp_single_worker(*args):
    """
    单slice插值worker，只使用pyinterp的bicubic方法，失败直接报错。
    参数: data_slice, source_lons, source_lats, target_lons, target_lats
    """
    if not pyinterp_available:
        raise ImportError("pyinterp package is required for geographic interpolation")

    data_slice, source_lons, source_lats, target_lons, target_lats = args

    # 预处理：填充NaN值以确保数据完整
    if np.isnan(data_slice).any():
        data_filled = _fill_nan_with_nearest(data_slice, source_lons, source_lats)
    else:
        data_filled = data_slice

    # 创建xarray DataArray
    da = xr.DataArray(
        data_filled,
        coords={"latitude": source_lats, "longitude": source_lons},
        dims=("latitude", "longitude"),
    )

    # 创建Grid2D对象
    grid = pyxr.Grid2D(da)

    # 使用bicubic方法插值
    result = grid.bicubic(coords={"longitude": target_lons.ravel(), "latitude": target_lats.ravel()}, bounds_error=False, num_threads=1).reshape(target_lons.shape)

    return result


def interp_2d_func_geo(
    target_x_coordinates: Union[np.ndarray, List[float]],
    target_y_coordinates: Union[np.ndarray, List[float]],
    source_x_coordinates: Union[np.ndarray, List[float]],
    source_y_coordinates: Union[np.ndarray, List[float]],
    source_data: np.ndarray,
) -> np.ndarray:
    """
    使用pyinterp进行地理插值，只使用bicubic方法。

    Args:
        target_x_coordinates: 目标点经度 (-180 to 180 或 0 to 360)
        target_y_coordinates: 目标点纬度 (-90 to 90)
        source_x_coordinates: 源数据经度 (-180 to 180 或 0 to 360)
        source_y_coordinates: 源数据纬度 (-90 to 90)
        source_data: 多维数组，最后两个维度为空间维度

    Returns:
        np.ndarray: 插值后的数据数组
    """
    if not pyinterp_available:
        raise ImportError("pyinterp package is required for geographic interpolation")

    # 验证纬度范围
    if np.nanmin(target_y_coordinates) < -90 or np.nanmax(target_y_coordinates) > 90:
        raise ValueError("Target latitude must be in range [-90, 90].")
    if np.nanmin(source_y_coordinates) < -90 or np.nanmax(source_y_coordinates) > 90:
        raise ValueError("Source latitude must be in range [-90, 90].")

    # 确保使用numpy数组
    source_x_coordinates = np.array(source_x_coordinates)
    source_y_coordinates = np.array(source_y_coordinates)
    target_x_coordinates = np.array(target_x_coordinates)
    target_y_coordinates = np.array(target_y_coordinates)

    # 创建网格坐标（如果是一维的）
    if source_x_coordinates.ndim == 1:
        source_x_coordinates, source_y_coordinates = np.meshgrid(source_x_coordinates, source_y_coordinates)
    if target_x_coordinates.ndim == 1:
        target_x_coordinates, target_y_coordinates = np.meshgrid(target_x_coordinates, target_y_coordinates)

    # 验证源数据形状
    if source_x_coordinates.shape != source_data.shape[-2:] or source_y_coordinates.shape != source_data.shape[-2:]:
        raise ValueError("Shape of source_data does not match shape of source_x_coordinates or source_y_coordinates.")

    # 处理多维数据
    data_dims = source_data.ndim
    if data_dims < 2:
        raise ValueError(f"Source data must have at least 2 dimensions, but got {data_dims}.")
    elif data_dims > 4:
        raise ValueError(f"Source data has {data_dims} dimensions, but this function currently supports up to 4.")

    # 扩展到4D
    num_dims_to_add = 4 - data_dims
    source_data = source_data.reshape((1,) * num_dims_to_add + source_data.shape)
    t, z, y, x = source_data.shape

    # 准备并行处理参数
    params = []
    for t_index in range(t):
        for z_index in range(z):
            params.append(
                (
                    source_data[t_index, z_index],
                    source_x_coordinates[0, :],  # 假设经度在每行都相同
                    source_y_coordinates[:, 0],  # 假设纬度在每列都相同
                    target_x_coordinates,
                    target_y_coordinates,
                )
            )

    # 并行执行插值
    with PEx() as executor:
        results = executor.run(_interp_single_worker, params)

    # 还原到原始维度
    return np.squeeze(np.array(results).reshape((t, z) + target_x_coordinates.shape))
