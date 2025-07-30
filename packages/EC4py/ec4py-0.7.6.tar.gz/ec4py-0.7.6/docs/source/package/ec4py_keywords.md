---
title: Keywords
parent: Package
nav_order: 100
---

# Keywords

## IR correction

| Keyword        | Meaning           | Where to use  |
| ------------- |:-------------| -----:|
| IRcorr = "R" | iR-compensation using measured <br>real part of the impedance |When loading a dataset|
| IRcorr = "Z" | iR-correct using measured <br> absolute impedance| When loading a dataset |
| IRcorr = "Rmed" | Calculates first the median of the real part of the impedance(Rmed), <br>and then i*Rmed to correct the potential| When loading a dataset |
| IRcorr = "Zmed" | Calculates first the median of the absolute impedance(Zmed), <br>then  the calculated i*Zmed to correct the potential| When loading a dataset |
| IRcorr = 1.0 | Manual iR-correct<br>where the number corresponds to the Rsol | When loading a dataset |

## For plotting
The plots are created using mathplotlib. Typical keywords associated with plotting using PLT can be used to adjust a plot.

| Keyword        | Meaning           | Where to use  |
| ------------- |:-------------| -----:|
| title = "string" | Change the title of a plot. | When plotting a dataset|
| xlabel = "string" | Change the xlabel of a plot. | When plotting a dataset|
| ylabel = "string" | Change the ylabel of a plot. | When plotting a dataset|
| xscale = "log" | Change the x scale to log. | When plotting a dataset|
| yscale = "log" | Change the y scale to log. | When plotting a dataset|
| y_smooth = 3 | moving averaging of the y data <br> number correspond to the width of the moving average. | When plotting a dataset|
| x_smooth = 4 | moving averaging of the y data <br> number correspond to the width of the moving average.| When plotting a dataset |
| label = "string" or ["str",..] | Change the label of a line(s). | When plotting a dataset|
| color = "color" or ["color1",..]| Change the color of a line(s). | When plotting a dataset|
| linewidth = float or [float,..]| Change the color of a line(s). | When plotting a dataset|
| linestyle = "style" or ["style1",..]| Change the linestyle of a line(s). | When plotting a dataset|
| alpha = float or [float,..]| Change the alpha channel of a line(s). | When plotting a dataset|
| xlim = [float , float]| Change x-limits of the graph. | When plotting a dataset|
| ylim = [float , float]| Change y-limits of the graph. | When plotting a dataset|


 

