import maya.api.OpenMaya as om2


poly_counts = [4, 4]

vertices = [om2.MPoint(0, 0, 0, 0),
          om2.MPoint(1.0, 0, 0, 0),
          om2.MPoint(0, 1.0, 0, 0),
          om2.MPoint(1.0, 1.0, 0, 0),
          om2.MPoint(0, 2.0, 0, 0),
          om2.MPoint(1.0, 2.0, 0, 0)]

poly_connects = [0, 1, 3, 2,
                 2, 3, 5, 4]

mesh = om2.MFnMesh()

mesh.create(vertices, poly_counts, poly_connects)

