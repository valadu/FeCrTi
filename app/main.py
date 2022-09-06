from part import Part


steps = ['Relaxation', 'Data Visualization', 'Optimization']
part = Part()

part.meta()
step = part.sidebar(steps)
if step == steps[0]:
    part.relaxation()
elif step == steps[1]:
    part.data_visualization()
