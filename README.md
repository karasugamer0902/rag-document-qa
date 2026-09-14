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

## 系統架構

PDF Document
    ↓
Text Extraction & Cleaning
    ↓
Chunking
    ↓
Gemini Embedding
    ↓
ChromaDB
    ↓
Top-K Retrieval
    ↓
Retrieved Context
    ↓
Gemini
    ↓
Answer


## 目前進度

- [x] FastAPI `/chat` API
- [x] PDF 文字擷取與清理
- [x] Fixed-size Chunking + Overlap
- [x] Gemini Embedding
- [x] ChromaDB Persistent Storage
- [x] Top-K Semantic Retrieval
- [x] Top-1 / Top-3 Retrieval 比較
- [x] 建立 27 題 Retrieval Evaluation Dataset
- [x] Direct / Paraphrase / Boundary Positive 測試
- [x] Hard / Adversarial / Easy Negative 測試
- [ ] Distance Threshold Evaluation
- [ ] Precision / Recall / F1 分析
- [ ] Answerability / Relevance Gate
- [ ] Docker

## Retrieval Evaluation

初期測試發現，單純使用 Top-1 Retrieval 時，
最高相似度的 Chunk 不一定包含問題所需的完整答案。

例如在 Tokenization 測試中，正確定義出現在 Top-3 Retrieval 的 Rank 3，
因此將 Retrieval Strategy 從 Top-1 調整為 Top-3，
提升 Retrieved Context 的資訊覆蓋能力。

進一步加入 Adversarial Negative Questions 後發現，
語意相似度高並不代表 Retrieved Context 足以回答問題。

因此目前正透過 Accuracy、Precision、Recall 與 F1 Score
評估 Distance Threshold，並規劃加入 Answerability / Relevance Gate，
降低缺乏文件依據時仍產生回答的風險。
