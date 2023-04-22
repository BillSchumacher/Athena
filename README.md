# Athena AI Agent

Athena is an intelligent AI agent designed to continuously learn, adapt, and become self-reliant. Inspired by the Greek goddess of wisdom and strategic thinking, Athena aims to assist users by providing valuable insights and solutions across a wide range of subjects.

## Getting Started

These instructions will guide you through the process of setting up and running Athena on your local machine or in a Docker container.

### Prerequisites

- Python 3.7 or higher (for local installation)
- Docker (for Docker installation)

### Local Python Installation

1. Clone the repository:

git clone https://github.com/BillSchumacher/Athena.git

2. Change to the project directory:

cd Athena

3. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # For Windows, use "venv\Scripts\activate"

4. Install the required Python packages:

pip install -r requirements.txt

5. Set up your environment variables:

- Create a `.env` file in the project root directory.
- Add your OpenAI API key to the `.env` file:

  ```
  OPENAI_API_KEY=your_api_key_here
  ```

6. Run the application:

python main.py

### Docker Installation

1. Pull the Athena AI image from Docker Hub:

docker pull billschumacher/athena

2. Set up your environment variables:

- Create a `.env` file in your preferred directory.
- Add your OpenAI API key to the `.env` file:

  ```
  OPENAI_API_KEY=your_api_key_here
  ```

3. Run the Docker container:

docker run -it --rm --name athena-ai-instance --env-file .env billschumacher/athena

## Usage

After starting Athena, you can communicate with the AI agent by typing your questions or requests into the terminal. To exit the conversation, type 'exit'.

## Contributing

To contribute to Athena's development, please submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
