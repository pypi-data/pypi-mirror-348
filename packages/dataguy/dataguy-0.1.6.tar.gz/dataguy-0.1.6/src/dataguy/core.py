import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from claudette import Chat, models
from .context_manager import ContextManager
import ast
from dataguy.utils import LLMResponseCache
import builtins
from typing import Optional, Dict, Any

def call_chat(chat_instance, *args, **kwargs):
    return chat_instance(*args, **kwargs)

class DataGuy:
    """
    An automatic tool for describing, analyzing and plotting data.
    It uses an LLM model to generate lambda functions for various data analysis methods.
    Its execution checks if the code has an error, and generates it again, by feeding the old code back together with the error.
    """
    def __init__(self, max_code_history=100, model_overrides: Optional[Dict[str, Any]] = None, auto_model_switch=True):
        self.context = ContextManager(max_code_history=max_code_history)
        self.data = None
        self._data_description = None
        self.model_overrides = model_overrides or {}
        self.auto_model_switch = auto_model_switch

        self.prompts = {
            "code": "You write Python code for pandas and matplotlib tasks.",
            "text": "You explain datasets and their structure clearly.",
            "image": "You describe uploaded data visualizations clearly, so plot can be recreated based on that."
        }

        self.cache=LLMResponseCache()

    def _select_model(self, mode, data=None):
        """
        Selects if it's an image or a text
        :param mode: a string to decide whether it is an image or text
        :return: returns the appropriate model
        """
        # 1. use override if given
        if mode in self.model_overrides:
            return self.model_overrides[mode]

        # 2. auto-switch logic
        if self.auto_model_switch and mode == "code" and data is not None:
            if isinstance(data, pd.DataFrame) and (data.shape[0] > 100_000 or data.shape[1] > 100):
                print("[Model use] The uploaded dataset is large. Switching to 'haiku' for performance.")
                for m in models:
                    if "haiku" in m:
                        return m

        # 3. fallback preferences by mode
        preferences = {
            "image": ["opus", "sonnet", "haiku"],
            "text": ["sonnet", "haiku"],
            "code": ["sonnet", "haiku"]
        }

        # Search preferences in order
        for preferred in preferences.get(mode, []):
            for m in models:
                if f"claude-3-{preferred}" in m:
                    return m

        # 4. last resort
        return models[-1]

    def _generate_code(self, task: str) -> str:
        """
        A code generator, that takes the context, and the task given by a text,
        sends it to the LLM, and generates the code.
        It also checks if the LLM generated code is valid.
        :param task: a string describing the task
        :return: a python code as a string
        """
        prompt = self.context.get_context_summary() + "\n# Task: " + task + "The dataset you're using is named data, trying with other names will likely error."
        model = self._select_model("code", data=self.data)
        chat = Chat(model, sp=self.prompts["code"])
        resp = call_chat(chat, prompt)

        # Safely extract LLM response
        try:
            raw = resp.content[0].text
        except (AttributeError, IndexError, TypeError) as e:
            raise ValueError(f"Invalid LLM response format: {resp}") from e

        match = re.search(r'```(?:python)?\n(.*?)```', raw, re.S)
        if match:
            extracted_code = match.group(1).strip()
        else:
            extracted_code = raw.strip()

        if not extracted_code:
            raise ValueError("No code found in LLM response.")

        return extracted_code

    def _is_safe_code(self, code_str):
        """
        Checks if the code can run, or is it safe to run. It blocks certain modules,
        that we now people can use to mess with their computer. The others are general,
        and often used modules that are safe to run. Unknown modules are assumed to be unsafe.
        :param code_str: Python code as a string
        :return: a boolean indicating if the code can run or is safe to run
        """
        SAFE_MODULES = {"numpy", "pandas", "matplotlib", "sklearn","math","random","seaborn",
                        "scipy","pyPCG","imblearn","xgboost","signal"}#would need a lot of expanding
        BLOCKED_MODULES = {"os", "sys", "subprocess", "builtins", "shutil"}

        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if module_name in BLOCKED_MODULES:
                            print(f"Blocked unsafe import: {module_name}")
                            return False
                        if module_name not in SAFE_MODULES:
                            print(f"Import of unknown module {module_name} blocked.")
                            return False

                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module.split('.')[0] if node.module else ""
                    if module_name in BLOCKED_MODULES:
                        print(f"Blocked unsafe from-import: {module_name}")
                        return False
                    if module_name not in SAFE_MODULES:
                        print(f"From-import of unknown module {module_name} blocked.")
                        return False

                elif isinstance(node, (ast.Global, ast.Nonlocal)):
                    print(f"Blocked unsafe node: {type(node).__name__}")
                    return False
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'exec':
                    print("Blocked unsafe function call: exec()")
                    return False

            return True

        except SyntaxError as e:
            print(f"Syntax error during AST check: {e}")
            return False

    def _exec_code(self, code: str, retries_left=3) -> dict:
        """
        The code executor function. It takes the code, inspects it with _is_safe_code,
        then it tries to run, and if it detects an error, it sends back to the _generate_code,
        along with the error message, and executes again.
        :param code: The generated code, that it will attempt to execute.
        :param retries_left: The number of recursions it allows for self mending.
        :return:
        """
        print("Executing code:\n", code)

        safe_globals = {
            "__builtins__": builtins,
            "pd": pd,
            "np": np,
            "plt": plt,
        }
        local_ns = {"data": self.data}
        base = set(local_ns)

        if not self._is_safe_code(code):
            print("Unsafe code detected. Execution aborted.")
            return {"error": "Unsafe code detected and blocked."}

        try:
            exec(code, safe_globals, local_ns)
        except (SyntaxError, Exception) as e:
            print(f"Error during code execution: {e}")

            if retries_left <= 0:
                return {"error": f"Execution failed after retries: {e}"}

            fix_task = (
                "The following code failed with this error:\n"
                f"{e}\n\n"
                "Original code:\n"
                f"{code}\n\n"
                "Please fix the code."
                "Ensure all variables are defined in the code."
                "Include all necessary imports and data loading."
                "Do not assume any variables exist beforehand."
            )

            # Re-generate code using error feedback
            new_code = self._generate_code(fix_task)
            print(f"Retrying with corrected code (retries left: {retries_left-1})...")
            return self._exec_code(new_code, retries_left=retries_left - 1)
        else:
            self.context.add_code(code)
            self.context.update_from_globals(local_ns)
        finally:
            self.context.update_from_globals(local_ns)

        new_keys = set(local_ns) - base
        return {k: local_ns[k] for k in new_keys if not k.startswith('__')} | \
               {'data': local_ns['data']} if 'data' in local_ns else {}

    def set_data(self, obj):
        """
        Imports the data into the structure.
        :param obj: An object to be imported, it can be many types, such as pd, np, a string to import from csv, bytes or pandas
        :return: Returns a pandas dataframe that was set to be the data, so you can check if it imported properly.
        """
        if isinstance(obj, pd.DataFrame):
            self.data = obj.copy()

        elif isinstance(obj, (dict, list, np.ndarray)):
            self.data = pd.DataFrame(obj)

        elif isinstance(obj, str) and obj.endswith('.csv'):
            self.data = pd.read_csv(obj)

        elif isinstance(obj, bytes):
            from io import BytesIO
            self.data = pd.read_csv(BytesIO(obj))

        elif hasattr(obj, 'to_pandas'):  # fallback for other dataframes
            self.data = obj.to_pandas()

        else:
            raise TypeError(f"Unsupported data type: {type(obj)}")

        self.context.update_from_globals({"data": self.data})
        return self.data

    def summarize_data(self):
        """
        Generates a summary of the data.
        :return: The shape, columns, missing count and means of the data.
        """
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'missing_counts': self.data.isna().sum().to_dict(),
            'means': self.data.mean(numeric_only=True).to_dict()
        }


    def describe_data(self) -> str:
        """
        Creates a description of the data, from the summary. Caches the response,
        so it doesn't make unnecessary API calls.
        :return: A string description of the data.
        """
        summary = self.summarize_data()
        prompt = (
            "Describe the dataset in a few sentences based on the following summary:\n"
            f"{summary}"
        )

        cached_resp = self.cache.get(prompt)
        if cached_resp:
            resp_text = cached_resp
        else:
            model = self._select_model("text")
            chat = Chat(model, sp=self.prompts["text"])
            resp = call_chat(chat, prompt)
            resp_text = resp.content[0].text
            self.cache.set(prompt, resp_text)

        self.context.add_code(f"# Description: {resp_text}")
        self._data_description=resp_text
        return resp_text

    def wrangle_data(self) -> pd.DataFrame:
        """
        Calls the _generate_code function with the task to write a wrangler lambda function,
         to clean up the data. Then it calls the _execute_code function.
        :return: Sets the data to the cleaned up version, and returns that.
        """
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        summary = self.summarize_data()
        desc = self.describe_data()
        task = (
            "Write a lambda function named `wrangler` that takes a pandas DataFrame and wrangles it for analysis.\n"
            f"Summary: {summary}\n"
            f"Description: {desc}"
        )
        code = self._generate_code(task)
        ns = self._exec_code(code)
        wrangler = ns.get('wrangler')
        if callable(wrangler):
            self.data = wrangler(self.data)
        return self.data

    def analyze_data(self):
        """
        Analyzes the data stored in DataGuy.
        :return: Returns a result dictionary, with shape, column, and descriptive stats.
        """
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")

        task = "Analyze the pandas DataFrame `data` and return a dict `result` with shape, columns, and descriptive stats."
        code = self._generate_code(task)
        ns = self._exec_code(code)

        result = ns.get('result')
        if result is None:
            print("Warning: LLM-generated code did not return a 'result'.")
            result = {"error": "No result returned by analysis code."}

        return result

    def plot_data(self, column_x: str, column_y: str):
        """
        Creates a scatterplot.
        :param column_x: Horizontal column name.
        :param column_y: Vertical column name.
        :return: Nothing, just executes the code.
        """
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        task = f"Create a scatter plot of `data` with x='{column_x}' and y='{column_y}'. Use matplotlib."
        code = self._generate_code(task)
        self._exec_code(code)

    def describe_plot(self, img_bytes: bytes) -> str:
        """
        Creates a detailed description from the given plot.
        :param img_bytes: The image converted to bytes.
        :return: A text description of the plot.
        """
        model = self._select_model("image")
        chat = Chat(model, sp=self.prompts["image"])
        resp = call_chat(chat, ([img_bytes,"Please describe this plot in detail so that it can be faithfully recreated in Python using matplotlib.Include ALL of the following in your description: 1. The type of plot (scatter, line, bar, etc.) 2. The variables plotted on X and Y axes (including units if visible) 3. The number of data points shown 4. The axis ranges (min and max for X and Y) 5. Any grouping or color coding used (legend categories) 6. Any markers, shapes, or line styles used 7. Any annotations or text present 8. The general pattern or trend visible 9. Figure size or aspect ratio if visible 10. Anything else visible that affects interpretation. Be precise and exhaustive. Do not assume anything; describe only what is visible.This description will be used to write Python code to recreate the plot as closely as possible."]))
        desc = resp.content[0].text
        self.context.add_code(f"# Plot description: {desc}")
        return desc

    def recreate_plot(self, plot_description: str):
        """
        Takes in a description made by describe_plot, and tries to recreate it using the data.
        :param plot_description: Text description of the plot.
        :return: Nothing, it just executes the code.
        """
        if self.data is None:
            raise ValueError("No data loaded. Use set_data() first.")
        # incorporate wrangled summary and dataset description
        summary = self.summarize_data()
        desc = self._data_description or ""
        task = (
            "Write Python code using pandas and matplotlib to create a plot for 'data' similar to the description below. It is a different dataset.\n"
            f"the data is in the variable data_to_plot\n"
            f"Dataset summary: {summary}\n"
            f"Dataset description: {desc}\n"
            f"Plot description: {plot_description}"
        )
        code = self._generate_code(task)
        self._exec_code(code)
