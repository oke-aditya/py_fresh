# How to structure the code ?

- The `src` folder provides a generic implementation of a python API.

```
app.py        Your flask / FastAPI / Django app.
engine.py     Main logic of the problem you want to solve.
utils.py      All utility functions required.
config.py     Configurable parameters or re-usable global variables.
data.py       Database connections or data loading utilities.
model.py      Django or Machine Learning models you want to use.
train.py      Traning the models (for ML projects)
predict.py    Predicting using the models (for ML projects)
```

- It is important to include `__init__.py` folder otherwise the package will not be able to import
functions / classes.

- In the `__init__.py` folder import stuff as you need. E.g. `from project.src.app import *`

- Use imports from `project` try to avoid relative imports. This is a better practice.

