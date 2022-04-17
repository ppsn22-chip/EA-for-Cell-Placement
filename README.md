# EA for Chip Placement

It's an open souce implemention for paper **Evolutionary Algorithms Can be Better Than Reinforcement Learning for Cell Placement in Chip Design** for PPSN-22.

## Requirements

**No further requirements** for our algorithm only (for results in Sec.4.1 and 4.3).

For  results in Sec.4.2 and RL method for comparison, see open source implemention [DeepPlace](https://github.com/Thinklab-SJTU/EDA-AI).

## Macroplacement

To run macro placement task on  *adaptec3*, using crossover operator *PMX*, mutation operator *swap*, population size 10, evaluation budget = 50000, number of grids = 32, number of macros = 710, type the following command:

```python
python main.py --crossover PMX --mutation swap --popsize 10 --max_eval 50000 --grid_num 32 --macro_num 710
```

We have implemented four different crossover operators **{PMX, CX, OX, EX}** and four different mutation operators **{swap, scramble, invert, inversion}**. To try them, simply change the command above.

