import cadquery as cq


box = cq.Workplane("XY").box(
    10.0,
    20.0,
    30.0,
    centered=(True, True, True),
)

model = cq.Assembly()
model.add(box, name="box")
