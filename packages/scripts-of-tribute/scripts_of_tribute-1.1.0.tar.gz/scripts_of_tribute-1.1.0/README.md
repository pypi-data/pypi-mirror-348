# Scripts of Tribute Python Library

The **Scripts of Tribute** Python library is a wrapper for creating AI bots to compete in the **Scripts of Tribute** programming game. It facilitates communication with the game's C# .NET engine via **gRPC**, allowing you to implement custom bots and simulate game scenarios.

---

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
   - [Generating gRPC Files](#generating-grpc-files)
   - [Creating Your Bot](#creating-your-bot)
   - [Running the Game](#running-the-game)
3. [Game Class Documentation](#game-class-documentation)
4. [Example](#example)
5. [Contributing](#contributing)
6. [License](#license)

---

## Installation

To install the library, use `pip`:

```bash
pip install scripts-of-tribute
```

## Getting Started
### Creating your bot
To create your own bot, you need to inherit from the `scripts_of_tribute.base_ai.BaseAI` class and implement the required methods:
```python
def pregame_prepare(self):
        """Optional: Prepare your bot before the game starts."""
        pass

def select_patron(self, available_patrons: List[PatronId]) -> PatronId:
    """Choose a patron from the available list."""
    raise NotImplementedError

def play(self, game_state: GameState, possible_moves: List[BasicMove], remaining_time: int) -> BasicMove:
    """Choose a move based on the current game state."""
    raise NotImplementedError

def game_end(self, final_state):
    """Optional: Handle end-of-game logic."""
    pass
```

What's important here in the `play` method that bot should return `BasicMove` object from the list, it is because `Move` objects come from the engine with an Identification number `move_id` which is used to quickly identify whether move is legal or not.

### Running the game
The `scripts_of_tribute.game.Game` class is used to register and run your bots. Here's how to use it:
```python
from ScriptsOfTribute.game import Game
from Bots.RandomBot import RandomBot
from Bots.MaxPrestigeBot import MaxPrestigeBot

def main():
    bot1 = RandomBot(bot_name="RandomBot")
    bot2 = MaxPrestigeBot(bot_name="MaxPrestigeBot")
    
    game = Game()
    game.register_bot(bot1)
    game.register_bot(bot2)
    
    game.run(
        "RandomBot",
        "MaxPrestigeBot",
        start_game_runner=True,
        runs=10,
        threads=1,
    )

if __name__ == "__main__":
    main()
```

Game.run Parameters:
* bot1Name: Name of the first bot.
* bot2Name: Name of the second bot.
* start_game_runner: If True, the game runner starts automatically. Set to False if you want to run the engine manually.
* runs: Number of games to run.
* threads: Number of threads to use for parallel execution.
* enable_logs: Logging level ("NONE", "INFO", "DEBUG", etc.). 
* log_destination: File path to save logs.
* seed: Random seed for reproducibility.
* timeout: Timeout for each game (in seconds).
* base_client_port: Base port for gRPC client communication (default: 50000).
* base_server_port: Base port for gRPC server communication (default: 49000).


## Game class documentation
The `Game` class manages bot registration, game execution, and cleanup.

**Key Methods**:
* register_bot: Register a bot instance.
* run: Start the game with the specified bots and parameters.
* _cleanup_processes: Clean up all running processes on exit.

Port Assignment:
* The library assigns ports incrementally for multiple threads or bots:
    * First bot: 50000 (client), 49000 (server).
    * Second bot: 50001 (client), 49001 (server).
    * Additional threads increment ports accordingly.

On the first run with `start_game_runner=True` the `Game` class will download newest GameRunner suited for your operating system from [our official releases page](https://github.com/ScriptsOfTribute/ScriptsOfTribute-Core/releases), unzip it and then run it. After that if `Game` class find the GameRunner it won't download it again.

## Example
Here’s a complete example of creating and running two bots:

```python
from Bots.RandomBot import RandomBot
from Bots.MaxPrestigeBot import MaxPrestigeBot
from ScriptsOfTribute.game import Game

def main():
    bot1 = RandomBot(bot_name="RandomBot")
    bot2 = MaxPrestigeBot(bot_name="MaxPrestigeBot")
    
    game = Game()
    game.register_bot(bot1)
    game.register_bot(bot2)
    
    game.run(
        "RandomBot",
        "MaxPrestigeBot",
        start_game_runner=True,
        runs=10,
        threads=1,
    )

if __name__ == "__main__":
    main()
```
This code is available in the `examples` directory, as well with the example bots.

## Contributing
if you would like to work with the code locally you might need to (re)generate `protobuf` files.
The library uses gRPC for communication with the C# .NET engine. The `.proto` files are located in the `scripts_of_tribute/protos` folder. To generate the necessary Python files, run:
```bash
python -m grpc_tools.protoc -Iprotos --python_out=./protos/ --grpc_python_out=protos/. protos/enums.proto protos/basics.proto protos/main.proto
```
This will generate the required gRPC Python files in the `protos` folder.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

-----
Happy bot building! 🚀