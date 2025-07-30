# ChatApp

**ChatApp** is a lightweight Python package that powers a Streamlit-based chatbot interface designed to refine user queries using prior chat history and a reference document.

The app uses OpenAI's GPT-4 model (via LangChain) to return:
- A **refined query**, and
- **Additional context or logic** to help with analysis or automation

---

## 🚀 Features

- 🧠 Maintains full **chat history** across turns
- 📄 Incorporates a static **reference document** with example queries and hints
- 🤖 Integrates with **OpenAI GPT-4** via LangChain
- 📦 Package-style installation for easy sharing or deployment
- ✅ Clean XML-style formatted response:
  ```xml
  <refined_query>
  ...
  </refined_query>

  <additional_info>
  ...
  </additional_info>
