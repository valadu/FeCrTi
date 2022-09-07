from part import Part


main_steps = ('Relaxation', 'Data Visualization', 'Optimization')
optim_steps = ('References', 'Get Started')
part = Part()

# Site logic
part.meta()
main_step = part.sidebar(main_steps)
if main_step == main_steps[0]:
    part.relaxation()
elif main_step == main_steps[1]:
    part.data_visualization()
elif main_step == main_steps[2]:
    optim_step = part.optimization(optim_steps)
    if optim_step == optim_steps[0]:
        part.optimization_references()
    elif optim_step == optim_steps[1]:
        part.optimization_getstarted()
