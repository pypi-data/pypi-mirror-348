# WGFMUpy

## How to use the package
1) `import WGFMUpy`
2) instantiate `WGFMU = WGFMUpy.WGFMU_class()`
3) use the functions from the _wgfmu.dll_ as `return_values=WGFMU.functionName(input_parameters)`.
The original functions from the library use variable pointers to pass the values, the python version of the function returns the values.
The python functions use python variable types for the inputs and return values, the conversion is handled internally.
4) All the parameter defined in _wgfmu.h_ (`WGFMU_paramName`) are available as `WGFMU.paramName`

## Original WGFMU library information
for more information about the original WGFMU library visit:
https://www.keysight.com/ca/en/lib/software-detail/driver/b1530a-wgfmu-instrument-library--sample-programs-2117445.html
https://www.keysight.com/ca/en/assets/9018-01706/user-manuals/9018-01706.pdf

## Disclaimer
ChatGPT and Gemini have been used to speed up the conversion of all the possible functions and parameters, some issues have been corrected but some are expected to still be present