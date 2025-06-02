# BlackJack
<sub>Final Project (Group 5), Introduction to AI, Spring 2025, NYCU</sub>

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
Many casino games that we see and hear of rely purely on skill—examples include the famous roulettes, slots, etc.—however, Blackjack stands out as one in only a handful of games where strategy matters.

In September 1956, a paper titled *The Optimum Strategy in BlackJack* was released by Baldwin et al., calculating the optimum play for every hand; six years later, Edward Thorp published his book  *Beat the Dealer: A Winning Strategy for the Game of Twenty-One*, where he used an IBM computer (the IBM 704, using Fortran) to fine-tune the math.

## 🚀 Installation
### 💻 Cloning the Repository
First, clone the repository to your local machine using Git:
```bash
git clone [https://github.com/clotpoledollophead/21-2u03.git](https://github.com/clotpoledollophead/21-2u03.git)
cd 21-2u03
```
### 🔧 Install Dependencies
We recommend using a virtual environment in your command line before installing dependencies:

1. Create a virtual environment
```bash
python -m venv blackjack_venv
```

2. Activate the virtual environment
```bash
# For Windows
.\blackjack_venv\Scripts\activate
```

```bash
# For macOs/Linux
source blackjack_venv/bin/activate
```

## ▶️ Usage
Once you've completed the [Installation](#-installation) steps, you can run the Blackjack AIs.
### 🏃‍♂️ Running
Navigate to the expectimax folder, and run the following code: 
```python
python main.py -n 1000 -rn 1000 -a -s
```
Navigate to the machine_learning folder, and run the following code:

train RFC model
```python
python train_rfc_agent.py
```
train NEAT model
```python
python train_neat_agent.py
```
Run the experiment 
```python
python main.py
```
Run the small game application
```python
python blackjack_gui.py
```

