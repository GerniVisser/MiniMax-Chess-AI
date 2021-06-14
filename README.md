
# Chess AI

A fully implemented interactive Chess AI implemented using the MiniMax algorithm and Alpha-beta pruning for optimization. Full-fledged UI makes for a pleasant user experience. 


## Demo


  ![Alt Text](https://media.giphy.com/media/hojJHfOF6Z8XvfHjl2/giphy.gif)
## Features

- Color selection
- Interactive UI
- Configure search depth
- invalid move prevention

  
## Lessons Learned

The engine operates evaluates every possible move up to six moves ahead. All the board states after the six moves are analyzed to determine which one has the highest probability of winning. By utilizing the MiniMax algorithm, the engine can then calculate which moves to make. The assumption is that the opposing player would also be making the optimal moves to ensure his/her victory. I then added the Alpha-beta pruning algorithm that reduces the number of board states to evaluate by removing those that are obviously unfavorable.
Evaluating any given board state is done with the use of an evaluation function. There are many ways to implement such a function, so my goal was to find one that balanced performance with accuracy. Performance is improved by reducing the number of parameters to process while accuracy is improved by increasing it. I set a 10 second limit to the processing time and then went on to find the most efficient evaluation function that I could. The one I finally came up with allowed the engine to evaluate 6 moves ahead.


  
