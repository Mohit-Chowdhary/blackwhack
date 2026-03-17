# 🎴 BlackWhack

A fun strategy card game inspired by Blackjack — but with hidden information, bluffing, and probability-based guessing.

---

## 🧠 Concept

BlackWhack is a **3-round competitive card game** where you don’t play your own hand —  
you try to **predict your opponents’ total card values** better than they predict yours.

The twist?

👉 You **never see all the cards**

---

## 🎮 Game Rules

- Deck: **27 cards**
  - Values **2 → 14 (A = 14)**  
  - 13 Red + 13 Black  
  - ⭐ 1 special **Star card (value = 16)**  

- Each round:
  - Every player gets **3 cards**
  - **1 card is revealed**, others are hidden  
  - You must **guess total value of opponent hands**

- Optional mechanic:
  - 🎯 **Peek ability (50% chance)**  
  - Reveal **one extra hidden card**

---

## 🏆 Objective

- Game lasts **3 rounds**
- Score = **sum of your prediction errors**
- Lowest total error wins

---

## 🤖 AI Difficulty Levels

### 🟢 Easy
- Completely random guesses  
- No strategy

### 🔵 Medium
- Uses **Expected Value (EV)**  
- Assumes average unknown card ≈ **7.5**
- Estimates totals based on partial info

### 🔴 Hard
- Tracks **missing cards in deck**
- Adjusts EV dynamically
- Makes smarter probabilistic guesses based on revealed + remaining cards

---

## 🛠️ Tech Stack

- Python
- Pygame (UI + rendering)
- Event-driven game loop
- Custom game state management

---

## ⚙️ Features

- 🎨 Interactive UI with card rendering
- 🧠 Multi-level AI opponents
- 🎯 Partial information + probabilistic reasoning
- 🔄 Multi-round scoring system
- ⚡ Real-time input + animations

---

## 🚀 Run Locally

```bash
pip install pygame
python main.py
