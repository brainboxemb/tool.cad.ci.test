import cadquery as cq

model = cq.Workplane("XY").box(
    10.0,
    20.0,
    30.0,
    centered=(True, True, True),
)
