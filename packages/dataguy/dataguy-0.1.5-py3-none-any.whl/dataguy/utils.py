def validate_file_path(file_path):
    """
    Validate that a file exists and is readable.

    Args:
        file_path (str): Path to the file to validate

    Returns:
        bool: True if file exists and is readable

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file isn't readable
    """
    import os

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"File is not readable: {file_path}")

    return True


class LLMResponseCache:
    """
    A response cacher for the LLM prompts. This is for not calling the API too many times.
    """
    def __init__(self):
        self.cache = {}

    def get(self, prompt):
        """
        Getter
        :param prompt:
        :return:
        """
        return self.cache.get(prompt)

    def set(self, prompt, response):
        """
        Setter
        :param prompt:
        :param response:
        :return:
        """
        self.cache[prompt] = response

    def get_or_set(self, prompt, llm_function):
        """
        Getter or Setter
        :param prompt:
        :param llm_function:
        :return:
        """
        if prompt in self.cache:
            return self.cache[prompt]
        response = llm_function(prompt)
        self.cache[prompt] = response
        return response

    def save_to_file(self, filepath):
        """
        Save the response to a JSON file.
        :param filepath:
        :return:
        """
        import json
        with open(filepath, 'w') as f:
            json.dump(self.cache, f)

    def load_from_file(self, filepath):
        """
        Load the response from a JSON file.
        :param filepath:
        :return:
        """
        import json
        import os
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.cache = json.load(f)
