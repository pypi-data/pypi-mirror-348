# vlm_inference

This repository contains code for performing inference using a Vision-Language Model (VLM) for robotic navigation tasks.

## Setup Instructions

Follow these steps to set up and run the VLM inference:

1.  **Clone the repository:**

    ```bash
    git clone ssh://git@gitlab.iri.upc.edu:2202/mobile_robotics/moonshot_project/vlm/vlm_inference.git
    cd vlm_inference
    ```

2.  **Create a `.env` file and add your OpenAI API key and the VLM configuration path:**

    Create a file named `.env` in the root directory of the repository and add the following content, replacing `sk-proj-_HFJE2I64...........` with your actual OpenAI API key and ensuring the `VLM_CONFIG_PATH` points to your configuration file:

    ```
    # .env
    OPENAI_API_KEY=sk-proj-_HFJE2I64...........
    VLM_CONFIG_PATH=vlm_inference/config.yaml
    ```

3. **Install libraries:**

If you have python 3.12:

- **Install Poetry:**

    If you haven't already, install Poetry, a tool for dependency management and packaging in Python:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

- **Activate the Poetry environment:**

    Navigate to the repository directory in your terminal and activate the virtual environment managed by Poetry:

    ```bash
    poetry shell
    ```

If you have can´t not modify the python version use the following command:
    ```bash
    python3 pip install -r requirements.txt
    ```


5.  **Set the navigation goal (optional):**

    If you want to specify a navigation goal as an object or person with a description, open the following file:

    ```
    vlm_navigation/prompt_manager/navigation_prompt.txt
    ```

    Locate line 7, which defines the `navigation_goal` variable, and modify it according to your desired goal. For example:

    ```
    navigation_goal = "a red chair near the window"
    ```

6.  **Run the inference script:**

    Execute the main inference script using Python 3:

    ```bash
    python3 vlm_navigation/inference.py
    ```

This script will load the VLM, potentially process images (depending on the script's functionality), and output the inference results based on the configuration and any specified navigation goal.
