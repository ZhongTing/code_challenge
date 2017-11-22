##  任務需求1：做一個情緒預測模型。
dataset 檔案名稱為Ch_trainfile_Sentiment_3000.txt  
請使用svm進行情緒預測模型。另外，請再想任何一個模型要能比svm好，用相同資料當驗證。  
input：句子 or 一個段落  
output：-2, -1, 0, 1, 2  
建議採用5-fold cross validation，回覆數據是多少。  
如：用SVM做完5-fold cross validation後的精準度為80.12％


## 任務需求2：recommendation task 。
dataset 檔案名稱為 rs.csv  
columns: (user：顧客／會員編號, item：商品編號, qty：交易量, datetime：交易時間)  
(a) 建模預測顧客購買行為（顧客-> List[商品]）  
(b) 自行split dataset：5-Fold CV + testSet，實現驗證方式。  
(c) 以AUC呈現驗證結果。

## 任務需求3 : 通用作者資訊爬蟲
設計一個通用型的作者資訊爬蟲  
input : 200 urls (may include noise)  
output : 對應url的作者名字(如果url不是文章就回傳None)