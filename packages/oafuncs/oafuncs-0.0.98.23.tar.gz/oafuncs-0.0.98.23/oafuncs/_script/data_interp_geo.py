from typing import List, Union

import numpy as np
import importlib.util

from oafuncs.oa_tool import PEx

# 检查pyinterp是否可用
pyinterp_available = importlib.util.find_spec("pyinterp") is not None

# 仅在pyinterp可用时导入相关模块
if pyinterp_available:
    import pyinterp
    from pyinterp.interpolator import RegularGridInterpolator, RTree


def _interp_single_worker(*args):
    """
    用于PEx并行的单slice插值worker。
    参数: data_slice, origin_points, target_points, interpolation_method, target_shape, source_xy_shape
    使用pyinterp进行地理插值
    """
    # 确保pyinterp可用
    if not pyinterp_available:
        raise ImportError("pyinterp package is required for geographic interpolation")
        
    data_slice, origin_points, target_points, interpolation_method, target_shape, source_xy_shape = args

    # 处理无效数据点
    valid_mask = ~np.isnan(data_slice.ravel())
    if np.count_nonzero(valid_mask) < 10:
        return np.full(target_shape, np.nanmean(data_slice))

    # 准备有效数据点
    valid_data = data_slice.ravel()[valid_mask]
    valid_points = origin_points[valid_mask]

    # 根据插值方法选择合适的策略
    if origin_points.shape[0] == source_xy_shape[0] * source_xy_shape[1]:  # 规则网格
        try:
            # 尝试使用规则网格插值
            y_size, x_size = source_xy_shape
            lons = origin_points[:, 0].reshape(y_size, x_size)[0, :]
            lats = origin_points[:, 1].reshape(y_size, x_size)[:, 0]

            # 检查网格数据的有效性
            grid_data = data_slice.reshape(source_xy_shape)
            nan_ratio = np.isnan(grid_data).sum() / grid_data.size
            if nan_ratio > 0.5:  # 如果超过50%是NaN，跳过规则网格插值
                raise ValueError("Too many NaN values in grid data")

            # 创建pyinterp网格 - 设置经度循环
            is_global = np.abs((lons[-1] - lons[0]) % 360 - 360) < 1e-6
            grid = pyinterp.Grid2D(
                x=pyinterp.Axis(lons, is_circle=is_global),  # 根据数据判断是否为全球网格
                y=pyinterp.Axis(lats),
                array=grid_data,
                increasing_axes=(-2, -1),  # 确保坐标轴方向正确
            )

            # 创建插值器并执行插值
            method_map = {"bilinear": "bilinear", "linear": "bilinear", "cubic": "bicubic", "nearest": "nearest"}
            interpolator = RegularGridInterpolator(grid, method=method_map.get(interpolation_method, "bilinear"))

            # 执行插值 - 使用geodetic坐标系统确保正确处理地球曲率
            coords = pyinterp.geodetic.Coordinates(target_points[:, 0], target_points[:, 1], pyinterp.geodetic.System.WGS84)

            result = interpolator.interpolate(coords).reshape(target_shape)

            # 如果规则网格插值没有产生太多NaN值，直接返回结果
            if np.isnan(result).sum() / result.size < 0.05:
                return result

        except Exception:  # noqa
            # 失败时使用RTree插值
            pass

    # 使用RTree进行非规则网格插值或填补规则网格产生的NaN
    try:
        # 创建RTree插值器
        mesh = RTree(pyinterp.geodetic.Coordinates(valid_points[:, 0], valid_points[:, 1], pyinterp.geodetic.System.WGS84), valid_data)

        # 根据插值方法和有效点数量选择合适的插值策略
        coords = pyinterp.geodetic.Coordinates(target_points[:, 0], target_points[:, 1], pyinterp.geodetic.System.WGS84)

        if interpolation_method in ["cubic", "quintic"] and len(valid_data) > 100:
            # 对于点数充足的情况，高阶插值使用径向基函数
            result = mesh.radial_basis_function(
                coords,
                function="thin_plate",  # 薄板样条，适合地理数据
                epsilon=0.1,  # 平滑参数
                norm="geodetic",  # 使用地理距离
                within=False,  # 允许外推
            ).reshape(target_shape)
        else:
            # 使用IDW，动态调整k值
            k_value = max(min(int(np.sqrt(len(valid_data))), 16), 4)  # 自适应近邻点数
            result, _ = mesh.inverse_distance_weighting(
                coords,
                k=k_value,
                p=2.0,  # 平方反比权重
                within=False,  # 允许外推
            ).reshape(target_shape)

        # 检查插值结果，如果有NaN，尝试使用最近邻补充
        if np.isnan(result).any():
            nan_mask = np.isnan(result)
            nan_coords = pyinterp.geodetic.Coordinates(target_points[nan_mask.ravel(), 0], target_points[nan_mask.ravel(), 1], pyinterp.geodetic.System.WGS84)
            nn_values, _ = mesh.k_nearest(nan_coords, k=1)
            result[nan_mask] = nn_values

    except Exception:
        # 如果所有复杂插值方法都失败，使用最基本的最近邻
        try:
            # 创建新的RTree对象尝试避免之前可能的问题
            simple_mesh = RTree(pyinterp.geodetic.Coordinates(valid_points[:, 0], valid_points[:, 1], pyinterp.geodetic.System.WGS84), valid_data)

            simple_coords = pyinterp.geodetic.Coordinates(target_points[:, 0], target_points[:, 1], pyinterp.geodetic.System.WGS84)

            result, _ = simple_mesh.k_nearest(simple_coords, k=1).reshape(target_shape)
        except Exception:
            # 极端情况下，使用平均值填充
            result = np.full(target_shape, np.nanmean(valid_data))

    return result


def interp_2d_func_geo(target_x_coordinates: Union[np.ndarray, List[float]], target_y_coordinates: Union[np.ndarray, List[float]], source_x_coordinates: Union[np.ndarray, List[float]], source_y_coordinates: Union[np.ndarray, List[float]], source_data: np.ndarray, interpolation_method: str = "cubic") -> np.ndarray:
    """
    使用pyinterp进行地理插值，适用于全球尺度的地理数据与区域数据。

    特点:
    - 正确处理经度跨越日期线的情况
    - 自动选择最佳插值策略
    - 处理规则网格和非规则数据
    - 支持多维数据并行处理

    Args:
        target_x_coordinates: 目标点经度 (-180 to 180 或 0 to 360)
        target_y_coordinates: 目标点纬度 (-90 to 90)
        source_x_coordinates: 源数据经度 (-180 to 180 或 0 to 360)
        source_y_coordinates: 源数据纬度 (-90 to 90)
        source_data: 多维数组，最后两个维度为空间维度
        interpolation_method: 插值方法:
            - 'nearest': 最近邻插值
            - 'linear'/'bilinear': 双线性插值
            - 'cubic': 三次样条插值
            - 'quintic': 五次样条插值

    Returns:
        np.ndarray: 插值后的数据数组

    Examples:
        >>> # 全球数据插值示例
        >>> target_lon = np.arange(-180, 181, 1)
        >>> target_lat = np.arange(-90, 91, 1)
        >>> source_lon = np.arange(-180, 181, 5)
        >>> source_lat = np.arange(-90, 91, 5)
        >>> source_data = np.cos(np.deg2rad(source_lat.reshape(-1, 1))) * np.cos(np.deg2rad(source_lon))
        >>> result = interp_2d_func_geo(target_lon, target_lat, source_lon, source_lat, source_data)
    """
    # 确保pyinterp可用
    if not pyinterp_available:
        raise ImportError("pyinterp package is required for geographic interpolation")

    # 验证输入数据范围
    if np.nanmin(target_y_coordinates) < -90 or np.nanmax(target_y_coordinates) > 90:
        raise ValueError("[red]Target latitude must be in range [-90, 90].[/red]")
    if np.nanmin(source_y_coordinates) < -90 or np.nanmax(source_y_coordinates) > 90:
        raise ValueError("[red]Source latitude must be in range [-90, 90].[/red]")

    # 转换为网格坐标
    if len(target_y_coordinates.shape) == 1:
        target_x_coordinates, target_y_coordinates = np.meshgrid(target_x_coordinates, target_y_coordinates)
    if len(source_y_coordinates.shape) == 1:
        source_x_coordinates, source_y_coordinates = np.meshgrid(source_x_coordinates, source_y_coordinates)

    # 验证源数据形状
    if source_x_coordinates.shape != source_data.shape[-2:] or source_y_coordinates.shape != source_data.shape[-2:]:
        raise ValueError("[red]Shape of source_data does not match shape of source_x_coordinates or source_y_coordinates.[/red]")

    # 准备坐标点并统一经度表示系统
    target_points = np.column_stack((np.array(target_x_coordinates).ravel(), np.array(target_y_coordinates).ravel()))
    origin_points = np.column_stack((np.array(source_x_coordinates).ravel(), np.array(source_y_coordinates).ravel()))
    source_xy_shape = source_x_coordinates.shape

    # 统一经度表示系统
    origin_points = origin_points.copy()
    target_points = target_points.copy()

    # 检测经度系统并统一
    src_lon_range = np.nanmax(origin_points[:, 0]) - np.nanmin(origin_points[:, 0])
    tgt_lon_range = np.nanmax(target_points[:, 0]) - np.nanmin(target_points[:, 0])

    # 如果数据接近全球范围并且表示系统不同，则统一表示系统
    if (src_lon_range > 300 or tgt_lon_range > 300) and ((np.nanmax(target_points[:, 0]) > 180 and np.nanmin(origin_points[:, 0]) < 0) or (np.nanmax(origin_points[:, 0]) > 180 and np.nanmin(target_points[:, 0]) < 0)):
        # 优先使用[0,360]系统，因为它不会在日期线处断开
        if np.nanmax(target_points[:, 0]) > 180 or np.nanmax(origin_points[:, 0]) > 180:
            # 转换为[0,360]系统
            if np.nanmin(origin_points[:, 0]) < 0:
                origin_points[:, 0] = np.where(origin_points[:, 0] < 0, origin_points[:, 0] + 360, origin_points[:, 0])
            if np.nanmin(target_points[:, 0]) < 0:
                target_points[:, 0] = np.where(target_points[:, 0] < 0, target_points[:, 0] + 360, target_points[:, 0])
        else:
            # 转换为[-180,180]系统
            if np.nanmax(origin_points[:, 0]) > 180:
                origin_points[:, 0] = np.where(origin_points[:, 0] > 180, origin_points[:, 0] - 360, origin_points[:, 0])
            if np.nanmax(target_points[:, 0]) > 180:
                target_points[:, 0] = np.where(target_points[:, 0] > 180, target_points[:, 0] - 360, target_points[:, 0])

    # 处理多维数据
    data_dims = len(source_data.shape)
    if data_dims < 2:
        raise ValueError(f"[red]Source data must have at least 2 dimensions, but got {data_dims}.[/red]")
    elif data_dims > 4:
        raise ValueError(f"Source data has {data_dims} dimensions, but this function currently supports only up to 4.")

    num_dims_to_add = 4 - data_dims
    new_shape = (1,) * num_dims_to_add + source_data.shape
    new_src_data = source_data.reshape(new_shape)

    t, z, y, x = new_src_data.shape

    # 准备并行处理参数
    params = []
    target_shape = target_y_coordinates.shape
    for t_index in range(t):
        for z_index in range(z):
            params.append((new_src_data[t_index, z_index], origin_points, target_points, interpolation_method, target_shape, source_xy_shape))

    # 并行处理
    with PEx() as excutor:
        result = excutor.run(_interp_single_worker, params)

    return np.squeeze(np.array(result).reshape(t, z, *target_shape))
