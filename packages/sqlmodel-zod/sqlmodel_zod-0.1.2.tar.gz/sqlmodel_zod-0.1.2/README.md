# SQLModel Zod Generator
A cli generator script to convert SQLModels into Zod schemas.


## Installation
```bash
pip install sqlmodel-zod
```

## Usage
Run the command with the relative path to the directory where your models are stored. The output will be a single file named `zod_schemas.js` with all model definitions.

```bash
sqlmodel-zod /path/to/model/directory
```
