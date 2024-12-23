# Days worth to note in 2022

## Day 4

[Day 4](4/README.md)

Overlapping sections and their aggregation into one

## Day 8

[Day 8](8/README.md)

2D matrix traversal with a "visibility" counting - so number of trees "higher" than previous one (in a particular
direction)

## Day 10

[Day 10](10/README.md)

In Part I you have to implement a code, then in Part II it will create an Asii ART - that present a world - a key

## Day 11

[Day 11](11/README.md)

Calculations of a Monkey and their worry level. The problem is the worry level is always increased by each item, so in
each round it's only growing. All the calculations are made base on fact that all tests are made by checking if a number
is "divisible" - so looking for a LCM of all "dividers" will help you decrease it

Instead you can simply get an error:

```
ValueError: Exceeds the limit (4300) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
```

## Day 13

[Day 13](13/README.md)

You need to parse and compact a strange notation for an expression like:

```
[[1],[2,3,4]]
[[1],4]
```

You need to compare if they are equal

## Day 14

[Day 14](14/README.md)

You build a map of 2D path, and then simulate sand failing from the top - it will land on a stable surface or move on
left/right. Then you count how much sand left...

## Day 15

[Day 15](15/README.md)

You need to find out a "blind spots" between sonars - to calculate it you have to use a Manhattan distance. I bruteforce
it but probably there is a better idea.

TODO: Check better options in a future

## Day 16

[Day 16](16/README.md)

DP problem - you have to count a different number of paths but under a condition that already opened valves are
generating energy. So elephants can either go from point of the Graph to a second point - or wait 1 round and open a
valve

In this case we can optimise an algorithm by:

* Instead of calculating a path each step - calculate "cost of an opening a valve" - so all paths from each node to
  another - and decrease a time by a number of steps (+1 to open)
* Calculate an energy emitted by each valve based on a time left - in this case we can simply maximise a results using a
  recurrence

## Day 17

[Day 17](17/README.md)

Tetris game - you simulate how rocks are failing down until it will be impossible. You need to calculate how tall will
be a group of rocks after 2022 rocks fails (part I) or 1_000_000_000_000 (part II).

Second part suggest that we can't simulate it endlessly - so we have to find out a "pattern". Patter is a marker "move
id" and "rock id" - we can find out a "loop" in a pattern - so then calculate a final "height"

## Day 18

[Day 18](18/README.md)

3D area traverse.

In Part I you have to find out all the boxes in a 3D that are neighbours of each-other.

In Part II you have to simulate water failing on a boxes - and then do a very similar counting.

## Day 19

[Day 19](19/README.md)

Simulation of a manufacture. You can buy one robot at once - so simulate a maximum energy. In my case I've just
simulated each step - but it took almost a minute to compute a last step in PII

I found that using a constrain programming (cpmpy) we can create an array of a "decisions" - for each step we can have a
decision matrix (value from 0 to 4, number of vals equal to number of rounds).
On each step and each robot we are adding a lot of constrains - equal to calculate number of resources and number of
robots after each decision, and "greater or equal" to check if we have enough resources to build a robot
After all those "constrains" we just maximize a model for one of the values (geodes) - in this case it takes 3 seconds
to compute all those rules

## Day 21

[Day 21](21/README.md)

We have a bunch of "equations" - how monkeys calculate defined "operations". At the end you just need to "reverse" an
operation. We can use either Sympy (200ms) or Cpmpy (8ms) to solve it recursively

## Day 22

[Day 22](22/README.md)

Amazing puzzle - when based on a map you have to build a cube - an any step at the border will be then another position
in another place (with a different direction) - AMAZING puzzle!

TODO: Check if it's possible more clever way

## Day 24

[Day 24](24/README.md)

You need to go through a mazze, but with a moving elements - so you can't simple do a BFS/DFS here - you need to keep a
time as a parameter.

TODO: Check if we can implement some build-in graph libraries

## Day 25