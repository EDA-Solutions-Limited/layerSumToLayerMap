# layerSumToLayerMap
<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">layerSumToLayerMap</h3>

  <p align="center">
    <br />
    <a href="https://github.com/EDA-Solutions-Limited/layerSumToLayerMap"><strong>Explore the project »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/EDA-Solutions-Limited/launch_putty/issues">Report Bug</a>
    ·
    <a href="https://github.com/EDA-Solutions-Limited/launch_putty/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#making-changes">Making changes</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Process Design Kits (PDKs) somtimes contain layout files that describe the layout. these layout files are used either in the setup of the layer pallet within the Tanner tools or to define names for layers in rule files. LVL rule decks in Calibre require a layermap file to get layer names that match the design layer name instead of Lxx_Dxx

it can be time consuming to build a layermap if one is not present. so this scipt will automate the pocess by taking an input layer summery file from L-edit and create a CSV

### Built With

* [Python](https://www.python.org/)


<!-- GETTING STARTED -->
## Getting Started

To get started with using this code, ensure you have python 3 installed. 

### Prerequisites

The following python libraries are required.

* pyclip
* pyautogui
* logging
* sys

  ```sh
  pip install pyclip
  pip install pyautogui
  ```

### Installation

1. Open the project at **..\EDA-Solutions-Limited\layerSumToLayerMap\layerSumToLayerMap** with an editor.
   Preferrably **vscode**
2. You could also clone the repo
   ```sh
   git clone https://github.com/layerSumToLayerMap/layerSumToLayerMap.git
3. Ensure you edit the createINI function in [**layerSumToLayerMap.py**](https://github.com/EDA-Solutions-Limited/layerSumToLayerMap/blob/main/layerSumToLayerMap.py#L179-L198) to your own desired default ini file.
4. create a shortcut that has a currently un assigned keystroke, through the right click context menu properties window.

### Notes:
1. Limitation: only built with windows in mind

<!-- ROADMAP -->
## Roadmap

1. None

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Not to be distributed to anyone outside EDA solutions. 

<!-- CONTACT -->
## Contact

Henry Frankland - [@hfrank](https://www.linkedin.com/in/henry-frankland-asic/) - henryfrankland@eda-solutions.com - henry@franklandhome.co.uk

Project Link: [layerSumToLayerMap](https://github.com/EDA-Solutions-Limited/layerSumToLayerMap.git)
