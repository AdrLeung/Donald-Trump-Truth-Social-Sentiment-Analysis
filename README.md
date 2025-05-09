# Truth Social Sentiment Analysis Discord Bot
Adrian Leung
A Discord bot designed for pulling posts by Donald Trump and analyzing them for buy signals on SPY options.

## Motivations
Donald Trump has proven to have an immense impact on the stock market whenever he chooses to. On Wednesday, April 9th, 9:37am ET, he posted that "THIS IS A GREAT TIME TO BUY!!! DJT," followed by a 90-day tariff pause less than 4 hours later. This pause caused the S&P 500 to gain 9.5%, the largest single-day gain in the past decade. This event sparked particular interest in me because:
- I like making money.
- It doesn't seem completely unlikely that this event will happen again.
- I would like to know when it happens without having to constantly check his posts.
Thus, I have created a Discord bot that pings a channel in my private Discord server whenever he posts on Truth Social, followed by an AI generated sentiment analysis that is done by ChatGPT using a specialized prompt.

## Features
- This Discord bot uses the publicly available [truthbrush](<https://github.com/stanfordio/truthbrush>) repository by stanfordio as an API client for Truth Social.
- The bot will send a message in a dedicated Discord Channel whenever Trump posts on Truth Social.
- The bot will perform a quick sentiment analysis on the post using ChatGPT with a specialized prompt.

## Usage
WIP

## Instructions for End User
WIP

## Strategy
Whenever the Discord Bot messages the Discord server with a buy signal, I will simulate placing a 5% out-of-the-money SPY call with minimum 7-day expiration; however, I will be selling these contracts on the same day in order to reduce the impact of theta. I chose SPY because it has high liquidity and because the S&P 500 tends to be a strong indication of how the US economy is doing.

I will sell the contract if it loses or gains more than 20% of its premium.

## Results & Effectiveness
Will be updated as trades occur.

## TODO
- Testing results by making trades according to the above strategy.
- Reduce delay of between when Donald Trump posts and when my bot sends the message on Discord.