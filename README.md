# CSV Correlations Program

## Overview
The **CSV Correlations Program** is a graphical user interface (GUI) application built with Tkinter that allows users to analyze correlations within a dataset stored in a CSV file. The program enables users to upload a CSV file, view the dataset in a structured format, compute correlation matrices, and visualize relationships between variables using scatter plots.

## Features
- **Upload CSV File**: Users can select and load a CSV file into the application.
- **Display Dataset**: The loaded data is displayed in a tabulated format for easy viewing.
- **Compute Correlation Matrix**: The program calculates and displays the correlation coefficients between numerical variables.
- **Scatter Plot Visualization**: Generates scatter plots showing the relationships between the dependent variable and predictor variables.
- **Navigation Toolbar**: Users can interact with the generated scatter plots, zooming and panning for better analysis.

## Functionality Breakdown
### 1. Uploading a CSV File
- The user selects a CSV file using the **Upload CSV** button.
- The file path is displayed in an entry widget.
- The program reads the CSV file using **pandas** and displays the dataset in a **Text widget** with a scrollable interface.
- If an error occurs (e.g., incorrect file format), a warning message is displayed.

### 2. Displaying Data
- The loaded dataset is displayed in a structured tabular format using the **tabulate** library.
- If no file is uploaded, placeholder values are displayed.

### 3. Running Correlation Analysis
- The user inputs a **dependent variable** (one of the column names in the dataset).
- The **Run Correlation** button calculates the correlation matrix using `pandas.DataFrame.corr()`.
- The correlation matrix is displayed in a tabulated format, showing the relationships between numerical variables.
- If no CSV file is loaded or the dependent variable is incorrect, a warning message is shown.

### 4. Visualizing Correlations with Scatter Plots
- The program generates scatter plots to visualize the relationship between the selected dependent variable and all other numerical variables.
- The plots are displayed in a 2-column grid layout.
- If the number of predictor variables is odd, unused plots are hidden for a cleaner display.
- The user can interact with the plots using a **Navigation Toolbar**, allowing zooming and panning.

## How It Works
1. **Launch the Program**
   - Run the Python script to open the GUI.
2. **Upload a CSV File**
   - Click **Upload CSV**, select a file, and view the data.
3. **Enter a Dependent Variable**
   - Type the column name of the dependent variable in the input field.
4. **Run Correlation Analysis**
   - Click **Run Correlation** to generate the correlation matrix and scatter plots.
5. **Analyze the Results**
   - View the correlation coefficients and use scatter plots to explore relationships between variables.

## Notes
- Ensure the CSV file has numerical values for meaningful correlation analysis.
- The dependent variable must be an existing column name in the dataset.

## Suggested Improvements
- Include more visualization options, such as heatmaps.


---
This program simplifies correlation analysis by providing an easy-to-use interface for data visualization and interpretation. 🚀

