## Task 1 : 情緒預測
資料前處理: 將分數大於2視為分數2, 小於-2視為-2, 空值則捨去  
驗證方式皆為5 fold CV, 使用LinearSVM 精確度73.72%, LogisticRegressionCV 精確度 73.75% 稍好一點  

使用的model詳細參數如下(default parameter): 

0.737186422392 LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
     verbose=0)

0.7375236379 LogisticRegressionCV(Cs=10, class_weight=None, cv=None, dual=False,
           fit_intercept=True, intercept_scaling=1.0, max_iter=100,
           multi_class='ovr', n_jobs=1, penalty='l2', random_state=None,
           refit=True, scoring=None, solver='lbfgs', tol=0.0001, verbose=0)
           
##  Task 2 : 預測購物行為
* 資料前處理:保留10%做測試資料，剩餘90%訓練資料，捨去timestamp並合併相同user與item的購物紀錄  
* 模型使用Matrix Factorization SVD(原理還沒搞懂)，user對item的分數大於一定的threshold就預測為會購買
* 評估方式: 將測試資料的購物紀錄合併得到user->list[item] (Truth Set)，再跟model預測出來的Predict Set比較。
計算在所有實際有購買的物品中，被成功預測有購買的比率(TPR)；所有實際沒有購買的物品，被錯誤地判斷有購買之比率(FPR)。
根據threshold值域平均分成十個點分別計算TPR與FPR畫ROC，最後用梯形法求得AUC
* 結果: AUC 0.5008 
* 備註 5-fold CV 沒作，目前model的參數是隨便挑的