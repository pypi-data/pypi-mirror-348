# Bladed Next Gen Python Models API

`dnv_bladed_models=0.6.0`

A Python package to create and edit JSON input models for Bladed Next Generation.

Visit <https://bladednextgen.dnv.com/> for more information.

## Prerequisites

- Requires Python 3.9 or above

## Usage

### Add import

```python
import dnv_bladed_models as models
```

There are a large number of model classes (500+) in the Bladed NG input API.

The root model is `BladedAnalysis`; a JSON file input to the calculation engine must have this model as the root object.

However the same capabilities are available for every model/class; each one can be read and written to JSON individually, as demonstrated below.

### Load a full Bladed NG JSON analysis model from file

```python
analysis = models.BladedAnalysis.from_file('/path/to/analysis.json')
```

This will perform some validation of the input to ensure the structure adheres to the input schema.

### Save a model to a JSON file

```python
analysis.to_file('/path/to/file.json')
```

The JSON file can then be opened in VS Code, and will automatically receive validation, doc-string and auto-complete support against the Bladed NG JSON Schema.

### Load a model from a JSON string

```python
analysis = models.BladedAnalysis.from_json(json_str)
```

This will perform some validation of the input to ensure the structure adheres to the input schema.

### Render a model as a JSON string

```python
json_str = analysis.to_json()
```

### Create a new model object in code

Create a new instance of the `BladedAnalysis` model object:

```python
analysis = models.BladedAnalysis()
```

A model object can be created with an empty initialiser as shown above, or by specifying some or all of the child models as keyword arguments:

```python
beam = models.LidarBeam(
    MountingPosition=models.LidarMountingPosition(
        X=1,
        Y=2,
        Z=3
    )
)
```

### Modify a model object in code

If a model object is already loaded, properties can be modified as required:

```python
analysis.Constants.AirCharacteristics.Density = 1.23
```

### Manipulate the turbine assembly

Access existing component definitions:

```python
# Access a known existing component by it's key, ensuring the correct type
blade = analysis.Turbine.ComponentLibrary.Component_as_Blade('blade')

# Iterate over all component entries...
for key, component in analysis.Turbine.ComponentLibrary.items():
    print(f"Component key: {key}, Component type: {component.ComponentType}")
```

Access existing nodes in the Assembly tree using string and integer accessors:

```python
blade_node = analysis.Turbine.Assembly['Hub']['PitchSystem_1'][0]

# or
blade_node = analysis.Turbine.Assembly['Hub']['PitchSystem_1']['Blade']

# or
blade_nodes = [ps_node[0] for node_name, ps_node in analysis.Turbine.Assembly['Hub'].items()]
```

Add new nodes and component definitions:

```python
analysis.Turbine.ComponentLibrary['MyHub'] = models.IndependentPitchHub()
analysis.Turbine.ComponentLibrary['MyPitchSystem'] = models.PitchSystem()
analysis.Turbine.ComponentLibrary['MyBlade'] = models.Blade()

hub_node = models.AssemblyNode(
    Definition = "ComponentLibrary.MyHub"
)
for i in range(1, 4):
    blade_node = models.AssemblyNode(
        Definition = "ComponentLibrary.MyBlade"
    )
    ps_node = models.AssemblyNode(
        Definition = "ComponentLibrary.MyPitchSystem"
    )
    ps_node[f'Blade'] = blade_node
    hub_node[f'PitchSystem_{i}'] = ps_node

analysis.Turbine.Assembly['Hub'] = hub_node
```

### Change a model to an alternative choice

Some model properties can be set to one of a number of different model types, to allow a choice between different options available in the calculation.

The property must simply be set to an object of one of the valid types. The valid types available are included in the doc strings, and the schema documentation available on the Bladed Next Gen website.

The example below is for dynamic stall. The detail of setting the specific properties on each model is omitted for brevity:

```python
analysis.Settings.Aerodynamics.DynamicStall = models.OyeModel()

# or
analysis.Settings.Aerodynamics.DynamicStall = models.IAGModel()

# or
analysis.Settings.Aerodynamics.DynamicStall = models.CompressibleBeddoesLeishmanModel()

# or
analysis.Settings.Aerodynamics.DynamicStall = models.IncompressibleBeddoesLeishmanModel()
```

### Working with type checking tooling

If using type checking development tooling, there are helper methods available to access typed references to values that could be one of several types.

For example, to obtain a reference to the DynamicStall value, the following method can be used. An error will be raised at run time if the type specifier cannot be honoured by actual objects.

The `oye` variable will receive a type of 'OyeModel' by the type engine, and at runtime is assured to receive an object of that type, or an error is raised.

```python
oye = analysis.Settings.Aerodynamics.DynamicStall_as_OyeModel
```

Additionally, a reference to the union of all possible types can be obtained using the 'as' methods (this raises an error if the object is specified with an 'insert'):

```python
dynamic_stall = analysis.Settings.Aerodynamics.DynamicStall_as_inline
```

Similar methods are available for libraries and arrays.

```python
# Get the tower object as a specific reference from the library
tower = analysis.Turbine.ComponentLibrary.Component_as_Tower('tower')

# Get a Tower Can by index, as a reference to a specific type
first_simple_can = tower.Cans_element_as_SimpleTowerCan(0)

# or process tower cans using a union of all possible types
for i, can in enumerate(tower.Cans_as_inline):
    can.CanHeight = i * 10
```

### Working with distributed files (`$insert`)

The Models API can be used to separate out a JSON file into multiple distributed files, and can read in individual files that have been distributed.

> _This package cannot resolve multiple distributed files into a single file or object. This capability is available via the Bladed Next Gen CLI, and equivalent capabilities will be made available natively in Python in a future release._

Given the following JSON:

```json
{
    "SteadyCalculation": {
        "SteadyCalculationType": "AerodynamicInformation",
        ...
    },
    "Constants": {
        "AccelerationDueToGravity": 9.8100004196167,
        ...
    }
}
```

1. Read in the document from a file:

   ```python
   analysis = models.BladedAnalysis.from_file(analysis_file)
   ```

2. Extract objects to separate files, and record the path reference in the owning object:

   ```python
   analysis.SteadyCalculation_as_inline.extract_to_insert_from_file('steady-calc/aero_info.json', analysis_file)
   
   assert analysis.SteadyCalculation.is_insert == True
   
   analysis.Constants.extract_to_insert_from_file('constants.json', analysis_file)
   
   assert analysis.Constants.is_insert = True
   ```
   
   These operations will write new JSON files relative to the directory of `analysis_file`, containing the JSON representation of the respective object.
   
   i.e.
   
   In the directory of `analysis_file`:
   
   - `steady-calc/aero_info.json` : Will contain the full JSON representation of the `AerodynamicInformationCalculation`    model object.
   
   - `constants.json` : Will contain the full JSON representation of the `Constants` model object.

3. Write out the updated analysis object to file, that now contains '$insert' references:

   ```python
   analysis.to_file(analysis_file)
   ```
   
   The following JSON will be written:
   
   ```json
   {
       "SteadyCalculation": {
           "$insert": "steady-calc/aero-info.json"
       },
       "Constants": {
           "$insert": "constants.json"
       }
   }
   ```

4. Read in a JSON document that contains inserts

    ```python
    distributed_analysis = models.BladedAnalysis.from_file(analysis_file)

    # Test and inspect
    assert distributed_analysis.SteadyCalculation.is_insert == True
    print(distributed_analysis.SteadyCalculation.insert)

    # Attempting to treat the now distributed model object as 'in-line', will yield an error
    try:
        steady_calc = distributed_analysis.SteadyCalculation_as_inline
    except ValueError as e:
        print(e)

    # Update the insert location
    distributed_analysis.SteadyCalculation.insert = 'new-dir/aero-info.json'
    ```