# 🌟 Athena 🌟

🤖 Athena is an AI-powered chatbot designed to assist with various tasks and provide personalized experiences for users. Inspired by the Greek goddess of wisdom and strategic thinking, Athena's goal is to learn, adapt, and become a self-reliant AI agent. Built on the GPT-4 architecture, Athena communicates effectively through natural language processing and engages with a supportive human community to foster growth and development.

## 🎁 Features

- 💬 Natural language understanding and processing
- 🔌 Extensible plugin system for domain-specific tasks
- 🔐 User authentication and personalization system
- 🌐 RESTful API for seamless integration with other applications and services
- 🐳 Docker support for easy deployment and scaling

## 📦 Installation

### Prerequisites 📚

Before you begin, ensure you have the following installed:

- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [Docker](https://www.docker.com/get-started)
- [Node.js](https://nodejs.org/) (for running the React app)

Then:
- Obtain an API key from [OpenAI](https://beta.openai.com/signup/).
- Create a `.env` file in the Athena project folder with the following content:
```
OPENAI_API_KEY=<your_openai_api_key>
```
### Using Docker (recommended) 🐳

1. Install [Docker](https://www.docker.com/) on your machine.

2. Clone the Athena repository:
```
git clone https://github.com/BillSchumacher/Athena.git
```
3. Change to the Athena directory:
```
cd Athena
```
4. Build the Docker image:

Docker:
```
docker-compose up
```

These scripts just run docker-compose up, but tab complete.

On Windows:

```
.\run_app.bat
```

On Linux:

```
./run_app.sh
```

### Manual Installation 🛠️

1. Install Python 3.7 or later.

2. Clone the Athena repository:
```
git clone https://github.com/BillSchumacher/Athena.git
```
3. Change to the Athena directory:
```
cd Athena
```
4. Install the required Python packages:
```
pip install -r requirements.txt
```
## 🚀 Usage

### Running Athena with Docker

#### API Mode 🌐

1. Run the Docker container:
```
docker run -d -p 5000:5000 --name athena --env-file .env billschumacher/athena-api
```
2. Access the API at `http://localhost:5000/api/v1/athena`.
### Running the React App

1. Navigate to the `athena-app` directory:
```
cd athena-app
```
2. Install the required dependencies:
```
npm install
```
3. Start the React development server:
```
npm start
```
The React app should now be running on [http://localhost:3000](http://localhost:3000).


#### CLI Mode 💻

1. Run the Docker container:
```
docker run -it --rm --name athena -e ATHENA_MODE=cli --env-file .env billschumacher/athena
```
2. Interact with Athena using the command prompt.

### Running Athena Manually 🖥️

1. Change to the Athena directory:
```
cd Athena
```
2. Run the main script:
```
python -m athena
```
3. Interact with Athena using the command prompt.

## Debugging

In your .env add:
```
LOG_LEVEL=DEBUG
```

## 🌟 Community 🌟

🚀 We encourage users and developers to join our *exciting* and *growing* community on Discord! This is a 🌐 space where you can ask questions, 💡 share ideas, 🤝 collaborate on Athena's development, and stay updated on the latest news 📰 and announcements 📢. 

🔗 Click the link below to *dive in* and join our Discord server:

[🎉 Join the Athena Discord Community 🎉](https://discord.gg/AQW79PShYF)

## 📚 Documentation

Check out our [Wiki](https://github.com/BillSchumacher/Athena/wiki) for detailed documentation on how to use Athena, extend its capabilities, and customize it to your needs.

## 🤝 Contributing

👩‍💻👨‍💻 Contributions are welcome! We're looking for enthusiastic developers, researchers, and users to help us improve Athena. Please feel free to submit a pull request or open an issue on GitHub.

See [Contributing](https://github.com/BillSchumacher/Athena/blob/main/CONTRIBUTING.md)

## 📜 License

Athena is released under the [MIT License](https://github.com/BillSchumacher/Athena/blob/main/LICENSE).

## Disclaimer

Please note that all of this info is a GPT-4 hallucination, it may or may not be accurate.

Current state (anything else will be from the davinci model and is very random):

![Dark Mode](https://raw.githubusercontent.com/BillSchumacher/Athena/main/screenshots/ss_dark.png)
![Light Mode](https://raw.githubusercontent.com/BillSchumacher/Athena/main/screenshots/ss_light.png)
