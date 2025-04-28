<a name="readme-top"></a>

<!-- ======================================================================================== -->
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Point Mass Robot Simulator</h3>

  <p align="center">
    Lightweight 2D dynamics simulator for mobile and swarm robotics research.
    <br />
  </p>
</div>

<!-- ======================================================================================== -->
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ======================================================================================== -->
<!-- ABOUT THE PROJECT -->
## About The Project

[![Simulator Screenshot][product-screenshot]](https://example.com)

The **Point Mass Robot Simulator** is a lightweight 2D physics engine designed to model point-mass robots for individual or swarm robotics studies.  
It provides easy-to-extend robot models, simple force-based control, and graphical visualization of robot movement.

**Key Features:**
- 2D multi-agent simulation
- Swarming and flocking behaviors (Boids model)
- Real-time visualization with `pygame`
- Modular, clean code structure for customization

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With


- <a href="https://www.python.org/"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"> </a>
  <br />
- <a href="https://numpy.org/"> <img src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"> </a>
  <br />
- <a href="https://www.pygame.org/"> <img src="https://img.shields.io/badge/Pygame-0C0C0C?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame"> </a>



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ======================================================================================== -->
<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

You must have Python 3.7 or higher installed.

Install required libraries:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repo
   ```bash
   git clone https://github.com/air-cbr/point-mass-robot-simulator.git
   cd point-mass-robot-simulator
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the simulator
   ```bash
   python Main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ======================================================================================== -->
<!-- USAGE EXAMPLES -->
## Usage

- Modify robot movement model in `Boids_Assets/Boid.py`
- Change environment settings and simulation scenarios in `Boids_Assets/Configuration.json`
- Customize GUI elements inside `GUI_Assets/`
- Add new behaviors under `Boids_Assets/Boids_Rules`



<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ======================================================================================== -->
<!-- CONTRIBUTING -->
## Contributing

### Top contributors:

<a href="https://github.com/othneildrew/Best-README-Template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=othneildrew/Best-README-Template" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ======================================================================================== -->
<!-- LICENSE -->
## License

This project is licensed under a custom license.

No part of this code may be used, copied, modified, or distributed without prior written permission from the author.

See `LICENSE.txt` for full details.



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ======================================================================================== -->
<!-- CONTACT -->
## Contact

**Reda Ghanem**  
Email: reda.ghanem@unsw.edu.au

Project Link: [https://github.com/air-cbr/point-mass-robot-simulator](https://github.com/air-cbr/point-mass-robot-simulator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: images/simulator_screenshot.png

