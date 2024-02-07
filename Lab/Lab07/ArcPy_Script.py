import arcpy

# Composite
source = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-1177815\ArcGIS\Projects\ArcGISPython"
band1 = arcpy.sa.Raster(source + r"\Band1.TIF") # blue
band2 = arcpy.sa.Raster(source + r"\Band2.TIF") # green
band3 = arcpy.sa.Raster(source + r"\Band3.TIF") # red
band4 = arcpy.sa.Raster(source + r"\Band4.TIF") # NIR

composite = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\outputCombined.tif")

# Hillshade
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(source + r"\dem.tif", source + r"\outputHillshade.tif", azimuth, altitude, shadows, z_factor)

# Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\dem.tif", source + r"\outputSlopes.tif",output_measurement, z_factor)

print("success")
