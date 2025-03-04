from tkinter import *
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from tabulate import tabulate

DATA = None
window = Tk()
window.title("Correlation Analysis Program")
window.config(padx=10, pady=10)
# window.minsize(width=1300,height=650)


# Default values for data display placeholders
default_data = [["0" for _ in range(5)] for _ in range(4)]
default_data_headers = ["Variable 1", "Variable 2", "Variable 3","Variable 4", "Variable 5", "Variable 6"]
default_correlation = [["0" for _ in range(4)] for _ in range(6)]
default_correlation_headers = ["Correlation 1", "Correlation 2", "Correlation 3","Correlation 4", "Correlation 5", "Correlation 6"]

# Function to add placeholder values to the Text widgets
def set_default_text():
    data_text.insert(END, tabulate(default_data, headers=default_data_headers, tablefmt="fancy_grid"))
    correlation_text.insert(END, tabulate(default_correlation, headers=default_correlation_headers, tablefmt="fancy_grid"))


# Upload CSV file and display data in Text widget
def upload_csv():
    global DATA
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if file_path:
        # Set the file path in the entry widget
        file_path_entry.delete(0, END)
        file_path_entry.insert(0, file_path)
        try:
            # Load the CSV data from the path in the Entry widget
            DATA = pd.read_csv(file_path_entry.get())
            data_text.delete("1.0", END)  # Clear previous content
            data_text.insert(END, tabulate(DATA, headers="keys", tablefmt="fancy_grid"))
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to load. Ensure file type is .csv\nError: {e}")


# Display correlation matrix in Text widget and generate plot
def correlation():
    global DATA
    try:
        correlation = DATA.corr()
        correlation_text.delete("1.0", END)
        correlation_text.insert(END, tabulate(correlation, headers="keys", tablefmt="fancy_grid"))
        show_correlation_scatter_plots()
    except Exception as e:
        messagebox.showwarning("Warning", f"Please load the CSV file first.\nError: {e}")


# Plot the correlation scatter plots
def show_correlation_scatter_plots():
    # Having already loaded the csv using the upload csv function, the DATA variable will already be populated with data. Thus, the function will use the DATA dataframe for most analysis.
    # Fetch the dependent variable from the entry by the user. This will be used as the target variable for the scatter plots
    target_variable = dependent_variable_entry.get()
    if target_variable not in DATA.columns:
        messagebox.showwarning("Warning", "Input a dependent variable to run correlation.\nHint: Dependent variable is one of the columns of the csv table ")
        return

    # Create a list through list comprehension called 'other variables' to be used to plot predictor variables against the target
    other_variables = [col for col in DATA.columns if col != target_variable]

    # Set up a grid for multiple scatter plots. Each grid box will have its own scatter plot.
    number_of_variables = len(other_variables)
    no_of_cols = 2
    no_of_rows = (number_of_variables + 1) // 2  # Calculate rows needed for 2 columns. By adding 1 to num_vars and then performing integer division by 2, you ensure it is round up when there’s an odd number of variables.

    fig, axes = plt.subplots(no_of_rows, no_of_cols, figsize=(6, 4)) #plt.subplots generates a figure (fig) with a grid of subplots (axes)
    fig.suptitle(f'Predictor variables vs {target_variable} Scatter Plots', fontsize=14) # sets a central title for the entire figure
    # The axes object is initially a 2D array (since it’s a 2x2 grid). Flattening it turns axes into a 1D array, making it simpler to loop over each subplot.
    #This way, we can easily reference each subplot in a loop as axes[i] instead of needing to specify row-column indexing like axes[row, col].
    axes = axes.flatten()

    #This loop iterates over each variable in other_variables (which contains all variables except the target variable) and assigns an index i to each variable.
    for i, variable in enumerate(other_variables):
        sns.scatterplot(x=DATA[variable], y=DATA[target_variable], ax=axes[i], alpha=0.6,color="red") #ax=axes[i]: This tells Seaborn to draw the scatter plot on a specific subplot in the axes array, where axes[i] refers to the current subplot and alpha is for transparency
        axes[i].set_title(f'{variable} vs {target_variable}')
        axes[i].set_xlabel(variable)
        axes[i].set_ylabel(target_variable)

    # Hide any extra subplot axes if the number of variables is odd
    for j in range(i + 1, len(axes)): # This loop iterates over any unused axes starting from i + 1 (the last populated axis). axes[j].axis('off'): This command hides the axis for the unused subplot, making the figure cleaner.
        axes[j].axis('off')

    # Adjust layout. The plt.tight_layout() adjusts the padding between subplots to prevent overlapping, especially for titles, labels, and axes.
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # The rect argument defines the position and size of the plotting area within the figure. [0, 0.03, 1, 0.95] specifies margins around the entire grid (left, bottom, right, top).

    #  Before adding the new scatter plots, this loop removes any widgets currently in frame3. This is essential to prevent overlapping figures if the function is called multiple times.
    for widget in frame3.winfo_children():
        widget.destroy()

    figure_canvas = FigureCanvasTkAgg(fig, master=frame3)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().pack(fill="both", expand=True)

    # Add navigation toolbar below the plot
    toolbar = NavigationToolbar2Tk(figure_canvas, frame3)
    toolbar.update()
    toolbar.pack(side=BOTTOM, fill=X)


def add_placeholder(entry, placeholder_text):
    # Function to add a placeholder to an Entry widget
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, END)  # Remove placeholder
            entry.config(fg="black")  # Set text color to black for user input

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)  # Add placeholder
            entry.config(fg="blue")  # Set text color to blue for placeholder

    # Set the initial placeholder text
    entry.insert(0, placeholder_text)
    entry.config(fg="blue")  # Set text color to gray for placeholder

    # Bind the focus events to the Entry widget
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# Frame for the CSV data
frame = ttk.Frame(window, width=400, height=200)
frame.grid(row=1, column=0, columnspan=2, pady=10)

# Csv input button for loading the csv and an entry widget for displaying the file path
file_path_entry = Entry(width=50, font=("Arial", 13, "normal"))
file_path_entry.grid(row=0, column=0, pady=10, sticky="w")

csv_input_button = Button(window, text="Upload\n CSV",font=("Arial", 15,),
                                 activebackground="blue", bg="white", command=upload_csv)
csv_input_button.grid(row=0, column=1, pady=10)

# Text widget with Vertical and Horizontal Scrollbars for CSV data display
data_text = Text(frame, wrap="none", height=12, width=80)
data_text.grid(row=0, column=0, sticky="nsew")

data_v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=data_text.yview)
data_v_scrollbar.grid(row=0, column=1, sticky="ns")
data_text.configure(yscrollcommand=data_v_scrollbar.set)

data_h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=data_text.xview)
data_h_scrollbar.grid(row=1, column=0, sticky="ew")
data_text.configure(xscrollcommand=data_h_scrollbar.set)

# Frame for the correlation data
frame2 = ttk.Frame(window, width=400, height=200)
frame2.grid(row=3, column=0, columnspan=2, pady=10)

# Entry widget and button for running correlations
dependent_variable_entry = Entry(width=40,font=("Arial", 15, "normal"))
dependent_variable_entry.grid(row=2, column=0, pady=10, sticky="w")
add_placeholder(dependent_variable_entry, "Input dependent variable...")

run_correlations_button = Button(window, text="Run\n Correlation",font=("Arial", 15,"normal"),
                                 activebackground="blue", bg="white", command=correlation)
run_correlations_button.grid(row=2, column=1, pady=10)

# Text widget with Vertical and Horizontal Scrollbars for Correlation Matrix display
correlation_text = Text(frame2, wrap="none", height=13, width=80)
correlation_text.grid(row=0, column=0, sticky="nsew")

correlation_v_scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=correlation_text.yview)
correlation_v_scrollbar.grid(row=0, column=1, sticky="ns")
correlation_text.configure(yscrollcommand=correlation_v_scrollbar.set)

correlation_h_scrollbar = ttk.Scrollbar(frame2, orient="horizontal", command=correlation_text.xview)
correlation_h_scrollbar.grid(row=1, column=0, sticky="ew")
correlation_text.configure(xscrollcommand=correlation_h_scrollbar.set)

# Frame for the plot
frame3 = ttk.Frame(window, width=200, height=500)
frame3.grid(row=0, column=2, rowspan=4, pady=10, sticky="nsew")  # Allow frame3 to expand

set_default_text()

window.mainloop()
