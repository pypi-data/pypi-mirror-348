# DataGuy

**DataGuy** is a Python package designed to simplify data science workflows by leveraging the power of Large Language Models (LLMs). It provides tools for automated data wrangling, intelligent analysis, and AI-assisted visualization, making it ideal for small-to-medium datasets.

- **GitHub**: [View the source code on GitHub](https://github.com/magistak/llm-data)
- **PyPI**: [Install from PyPI](https://pypi.org/project/dataguy)
- **Documentation**: [Read the full documentation](https://dataguy.readthedocs.io)
- **Demo**: [Try the demo](https://colab.research.google.com/drive/1RhLC0b4RN1kVKAh3NqNPn_Axlc0Rn3L8?usp=sharing)

## Features

- **Automated Data Wrangling**: Clean and preprocess your data with minimal effort using LLM-generated code.
- **AI-Powered Data Visualization**: Generate insightful plots and visualizations based on natural language descriptions.
- **Intelligent Data Analysis**: Perform descriptive and inferential analysis with the help of LLMs.
- **Customizable Workflows**: Integrate with pandas, matplotlib, and other Python libraries for seamless data manipulation.
- **Safe Code Execution**: Built-in safeguards to ensure only safe and trusted code is executed.

## Installation

Install the package using pip:

```bash
pip install dataguy
```

## Usage

### Getting Started

0. **Load Anthrpic API key in your environment**:
   ```python
   import os
   os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"
   ```
   Replace `your_api_key_here` with your actual API key from Anthropic.

1. **Import the Package**:
   ```python
   from dataguy import DataGuy
   ```

2. **Initialize a DataGuy Instance**:
   ```python
   dg = DataGuy()
   ```

3. **Load Your Data**:
   ```python
   import pandas as pd
   data = pd.DataFrame({"age": [25, 30, None], "score": [88, 92, 75]})
   dg.set_data(data)
   ```

4. **Summarize Your Data**:
   ```python
   summary = dg.summarize_data()
   print(summary)
   ```

5. **Wrangle Your Data**:
   ```python
   cleaned_data = dg.wrangle_data()
   ```

6. **Visualize Your Data**:
   ```python
   dg.plot_data("age", "score")
   ```

7. **Analyze Your Data**:
   ```python
   results = dg.analyze_data()
   print(results)
   ```

### Example Workflow

```python
from dataguy import DataGuy
import pandas as pd

# Initialize DataGuy
dg = DataGuy()

# Load data
data = pd.read_csv("path/to/data.csv")
dg.set_data(data)

# Summarize data
summary = dg.summarize_data()
print("Data Summary:", summary)

# Wrangle data
cleaned_data = dg.wrangle_data()

# Visualize data
dg.plot_data("column_x", "column_y")

# Analyze data
analysis_results = dg.analyze_data()
print("Analysis Results:", analysis_results)
```

## Key Methods

- **`set_data(obj)`**: Load data into the `DataGuy` instance. Supports pandas DataFrames, dictionaries, lists, numpy arrays, and CSV files.
- **`summarize_data()`**: Generate a summary of the dataset, including shape, columns, missing values, and means.
- **`wrangle_data()`**: Automatically clean and preprocess the dataset for analysis.
- **`plot_data(column_x, column_y)`**: Create a scatter plot of two columns using matplotlib.
- **`analyze_data()`**: Perform an automated analysis of the dataset, returning descriptive statistics and insights.

## Requirements

- Python 3.8 or higher
- Dependencies:
  - pandas
  - numpy
  - matplotlib
  - scikit-learn
  - claudette
  - anthropic

## Contributing

Contributions are welcome! Please submit issues or pull requests via the [GitHub repository](https://github.com/magistak/llm-data).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

- István Magyary
- Sára Viemann
- Kristóf Bálint

For inquiries, contact: magistak@gmail.com