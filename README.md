# Compute Engineering IAUN Bot

## Table of contents

+ [How to Run](#how-to-run)

## How to Run

To run project, follow the steps below:

1. Clone the repository:

   ```bash
   git clone https://github.com/MrUmbr3lla/ceiaun_bot.git
   cd ceiaun_bot/ceiaun_bot
   ```

2. Copy the `.env.example` file and fill in the required information:

   ```bash
   cp .env.example .env
   ```

3. Up the Docker container:
   ```bash
   docker compose up -d
   ```
   The `-d` flag runs the container in detached mode, allowing it to run the background.