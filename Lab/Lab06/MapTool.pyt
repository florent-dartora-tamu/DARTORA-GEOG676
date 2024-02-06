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
        self.tools = [GraduatedColorsRender, UniqueValueRenderer]

class GraduatedColorsRender(object):
    # required : define and init the tool.
    def __init__(self): 
        self.label = "Graduated Color"
        self.description = "Create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False # Only used in ArcGIS
        self.category = "MapTools" # the category attribute is a way to group different tools within our toolbox in ArcGIS Pro interface

    # optional only if you do not need to use any user provided inputs. Within this method we define what parameters our tool requires from the user. 
    def getParameterInfo(self):
        # original project name
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="arpxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        # which layer you want to classify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )
        # output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        # output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
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
        readTime = 3
        start = 0
        maximum = 100
        step = 25
        
        # Setup the progressor
        arcpy.SetProgressor("step", "Running script...", start, maximum, step)
        time.sleep(readTime)
        # Displays message to the user
        arcpy.AddMessage("Running script...")

        # Setup our user input variables
        # Reference to our .aprx
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        # Grab the first map in the .aprx
        campus = project.listMaps('Map')[0]

        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding map layer....")
        time.sleep(readTime)
        arcpy.AddMessage("Finding map layer....")

        # Loop through available layers in the map
        for layer in campus.listLayers():
            # Check if layer is a feature layer
            if layer.isFeatureLayer:
                # Obtain a copy of the layer's symbology
                symbology = layer.symbology
                # Check if it has a 'renderer' attribute
                if hasattr(symbology, 'renderer'):
                    # Check if the layer's name is the one in input
                    if layer.name == parameters[1].valueAsText:

                        # Increment the progressor, change label, output message to results pane too
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Calculating and classifying....")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying....")

                        # Update the copy's renderer to be 'GraduatedColorsRenderer'
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        # Tell arcpy which field we want to base our choropleth off of
                        symbology.renderer.classificationField = "Shape_Area"
                        # Set how many classes we'll have 
                        symbology.renderer.breakCount = 5
                        # Set the color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology 
                    else:
                        print("Not a valid layer")

        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving output project....")
        time.sleep(readTime)
        arcpy.AddMessage("Saving output project....")
        
        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".arpx")

        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(maximum)
        arcpy.SetProgressorLabel("Operation completed.")
        time.sleep(readTime)
        arcpy.AddMessage("Operation completed.")

        return

def postExecute(self, parameters):
    """This method takes place after outputs are processed and 
    added to the display."""
    return



class UniqueValueRenderer(object):
    # required : define and init the tool.
    def __init__(self): 
        self.label = "Unique Value Color"
        self.description = "Create a unique value colored map based on a specific attribute of a layer"
        self.canRunInBackground = False # Only used in ArcGIS
        self.category = "MapTools" # the category attribute is a way to group different tools within our toolbox in ArcGIS Pro interface

    # optional only if you do not need to use any user provided inputs. Within this method we define what parameters our tool requires from the user. 
    def getParameterInfo(self):
        # original project name
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="arpxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        # which layer you want to classify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )
        # output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        # output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
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
        readTime = 3
        start = 0
        maximum = 100
        step = 25
        
        # Setup the progressor
        arcpy.SetProgressor("step", "Running script...", start, maximum, step)
        time.sleep(readTime)
        # Displays message to the user
        arcpy.AddMessage("Running script...")

        # Setup our user input variables
        # Reference to our .aprx
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        # Grab the first map in the .aprx
        campus = project.listMaps('Map')[0]

        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding map layer....")
        time.sleep(readTime)
        arcpy.AddMessage("Finding map layer....")

        # Loop through available layers in the map
        for layer in campus.listLayers():
            # Check if layer is a feature layer
            if layer.isFeatureLayer:
                # Obtain a copy of the layer's symbology
                symbology = layer.symbology
                # Check if it has a 'renderer' attribute
                if hasattr(symbology, 'renderer'):
                    # Check if the layer's name is the one in input
                    if layer.name == parameters[1].valueAsText:

                        # Increment the progressor, change label, output message to results pane too
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Calculating and classifying....")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying....")

                        # Update the copy's renderer to be 'UniqueValueRenderer'
                        symbology.updateRenderer('UniqueValueRenderer')
                        # Tells arcpy that we want to use "Type" as our unique value
                        symbology.renderer.fields = ["Type"]
                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology # Very important step
                    else:
                        print("Not a valid layer")

        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving output project....")
        time.sleep(readTime)
        arcpy.AddMessage("Saving output project....")
        
        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".arpx")

        # Increment the progressor, change label, output message to results pane too
        arcpy.SetProgressorPosition(maximum)
        arcpy.SetProgressorLabel("Operation completed.")
        time.sleep(readTime)
        arcpy.AddMessage("Operation completed.")

        return

def postExecute(self, parameters):
    """This method takes place after outputs are processed and 
    added to the display."""
    return
