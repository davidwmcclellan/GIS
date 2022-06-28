import matplotlib.pyplot as plt
import arcpy
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('spatial')
dem = arcpy.GetParameterAsText(0)
flow_accum_raster = arcpy.GetParameterAsText(1)
flow_accum_plot = arcpy.GetParameterAsText(2)
cutoff = 1000

flow_dir = arcpy.sa.FlowDirection(dem)

accumulation = arcpy.sa.FlowAccumulation(flow_dir)
accumulation.save(flow_accum_raster)

# 4.2
# Create some lists that will be used to map elevation ranges to single numbers.
# [min_elevation, max_elevation, new_value]
values = [[accumulation.minimum, cutoff, 1],
          [cutoff, accumulation.maximum, 0]]

# Create a RemapRange using the data just created, and print it out.
remap = arcpy.sa.RemapRange(values)


reclass = arcpy.sa.Reclassify(accumulation, 'VALUE', remap)


# 4.3
import numpy as np

# Load the accumulation raster into a numpy array called data.
nump = arcpy.RasterToNumPyArray(reclass)
# 4.4
# Plot the masked data in grayscale.
plt.imsave(flow_accum_plot, nump, cmap='gray')
messages.addMessage('Done!')
