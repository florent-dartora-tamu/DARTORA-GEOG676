# Lab4

import arcpy

# Setting the workspace (overall settings of our script)
folder_path = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-1177815\ArcGIS\Projects\ArcGISPython"
arcpy.env.workspace = folder_path

# Setting scratch workspace (output data we do not wish to maintain)
arcpy.env.scratchWorkspace = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-1177815\ArcGIS\Projects\ArcGISPython\scratch"


# Task 1 : Read in garage location X/Y coords from the provided .csv
# Turn the .csv into a feature class (into a shapefile)
garages = arcpy.management.MakeXYEventLayer("garages.csv", "x", "y", "garages")


# Task 2 : Create a geodatabase and add in the input layers
# Create a geodatabase named "lab3"
arcpy.CreateFileGDB_management(folder_path, "lab3.gdb")
lab3Gdb = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-1177815\ArcGIS\Projects\ArcGISPython\lab3.gdb"

# Extract the "Structures" layer from Campus.gbd
campusDB = r"\\storage\homes\S-1-5-21-1167378736-2199707310-2242153877-1177815\ArcGIS\Projects\ArcGISPython\Campus.gdb"
structureLayer = campusDB + r"\Structures"


# We creates a list variable containing the 2 layers. Then we use the FeatureClassToGeodatabase_conversion() method to copy our layers into the geodatabase.
input_layers = [structureLayer, garages]
arcpy.FeatureClassToGeodatabase_conversion(input_layers, lab3Gdb)


# Task 3 : Buffer the garage points
# Setup our user input variables
bufferSize_input = input("Please enter a buffer size in meters: ")
arcpy.Buffer_analysis(lab3Gdb + r"\garages", lab3Gdb + r"\garages_buffered", bufferSize_input + " Meters")


# Task 4 : Intersect the buildings layer with the buffered garage points
arcpy.Intersect_analysis([lab3Gdb + r"\garages_buffered", lab3Gdb + r"\Structures"], lab3Gdb + r"\garages_intersection", "ALL")


# Task 5 : Output the resulting table to a .csv
arcpy.TableToTable_conversion(lab3Gdb + r"\garages_intersection.dbf", folder_path, "garages_intersection.csv")

