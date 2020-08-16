# What is this repo

This reposytorium contains programs, which were intented to verify a conjecture about a specific property of small weak epsilon-nets.


# How to use (Linux/MAC)

Clone this repositorium and install or-tools for Python. 
Make sure Python3 is installed on Your computer.
```
git clone git@github.com:erheron/grid-conjecture.git && cd grid-conjecture
python3 -m venv ortools
source ortools/bin/activate
python3 -m pip install ortools
```


Run ```gen4.cpp``` which (for nets for size 4) generates the set G of inclusion-minimal sets of rectangles, which cannot be hit by any net.

```
cd grid-conjecture
g++ -O4 gen4.cpp -o gen4
./gen4 > input.txt &
```

Next, run LP solver, which will take a few hours. You can pass ```--terminate``` option, and in that case the program will end after it finds first counterexample.

```
python3 lp-solver.py [--terminate] input.txt 4 > examples.out &

```

In ```examples.out``` there will be all counterexamples for ```k=4```.
