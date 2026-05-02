# 📦 Termux Skill Master 

**Advanced Prompt Engineering & Architecture Generator for LLMs / SLMs**

Termux Skill Master is a professional, terminal-based tool designed to run on Termux (Android) or any Unix/Windows environment. It acts as an interactive mentor and generator, helping developers and beginners structure complex software architectures before feeding them to AI models.

## 🚀 Key Features

- **🛡️ Anti-Hallucination Guardrails:** Automatically injects strict policies in the generated prompt to prevent the AI from inventing non-existent components, libraries, or APIs. The AI is forced to ask clarifying questions if your strategy is ambiguous.
- **🧩 Multi-Choice Architecture:** Build complex systems. Choose multiple UI stacks (e.g., CLI + WebApp + GUI Desktop) and define exact file names for modular orchestration (preventing spaghetti-code).
- **🔒 Safe Bootstrap & API Policy:** Instructs the AI to verify the system before blindly running `pip install` and enforces the use of free, accessible APIs.
- **🔄 Interactive Correction Loop:** Made a typo? The built-in Ask-Step loop allows you to press `X` to repeat any single step on the fly without restarting the entire configuration.
- **🌍 Dual Language Support:** Comes with both English (`skill_master.py`) and Italian (`skill_master_it.py`) interfaces out of the box.

## 🛠️ How to Use

1. Clone the repository to your Termux or PC:
   ```bash
   git clone https://github.com/dcarrieri73-hub/termux-skill-master.git
   cd termux-skill-master
   ```

2. Run your preferred language version:
   ```bash
   python skill_master.py
   # OR for Italian
   python skill_master_it.py
   ```

3. Follow the interactive CLI to define your workspace, cognitive model, tech stack, and modular files.
4. The tool will generate a perfectly structured prompt (`latest_prompt.txt`) and automatically copy it to your clipboard. Paste it to your AI (ChatGPT, Claude, or a local SLM) and watch the magic happen!

## 💡 Why use this?
Instead of writing vague requests like "build me a bot", Skill Master forces you to think like a Software Architect. It outputs a standardized, imperative prompt that dictates strict rules to the AI, ensuring the generated code is modular, robust, and explicitly adheres to your exact specifications. Every error made during prompt creation becomes a lesson, as the AI will mentor you rather than generating broken code.

---
*Created by Davide - Engineering prompts for the future.*
