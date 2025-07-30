import re
import json

try:
    from json_equationer.equation_evaluator import evaluate_equation_dict
except:  
    try:
        from .equation_evaluator import evaluate_equation_dict
    except:
        from equation_evaluator import evaluate_equation_dict

class Equation:
    """
    A class to manage mathematical equations with units and to evaluate them.
    Provides utilities for evaluating, formatting, exporting, and printing.
   
    Initialization:
    - Normally, should be initialized as a blank dict object like example_Arrhenius = Equation().
    - Defaults to an empty equation with predefined structure.
    - Accepts an optional dictionary (`initial_dict`) to prepopulate the equation dictionary.

    Example structure:
    ```
    custom_dict = {
        'equation_string': "k = A * (e ** (-Ea / (R * T)))",
        'x_variable': "T (K)",
        'y_variable': "k (s**-1)",
        'constants': {"Ea": "30000 J/mol", "R": "8.314 J/(mol*K)", "A": "1*10**13 (s**-1)", "e": "2.71828"},
        'num_of_points': 10,
        'x_range_default': [200, 500],
        'x_range_limits': [None, 600],
        'points_spacing': "Linear"
    }

    equation_instance = Equation(initial_dict=custom_dict)
    ```
    """

    def __init__(self, initial_dict={}):
        """Initialize an empty equation dictionary."""
        self.equation_dict = {
            'equation_string': '',
            'x_variable': '',  
            'y_variable': '',
            'constants': {},
            'num_of_points': None,  # Expected: Integer, defines the minimum number of points to be calculated for the range.
            'x_range_default': [0, 1],  # Default to [0,1] instead of an empty list.
            'x_range_limits': [None, None],  # Allows None for either limit.
            'x_points_specified': [],
            'points_spacing': '',
            'reverse_scaling': False
        }

        # If a dictionary is provided, update the default values
        if len(initial_dict)>0:
            if isinstance(initial_dict, dict):
                self.equation_dict.update(initial_dict)
            else:
                raise TypeError("initial_dict must be a dictionary.")

    def validate_unit(self, value):
        """Ensure that the value is either a pure number or contains a unit."""
        unit_pattern = re.compile(r"^\d+(\.\d+)?(.*)?$")
        if not unit_pattern.match(value):
            raise ValueError(f"Invalid format: '{value}'. Expected a numeric value, optionally followed by a unit.")

    def add_constants(self, constants):
        """Add constants to the equation dictionary, supporting both single and multiple additions."""
        if isinstance(constants, dict):  # Single constant case
            for name, value in constants.items():
                self.validate_unit(value)
                self.equation_dict['constants'][name] = value
        elif isinstance(constants, list):  # Multiple constants case
            for constant_dict in constants:
                if isinstance(constant_dict, dict):
                    for name, value in constant_dict.items():
                        self.validate_unit(value)
                        self.equation_dict['constants'][name] = value
                else:
                    raise ValueError("Each item in the list must be a dictionary containing a constant name-value pair.")
        else:
            raise TypeError("Expected a dictionary for one constant or a list of dictionaries for multiple constants.")

    def set_x_variable(self, x_variable):
        """
        Set the x-variable in the equation dictionary.
        Expected format: A descriptive string including the variable name and its unit.
        Example: "T (K)" for temperature in Kelvin.
        """
        self.equation_dict["x_variable"] = x_variable

    def set_y_variable(self, y_variable):
        """
        Set the y-variable in the equation dictionary.
        Expected format: A descriptive string including the variable name and its unit.
        Example: "k (s**-1)" for a rate constant with inverse seconds as the unit.
        """
        self.equation_dict["y_variable"] = y_variable

    def set_x_range_default(self, x_range):
        """
        Set the default x range.
        Expected format: A list of two numeric values representing the range boundaries.
        Example: set_x_range([200, 500]) for temperatures between 200K and 500K.
        """
        if not (isinstance(x_range, list) and len(x_range) == 2 and all(isinstance(i, (int, float)) for i in x_range)):
            raise ValueError("x_range must be a list of two numeric values.")
        self.equation_dict['x_range_default'] = x_range

    def set_x_range_limits(self, x_limits):
        """
        Set the hard limits for x values.
        Expected format: A list of two values (numeric or None) defining absolute boundaries.
        Example: set_x_range_limits([100, 600]) to prevent x values outside this range.
        Example: set_x_range_limits([None, 500]) allows an open lower limit.
        """
        if not (isinstance(x_limits, list) and len(x_limits) == 2):
            raise ValueError("x_limits must be a list of two elements (numeric or None).")
        if not all(isinstance(i, (int, float)) or i is None for i in x_limits):
            raise ValueError("Elements in x_limits must be numeric or None.")
        self.equation_dict['x_range_limits'] = x_limits

    def set_num_of_points(self, num_points):
        """
        Set the number of calculation points.
        Expected format: Integer, specifies the number of discrete points for calculations.
        Example: set_num_of_points(10) for ten data points.
        """
        if not isinstance(num_points, int) or num_points <= 0:
            raise ValueError("Number of points must be a positive integer.")
        self.equation_dict["num_of_points"] = num_points

    def set_equation(self, equation_string):
        """Modify the equation string."""
        self.equation_dict['equation_string'] = equation_string

    def get_equation_dict(self):
        """Return the complete equation dictionary."""
        return self.equation_dict
    
    def evaluate_equation(self, remove_equation_fields= False):
        evaluated_dict = evaluate_equation_dict(self.equation_dict) #this function is from the evaluator module
        self.equation_dict["x_points"] = evaluated_dict["x_points"]
        self.equation_dict["y_points"] = evaluated_dict["y_points"]
        self.equation_dict["x_units"] = evaluated_dict["x_units"]
        self.equation_dict["y_units"] = evaluated_dict["y_units"]
        
        if remove_equation_fields == True:
            #we'll just make a fresh dictionary for simplicity, in this case.
            equation_dict = {}
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
            self.equation_dict = equation_dict
        return self.equation_dict

    def print_equation_dict(self, pretty_print=True, evaluate_equation = True, remove_equation_fields = False):
        equation_dict = self.equation_dict #populate a variable internal to this function.
        #if evaluate_equation is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if evaluate_equation == True:
            evaluated_dict = self.evaluate_equation(remove_equation_fields = remove_equation_fields) #For this function, we don't want to remove equation fields from the object, just the export.
            equation_dict = evaluated_dict
        if remove_equation_fields == True:
            equation_dict = {}
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]
        if pretty_print == False:
            print(equation_dict)
        if pretty_print == True:
            equation_json_string = json.dumps(equation_dict, indent=4)
            sys.stdout.flush()
            print(equation_json_string)

    def export_to_json_file(self, filename, evaluate_equation = True, remove_equation_fields= False):
        """
        writes the json to a file
        returns the json as a dictionary.
        update_and_validate function will clean for plotly. One can alternatively only validate.
        optionally simulates all series that have a simulate field (does so by default)
        optionally removes simulate filed from all series that have a simulate field (does not do so by default)
        optionally removes hints before export and return.
        """
        equation_dict = self.equation_dict #populate a variable internal to this function.
        #if evaluate_equation is true, we'll try to simulate any series that need it, then clean the simulate fields out if requested.
        if evaluate_equation == True:
            evaluated_dict = self.evaluate_equation(self, remove_equation_field = False) #For this function, we don't want to remove equation fields from the object, just the export.
            equation_dict = evaluated_dict
        if remove_equation_fields == True:
            equation_dict = {}
            equation_dict["x_points"] = self.equation_dict["x_points"] 
            equation_dict["y_points"] = self.equation_dict["y_points"] 
            equation_dict["x_units"] = self.equation_dict["x_units"] 
            equation_dict["y_units"] = self.equation_dict["y_units"]

        # filepath: Optional, filename with path to save the JSON file.       
        if len(filename) > 0: #this means we will be writing to file.
            # Check if the filename has an extension and append `.json` if not
            if '.json' not in filename.lower():
                filename += ".json"
            #Write to file using UTF-8 encoding.
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(equation_dict, f, indent=4)
        return equation_dict



if __name__ == "__main__":
    # Create an instance of Equation
    example_Arrhenius = Equation()
    example_Arrhenius.set_equation("k = A * (e ** (-Ea / (R * T)))")
    example_Arrhenius.set_x_variable("T (K)")  # Temperature in Kelvin
    example_Arrhenius.set_y_variable("k (s**-1)")  # Rate constant in inverse seconds

    # Add a constants one at a time, or through a list.
    example_Arrhenius.add_constants({"Ea": "30000 J/mol"})  
    example_Arrhenius.add_constants([
        {"R": "8.314 J/(mol*K)"},
        {"A": "1*10**13 (s**-1)"},
        {"e": "2.71828"}  # No unit required
    ])

    # Optinally, set minimum number of points and limits for calculations.
    example_Arrhenius.set_num_of_points(10)
    example_Arrhenius.set_x_range_default([200, 500])
    example_Arrhenius.set_x_range_limits([None, 600])  

    # Define additional properties.
    example_Arrhenius.equation_dict["points_spacing"] = "Linear"

    # Retrieve and display the equation dictionary
    equation_dict = example_Arrhenius.get_equation_dict()
    print(equation_dict)

    example_Arrhenius.evaluate_equation()
    import sys
    sys.stdout.flush()
    example_Arrhenius.print_equation_dict()
    