from osgeo import gdal, osr
from pathlib import Path
import logging
import os
import shutil

gdal.UseExceptions()
osr.UseExceptions()
gdal.ConfigurePythonLogging(enable_debug=True)

DATA_DIR = "./data"
CRSs = [32610, 32611]
input_res = 1.0
output_res = input_res * 2.0


def create_test_data(
    start_xx: int,
    start_yy: int,
    epsg: int,
    height: int,
    width: int,
    res: float,
    num_files: int = 100,
) -> None:
    data_path = Path(DATA_DIR)
    data_path.mkdir(parents=True, exist_ok=True)
    xx, yy = start_xx, start_yy
    transforms = [
        (xx + i * width * res, res, 0.0, yy + i * height * res, 0.0, -res)
        for i in range(num_files)
    ]
    for i in range(num_files):
        filename = (
            data_path
            / f"test_{int(transforms[i][0])}_{int(transforms[i][3])}_{epsg}.tif"
        )
        with gdal.GetDriverByName("GTiff").Create(
            str(filename),
            width,
            height,
            1,
            gdal.GDT_Byte,
        ) as ds:
            ds.SetGeoTransform(transforms[i])
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(epsg)
            ds.SetProjection(srs.ExportToWkt())
            band = ds.GetRasterBand(1)
            band.SetNoDataValue(0)
            band.Fill(1)


def create_gti(input_dir: str, output_name: str, res: float) -> None:
    alg = gdal.alg.driver.gti.create(
        input=input_dir,
        output=output_name,
        dst_crs="EPSG:3857",
        resolution=[res, res],
        filename_filter="*.tif",
        output_data_type="Byte",
        band_count=1,
        nodata=0,
        mask=False,
        overwrite=True,
    )
    alg.Finalize()


def create_tiff(input_file: str, output_file: str) -> None:
    alg = gdal.alg.raster.convert(
        input=input_file,
        output=output_file,
        output_format="GTiff",
        creation_option={
            "SPARSE_OK": "TRUE",
            "BIGTIFF": "YES",
            "TILED": "YES",
            "BLOCKXSIZE": 512,
            "BLOCKYSIZE": 512,
        },
        overwrite=True,
    )
    alg.Finalize()


if __name__ == "__main__":
    if (data_path := Path(DATA_DIR)).exists():
        shutil.rmtree(data_path)
    config_options = {
        "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    }
    with gdal.config_options(config_options, thread_local=False):
        create_test_data(
            490968, 5456767, CRSs[0], 2000, 2000, input_res, num_files=500
        )
        create_test_data(
            705126, 5657838, CRSs[1], 2000, 2000, input_res, num_files=500
        )
        create_gti(DATA_DIR, "test.gti.gpkg", output_res)
        create_tiff("test.gti.gpkg", "test.tif")
