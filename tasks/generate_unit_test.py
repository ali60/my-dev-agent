import os
from configuration.config import config
from models.model_manager import ModelManager

class BulkUnitTestGenerator:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def unit_test_code(self, input_text):
        prompt = f"Write a unit test for this code using unittest, following the given/then/when structure:\n{input_text}"
        return self.model_manager.invoke_model(prompt)

    def generate_tests_for_files(self, source_dir, tests_dir, allowed_dirs):
        for root, dirs, files in os.walk(source_dir):
            # Check if the current directory is one of the allowed directories
            relative_root = os.path.relpath(root, start=source_dir)
            if relative_root in allowed_dirs:
                for file in files:
                    if file.endswith(".py") and not file.endswith("_test.py"):
                        source_file_path = os.path.join(root, file)
                        # Skip empty files
                        if os.path.getsize(source_file_path) < 2:
                            print(f"Skipping empty file: {source_file_path}")
                            continue                        # Read the content of the source file
                        with open(source_file_path, "r") as f:
                            input_text = f.read()
                        # Generate unit test code based on the source file content
                        print(f"Writing unit test for {file}")
                        test_code = self.unit_test_code(input_text)
                        # Create the corresponding test file
                        self.create_test_file(source_file_path, tests_dir, test_code)

    def create_test_file(self, source_file_path, tests_dir, test_code):
        # Construct the name for the test file
        relative_path = os.path.relpath(source_file_path, start=".")
        test_file_path = os.path.join(
            tests_dir, relative_path.replace(".py", "_test.py")
        )

        # Create the directory for tests if it doesn't exist
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

        # Write the generated test code to the test file
        with open(test_file_path, "w") as f:
            f.write(test_code)


# Example usage:
if __name__ == "__main__":
    model_manager = ModelManager(config)
    unit_test_generator = BulkUnitTestGenerator(model_manager=model_manager)
    
    source_directory = "."  # The root source directory
    tests_directory = "tests"  # The target tests directory
    
    # Specify the allowed folders relative to the source directory
    allowed_folders = ['configuration', 'models', 'service', 'tasks']

    unit_test_generator.generate_tests_for_files(source_directory, tests_directory, allowed_folders)
