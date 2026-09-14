# RAG Document QA

使用 Python、FastAPI、Gemini API 與 ChromaDB 建立的
Retrieval-Augmented Generation（RAG）文件問答系統。

> 🚧 Project Status: In Development

## 專案目標

本專案旨在實作一套文件型 RAG 問答系統，
將 PDF 文件進行文字擷取、清理、Chunking 與 Embedding，
並將向量資料儲存於 ChromaDB。

使用者提出問題後，系統會透過語意檢索取得相關文件內容，
再將 Retrieved Context 提供給 Gemini 產生文件導向的回答。

除了基本 RAG Pipeline，本專案亦著重於 Retrieval Evaluation，
透過測試資料分析 Top-K Retrieval、Distance Threshold
與 Answerability 之間的關係。
