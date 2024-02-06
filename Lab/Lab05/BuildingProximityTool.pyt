# -*- coding: utf-8 -*-

import arcpy
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BuildingProximity]

class BuildingProximity(object):
    # required : define and init the tool.
    def __init__(self): 
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False # Only used in ArcGIS
        self.category = "Building Tools" # the category attribute is a way to group different tools within our toolbox in ArcGIS Pro interface

    # optional only if you do not need to use any user provided inputs. Within this method we define what parameters our tool requires from the user. 
    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GBDFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",
            datatype="DEType",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="bufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3, param4, param5]
        return params

    # optional : this method is used to check for any extensions your tool may need and if the user has an appropriate license.
    def isLicensed(self):
        return True

    # optional : this method is used to update input parameters before ArcGIS's internal validation step runs. This method is useful if you need to process the user's input in some way before using them.
    def updateParameters(self, parameters):
        return

    # optional : this method is useful for creating custom error messages regarding your inputs.
    def updateMessages(self, parameters): 
        return

    # required : contains the source code of the tool.
    def execute(self, parameters, messages): 
        # Define progressor variables
        readTime = 2.5
        start = 0
        maximum = 100
        step = 25
        
        # Setup the progressor
        arcpy.SetProgressor("step", "Checking building proximity...", start, maximum, step)
        time.sleep(readTime)

        # Displays message to the user
        arcpy.AddMessage("Running script...")

        # Setup our user input variables
        gdbFolder_input = parameters[0].valueAsText
        gdbName_input = parameters[1].valueAsText
        gdbPath = gdbFolder_input + "\\" + gdbName_input
        garageCSVFile_input = parameters[2].valueAsText
        garageLayerName_input = parameters[3].valueAsText
        campusGDB_input = parameters[4].valueAsText
        bufferDistance_input = int(parameters[5].value)


        # Read in garage location X/Y coords from the provided .csv
        garages = arcpy.management.MakeXYEventLayer(garageCSVFile_input, "x", "y", garageLayerName_input)
        arcpy.AddMessage("Reading CSV file...")

        # Create a geodatabase 
        arcpy.CreateFileGDB_management(gdbFolder_input, gdbName_input)
        # Increment the progressor and change the label; add message to the results pane
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Creating geodatabase...")
        time.sleep(readTime)
        arcpy.AddMessage("Creating geodatabase...")

        # Extract the "Structures" layer from Campus.gbd
        structureLayer = campusGDB_input + r"\Structures"
        buildingsLayer = gdbPath + "\\" + 'Buildings'
        arcpy.Copy_management(structureLayer, buildingsLayer)

        # import garages layer in geodatabase
        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdbPath)
        garagePath = gdbPath + "\\" + garageLayerName_input

        spatial_ref = arcpy.Describe(buildingsLayer).spatialReference
        arcpy.Project_management(garagePath, gdbPath + r"\Garage_Points_reprojected", spatial_ref)

        # Buffer the garage points
        arcpy.Buffer_analysis(gdbPath + r"\Garage_Points_reprojected", gdbPath + r"\Garages_Buffered", str(bufferDistance_input) + " Meters")
        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Buffering....")
        time.sleep(readTime)
        arcpy.AddMessage("Buffering...")

        # test
        arcpy.Project_management(gdbPath + r"\Garages_Buffered", gdbPath + r"\Garage_Buffered_reprojected", spatial_ref)


        # Intersect the buildings layer with the buffered garage points
        arcpy.Intersect_analysis([gdbPath + r"\Garage_Buffered_reprojected", gdbPath + r"\Buildings"], gdbPath + r"\Garages_Intersection", "ALL")
        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Generating intersection layer....")
        time.sleep(readTime)
        arcpy.AddMessage("Generating intersection layer...")

        # test
        arcpy.Project_management(gdbPath + r"\Garages_Intersection", gdbPath + r"\Garage_Intersection_reprojected", spatial_ref)


        # Output the resulting table to a .csv
        arcpy.TableToTable_conversion(gdbPath + r"\Garage_Intersection_reprojected.dbf", gdbFolder_input, "Garages_Intersection.csv")
        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(maximum)
        arcpy.SetProgressorLabel("Generating output csv file....")
        time.sleep(readTime)
        arcpy.AddMessage("Generating output csv file...")

        arcpy.AddMessage("Script completed")
        
        return

def postExecute(self, parameters):
    """This method takes place after outputs are processed and 
    added to the display."""
    return

