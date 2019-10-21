### Gym environment
* Observation space: RGB image (640x400x3)
* Action space: move in 8 directions + shoot
* Reward function: 

  ![](https://raw.githubusercontent.com/borijang/gym-duckhunt/master/gym_duckhunt/envs/assets/sprites/black/duck1.png) Black duck: 75 reward

  ![](https://raw.githubusercontent.com/borijang/gym-duckhunt/master/gym_duckhunt/envs/assets/sprites/red/duck1.png) Red duck: 50 reward

  ![](https://raw.githubusercontent.com/borijang/gym-duckhunt/master/gym_duckhunt/envs/assets/sprites/blue/duck1.png) Blue duck: 25 reward

  Moving or missing a shot: 0 reward

* Game session: 60 seconds

### Requirements
The environment is developed with:
* Python 3.7
* gym 0.14.0
* pygame 1.9.6
* numpy 1.17.2

### Installation
Clone this repo and then run `pip install -e gym-duckhunt` inside the project. Afterwards you can create the environment with `env = gym.make("gym_duckhunt:DuckHunt-v0")`.

### Acknowledgement
Most of the sprites and game logic are borrowed from [this repo](https://github.com/mwrouse/DuckHunt-Python).
