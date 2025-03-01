# Crypto News Automation with FastAPI, ChatGPT & YouTube 🚀📰  

## 📌 Project Description  
This project is a fully automated **crypto news aggregation and YouTube posting system** powered by **FastAPI, OpenAI’s GPT-4, and Make.com**. It fetches the latest cryptocurrency news, summarizes key articles using AI, and allows user approval before automatically posting videos to YouTube. The system is hosted on **AWS** for scalability and reliability.  

### 🔹 Key Features  
✅ Fetch **real-time crypto news** from trusted sources using **NewsAPI**  
✅ Summarize news articles with **ChatGPT (GPT-4)**  
✅ Expose an API using **FastAPI** for structured access  
✅ Automate **YouTube video creation and posting** (after user approval)  
✅ Use **Make.com** for workflow automation (notifications, approvals, scheduling)  
✅ Host and deploy the system on **AWS** for continuous operation  

---

## 🛠 How It Works  

1️⃣ **News Retrieval:**  
   - The system fetches the latest cryptocurrency news using **NewsAPI**.  
   - It extracts headlines, summaries, and article links.  

2️⃣ **Summarization with AI:**  
   - OpenAI's **GPT-4** generates concise summaries of selected news.  
   - The system formats content for video narration.  

3️⃣ **User Approval Process:**  
   - A notification is sent via **Make.com** (Telegram, email, or dashboard).  
   - The user reviews and approves the news script before video generation.  

4️⃣ **YouTube Video Generation & Upload:**  
   - The approved script is converted into an **AI-narrated video**.  
   - The final video is **uploaded to YouTube** automatically using the **YouTube Data API**.  

5️⃣ **Hosting & Automation:**  
   - The entire system runs on an **AWS instance**.  
   - **Make.com** automate daily execution of the news-fetching process.  