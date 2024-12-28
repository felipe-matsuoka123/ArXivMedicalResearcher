# **ArXiv Medical Insights Tool**

An interactive tool to explore research papers from ArXiv in computer science and engineering, uncovering valuable insights for potential medical applications.

---

## **Overview**

This project helps researchers and enthusiasts bridge the gap between engineering innovations and healthcare applications. By leveraging the **ArXiv API**, **Streamlit**, and **Crew AI**, the tool:
- Generates targeted search queries for ArXiv.
- Retrieves and presents relevant research papers.
- Highlights insights on how the papers could be applied in medical contexts.

---

## **Features**
- Tailored query generation for precise results.
- Automated retrieval of research papers from ArXiv.
- User-friendly Streamlit interface for exploration.
- Explanation of each paper’s relevance to healthcare. 🩺

---

## **Technologies Used**
- **Crew AI**: For building and managing intelligent agents.
- **Streamlit**: For the interactive web-based interface.
- **ArXiv API**: For accessing the latest research papers.

---

## **Getting Started**

### **1. Prerequisites**
- Python 3.8 or higher.
- An OpenAI API key. 🔑

### **2. Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/arxiv-medical-insights.git
   cd arxiv-medical-insights
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=<your_openai_key>
   ```

---

### **3. Running the Application**
Start the Streamlit app by running:
```bash
streamlit run streamlit-app.py
```
This will launch the app in your default web browser.

---

## **Usage**
1. Enter your research query in the text box (e.g., "attention mechanism").
2. Click the **Search Papers** button.
3. Browse through the displayed papers, including:
   - Title, Abstract, Authors, and Publication Date.
   - Explanation of each paper’s relevance to healthcare.
---

## **License**
This project is open-source and available under the MIT License.
