# **BrokoliSQL**

**BrokoliSQL** is a Python script designed to facilitate the conversion of CSV and Excel files into SQL insertion commands. It reads a CSV or Excel file and generates SQL `INSERT INTO` commands based on the columns in the file. The generated commands are then written to a specified output file.

## **How It Works**

**BrokoliSQL** works in a simple and intuitive way. It allows you to insert data from CSV or Excel files directly into a SQL database, without the need to manually perform the insertion.

### **Execution Flow**

1. The script reads an input CSV or Excel file.
2. It normalizes the column names to ensure they are in the appropriate format for SQL (e.g., converting `Name Id` to `Name_ID`).
3. The script automatically infers the column types (such as `INTEGER`, `TEXT`, etc.).
4. It generates SQL `INSERT INTO` commands for each row in the file.
5. The SQL commands are written to an output file, ready to be executed in a database.

### **How to Use**

To use **BrokoliSQL**, you can run the script directly from the command line. Here’s the basic syntax:

```bash
python cli.py --input <path_to_input_file> --output <path_to_output_file> --table <table_name>
```

#### **Arguments:**

- `--input`: Path to the input CSV or Excel file.
- `--output`: Path to the output file where SQL commands will be generated.
- `--table`: Name of the SQL table where the data will be inserted.

### **Example Usage**

```bash
python cli.py --input data.csv --output commands.sql --table products
```

This will generate SQL commands to insert the data from `data.csv` into the `products` table, and save the commands in the `commands.sql` file.

You can install BrokoliSQL directly from [PyPI](https://pypi.org/) using pip:

```bash
pip install brokolisql
```

## Usage

Once installed, you can use the `brokolisql` command in your terminal:

```bash
brokolisql --input path/to/your/file.csv --output output.sql --table your_table_name
```

### Example:

```bash
brokolisql --input data/users.xlsx --output sql/users.sql --table users
```

### **Prerequisites**

Make sure you have Python 3 installed on your system. You can check the Python version by running:

```bash
python --version
```

Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

### **Project Structure**

The project is organized as follows:

```
BrokoliSQL/
│
├── cli.py                # Main command line script
├── requirements.txt      # Dependencies file
├── utils/                # Utility functions (e.g., file loading)
│   └── file_loader.py    # Loads CSV/Excel files and normalizes data
├── services/             # Service functions (e.g., SQL generation)
│   ├── sql_generator.py  # Generates SQL commands
│   └── normalizer.py     # Normalizes column names
├── output/               # Output functions
│   └── output_writer.py  # Writes SQL commands to a file
├── .gitignore            # Files and folders to be ignored by Git
├── banner.txt            # Text-based banner displayed on execution
└── README.md             # This file
```

### **Contributing to the Project**

If you want to contribute to **BrokoliSQL**, follow these steps:

1. **Fork the Repository**: Fork the repository to your GitHub account.
2. **Clone the Repository**: Clone the repository to your local machine.

   ```bash
   git clone https://github.com/your_username/brokolisql.git
   ```

3. **Create a Branch**: Create a new branch for your changes.

   ```bash
   git checkout -b my-new-feature
   ```

4. **Make Changes**: Make the desired changes to the code. Be sure to follow the coding conventions and best practices.

5. **Tests**: Add tests to ensure your changes don’t break existing functionality. Test the script to make sure it works as expected.

6. **Commit and Push**: After making your changes, commit and push them to the remote repository.

   ```bash
   git add .
   git commit -m "feat(postgres): Add support to postgres"
   git push origin my-new-feature
   ```

7. **Create a Pull Request**: Open a pull request explaining your changes and why they are necessary.

### **Code Standards**

- **Code Style**: Use the PEP 8 coding style for Python.
- **Function and Variable Names**: Use clear and descriptive names.
- **Tests**: Add unit tests wherever possible to validate the features.

### **License**

This project is licensed under the **GPL-3.0**. Please refer to the [LICENSE](LICENSE) file for more details.

---

**BrokoliSQL** simplifies inserting data from CSV and Excel files into SQL databases, and we welcome contributions! If you find a bug or have an improvement suggestion, feel free to open an **issue** or a **pull request**.

---