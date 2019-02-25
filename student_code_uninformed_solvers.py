
from solver import *
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True

        movables = self.gm.getMovables()
        if movables:
            for move in movables:
                self.gm.makeMove(move)
                # create new state
                newState = self.gm.getGameState()
                newState = GameState(newState, self.currentState.depth + 1, move)
                newState.parent = self.currentState
                self.gm.reverseMove(move)
            # see if new state has been visited, if not travel down
            for new in self.currentState.children:
                if new not in self.visited:
                    self.visited[new] = True
                    self.gm.makeMove(new.requiredMovable)
                    self.currentState = new
                    break
        else:
            # all child states been visited, jump back to original state
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = queue.Queue()

    @property
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True

        movables = self.gm.getMovables()
        current = self.currentState

        if current not in self.visited:
            self.visited[current] = True
        while True:
            if movables and not current.children:
                for move in movables:
                    self.gm.makeMove(move)
                    newState = self.gm.getGameState()
                    # new game state --> move creates new game state & add to queue
                    if current.parent and newState == current.parent.state:
                        self.gm.reverseMove(move)
                        continue
                    else:
                        newState = GameState(newState, current.depth + 1, move)
                        newState.parent = current
                        current.children.append(newState)
                        self.queue.put(newState)
                        self.gm.reverseMove(move)
            print("queue size", self.queue.qsize())
            # get next state, see if visited
            nextS = self.queue.get()
            print("next state=", nextS.state)
            toRoot = []

            while current.requiredMovable:  # start from new state --> root

                self.gm.reverseMove(current.requiredMovable)
                current = current.parent

            while nextS.requiredMovable:
                toRoot.append(nextS.requiredMovable)
                nextS = nextS.parent
            while len(toRoot) != 0:
                move = toRoot.pop()

                self.gm.makeMove(move)
                newState = self.gm.getGameState()

                for new in current.children:
                    if new.state == newState:
                        current = new
                        self.visited[current] = True
                        break
            break

        return False
