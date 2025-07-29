# bit_collision_free_MF

A Python package for generating molecular fingerprints without bit collisions.

## Description

`bit_collision_free_MF` generates Morgan fingerprints while eliminating bit collisions, which can significantly improve the accuracy and reliability of molecular fingerprints in cheminformatics applications. The package automatically determines the optimal fingerprint length to ensure that each structural feature maps to a unique bit in the fingerprint.

## Installation

### Requirements

- Python 3.9 or higher
- numpy
- pandas
- rdkit

### Simple Installation

```bash
pip install -U bit_collision_free_MF
```

This will automatically install all dependencies, including RDKit.

### Manual Installation

```bash
# Install dependencies
pip install numpy pandas rdkit

# Install the package
pip install -U bit_collision_free_MF  
```

For development installation:
```bash
# Clone the repository
git clone https://github.com/Shifa-Zhong/bit_collision_free_MF.git
cd bit_collision_free_MF

# Install in development mode
pip install -e .
```

## Features

- Automatically determines the optimal fingerprint length to avoid bit collisions
- Supports custom fingerprint radius
- Option to remove zero-value columns
- Easy CSV export with customizable headers
- Seamless integration with pandas and NumPy

## Usage

### Basic Usage

```python
from bit_collision_free_MF import generate_fingerprints, save_fingerprints
import pandas as pd

# Load your data
data = pd.read_csv('your_molecules.csv')

# Generate fingerprints
fingerprints, fp_generator = generate_fingerprints(
    data, 
    smiles_column='smiles',
    radius=1,
    remove_zero_columns=True
)

# Save fingerprints to CSV
save_fingerprints(
    fingerprints,
    fp_generator,
    output_path='path/to/output.csv',
    include_header=True
)
```

### Using the CollisionFreeMorganFP Class Directly

```python
from bit_collision_free_MF import CollisionFreeMorganFP
import pandas as pd

# Load your data
data = pd.read_csv('your_molecules.csv')
smiles_list = data['smiles'].tolist()

# Create and fit the fingerprint generator
fp_generator = CollisionFreeMorganFP(radius=1)
fp_generator.fit(smiles_list)

# Generate fingerprints
fingerprints = fp_generator.transform(smiles_list, remove_zero_columns=True)

# Get feature names
feature_names = fp_generator.get_feature_names()

# Create a DataFrame with the fingerprints
result_df = pd.DataFrame(fingerprints, columns=feature_names)

# Save to CSV
result_df.to_csv('fingerprints.csv', index=False)
```

## License

MIT License

Copyright (c) 2025 Shifa Zhong; Jibai Li

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact

For academic inquiries or collaboration, please contact:
- Shifa Zhong (sfzhong@tongji.edu.cn)
- Jibai Li (51263903065@stu.ecnu.edu.cn)