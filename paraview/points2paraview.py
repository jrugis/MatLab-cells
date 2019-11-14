###################################
###################################
IMAGE_SIZE_XY = 1024.0
IMAGE_SIZE_Z = 26.0 
ACTUAL_XY = 80.0
ACTUAL_STEP_Z = 2.0
ACTUAL_GLYPH = 3.0

###################
SCALE_X = ACTUAL_XY / IMAGE_SIZE_XY 
SCALE_Y = SCALE_X
SCALE_Z = ACTUAL_STEP_Z

###################################
###################################
data = CSVReader(FileName=['/Users/jrug001/Desktop/nesi00119/mesh-cells/paraview/points.txt'])
RenameSource('data')
data.HaveHeaders = 0
data.FieldDelimiterCharacters = " "

###################
points = TableToPoints(Input=data)
RenameSource('points')
points.XColumn = 'Field 1'
points.YColumn = 'Field 2'
points.ZColumn = 'Field 0'
points.KeepAllDataArrays = 1
#points.PointData.GetArray('Field 0').GetRange()

###################
transform = Transform(Input=points)
RenameSource('transform')
transform.Transform = 'Transform'
transform.Transform.Scale = [SCALE_X, SCALE_Y, SCALE_Z]
#transform.Transform.Rotate = [15., 20., 60.]
#transform.Transform.Translate = [1., 0., 0.]

###################
glyph = Glyph(Input=transform, GlyphType='Sphere')
RenameSource('glyph')
glyph.ScaleArray = ['POINTS', 'No scale array']
glyph.ScaleFactor = ACTUAL_GLYPH
glyph.GlyphMode = 'All Points'
glyph.GlyphType.PhiResolution = 12
glyph.GlyphType.ThetaResolution = 12
#glyph.Scalars = ['POINTS', 'Field 0']
#glyph.Vectors = ['POINTS', 'None']
# glyph1.Scalars = ['POINTS', 'Field 2']
# glyph1.ScaleMode = 'scalar'
UpdatePipeline()

###################################
###################################
renderView = GetActiveView()

###################
#pointsDisplay = Show(points, renderView)
#pointsDisplay.PointSize = 5

###################
glyphDisplay = Show(glyph, renderView)
glyphDisplay.Representation = 'Surface'
glyphDisplay.DiffuseColor = [1.0, 0.1, 0.1]
#ColorBy(glyphDisplay, ('POINTS', 'Field 2'))
#glyphDisplay.SetScalarBarVisibility(renderView, True)
#glyphDisplay.RescaleTransferFunctionToDataRange(True, False)

###################
UpdatePipeline()
renderView.Update()

renderView.AxesGrid.Visibility = 1
renderView.CenterAxesVisibility = 1

renderView.ResetCamera()
renderView.CameraParallelProjection = 1

Render(renderView)

###################################
