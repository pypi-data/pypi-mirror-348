![Py Carousel Greedy Logo](https://raw.githubusercontent.com/CarmineCerrone/py_carouselgreedy/refs/heads/main/cglogo.png)
# Py Carousel Greedy

**A modular and user-friendly Python implementation of the Carousel Greedy algorithm.**

`py-carouselgreedy` is the first open-source Python library designed specifically for the Carousel Greedy algorithm, a flexible metaheuristic for solving a wide variety of combinatorial optimization problems. The library was developed with a focus on ease of use, modularity, and integration into experimental pipelines.

> 📄 Introduced in the Conference Paper:  
> *Carousel Greedy: From Drone Photogrammetry to Social Network Analysis, A Systematic Survey and the First Open-Source Python Library*  
> Raffaele Dragone, Carmine Cerrone, Bruce L. Golden  
> Presented at ODS 2025

---

## ✨ Features

- Easy to use: define only a feasibility function and a greedy function.
- Modular and lightweight: no external dependencies.
- Adaptable to any discrete optimization problem (e.g. vertex cover, knapsack, influence maximization).
- Includes ready-to-use examples for common problems.
- Fully documented and tested.

---

## 🚀 Installation

Install from PyPI:

```bash
pip install py_carouselgreedy
```


---

## 🔧 Usage Example

```python
from py_carouselgreedy import carousel_greedy

def my_feasibility(cg_instance, solution):
    # Return True if solution is feasible
    return ...

def my_greedy(cg_instance, solution, candidate):
    # Return a score for the candidate
    return ...

cg = carousel_greedy(
    candidate_elements=[...],
    test_feasibility=my_feasibility,
    greedy_function=my_greedy
)

best_solution = cg.minimize(alpha=10, beta=0.2)
```

---

## 📂 Examples

You can find full working examples in the `examples/` folder:

- `minimum_vertex_cover.py`
- `minimum_label_spanning_tree.py`

Each example shows how to define a problem-specific greedy function and feasibility check using NetworkX or standard Python structures.

---

## 🛠️ Function Parameters and Customization

When creating a `CarouselGreedy` instance, two user-defined functions must be provided:

- `test_feasibility(cg_instance, solution)`
- `greedy_function(cg_instance, solution, candidate)`

These functions encapsulate the problem-specific logic and allow the algorithm to be used for a wide range of optimization problems.

### 🔁 `cg_instance`: Passing Problem Data

You can optionally pass a custom `data` object when instantiating the `carousel_greedy` class:

```python
cg = carousel_greedy(
    candidate_elements=...,
    test_feasibility=my_feasibility,
    greedy_function=my_greedy,
    data=your_custom_data  # optional
)
```

This `data` object can store any useful information (e.g., a graph, cost matrix, etc.) and is accessible inside the two functions through `cg_instance.data`.

### ✅ Feasibility Function

```python
def my_feasibility(cg_instance, solution):
    ...
```

- `cg_instance`: instance of `carousel_greedy` class (with access to `.data`).
- `solution`: the current set of selected elements.
- **Returns**: `True` if the current solution is feasible, `False` otherwise.

### 🔍 Greedy Function

```python
def my_greedy(cg_instance, solution, candidate):
    ...
```

- `cg_instance`: instance of `CarouselGreedy`.
- `solution`: the current partial solution.
- `candidate`: the element under evaluation.
- **Returns**: a real-valued score (higher = more promising).

The **feasibility function must return a boolean**, and the **greedy function must return a real number**, which is used to guide the greedy selection. The candidate with the highest score is selected at each step.

---

## 📖 Algorithm Overview

The Carousel Greedy algorithm is composed of four phases:

1. **Greedy Construction** – builds an initial solution.
2. **Removal Phase** – removes a portion of it (based on β).
3. **Iterative Phase** – removes and adds elements (based on α).
4. **Completion Phase** – restores feasibility if necessary.

Users only need to define two functions:
- `greedy_function(cg_instance, solution, candidate)`
- `test_feasibility(cg_instance, solution)`

---

## 🧑‍🔬 Citation

If you use this library in your research, please cite:

```bibtex
@inproceedings{dragone2025carousel,
  title={Carousel Greedy: From Drone Photogrammetry to Social Network Analysis, A Systematic Survey and the First Open-Source Python Library},
  author={Dragone, Raffaele and Cerrone, Carmine and Golden, Bruce L.},
  booktitle={Optimization and Decision Science (ODS)},
  year={2025}
}
```

---

## 📬 Contact & Contributions

Pull requests are welcome. For major changes, please open an issue first.

Questions? Suggestions? Reach out to:

- `raffaele.dragone@edu.unige.it`

---

## 📄 License

This project is licensed under the **BSD 3-Clause License**.  
See the [LICENSE](./LICENSE) file for details.
