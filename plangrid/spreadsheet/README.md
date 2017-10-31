# Programming task: Spreadsheet 

## Approach

1. Read input CSV
1. Compute web of cell precedents and dependents
1. Find cells with no unknown precedents, compute them, and mark their dependents as now having known precedent values.
1. Continue until all cells are computed. 

### How to run

* Save sample_input.csv, main.py, and helpers.py in the same folder. 
* run main.py

### Improvements

* Alert on specific error conditions (circular reference, out of bounds references, bad input formula)
* Handle csv's wider than 26 columns
* Expand tests

## Assignment

This task is designed to help us understand how you solve problems, how you translate your ideas into code, and how you model and structure a non­trivial programming project. You can complete this task in a programming language of your choice, but please check with us if that’s not one of Java, Scala, Javascript, Python, Swift, C++, or Go. You should expect to spend about 2 hours on this problem.

### Requirements

1. Write a program which parses a spreadsheet­-like CSV file and evaluates each cell by these rules: 
1. Each cell is an expression in postfix notation (see Wikipedia). 
1. Each token in the expression will be separated by one or more spaces. 
1. Expressions may include the basic arithmetic operators +, ­, *, / 
One cell can refer to another cell with the {LETTER}{NUMBER} notation (e.g. “A2”, “B4”– letters refer to columns, numbers to rows). 

Your program should output another CSV file of the same dimensions containing the results of evaluating each cell to its final value. If any cell is an invalid expression, then for that cell only ​print #ERR. 

For example, for the following CSV input: 

    b1 b2 + ,2 b2 3 * -­ ,3 ,+ 
    a1      ,5          ,  ,7 2 / 
    c2 3 *  ,1 2        ,  ,5 1 2 + 4 * + 3 -

...output something like: 

    -8, -­13,   3, #ERR ­
    -8, 5,     0, 3.5 
    0,  #ERR,  0, 14 

There are other error conditions that your implementation should detect and handle in a manner you think appropriate. 

### Solution guide 

* To ensure quick turnaround on your homework evaluation, please include a readme file with instructions on how to build and run your application from the command line (do not submit a Jupyter notebook).
* We are looking for well written, tested, and structured code; don’t rush. If you have to choose between completely implementing the requirements and good architecture/automated tests, choose the latter.
* Use only what is available in the standard and most commonly-used extension libraries for your platform.
* Where some detail of the task is unspecified, use your best judgement. Assumptions or limitations in your implementation are fine, but please document them.
