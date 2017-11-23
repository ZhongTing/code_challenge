import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds


def load():
    header = ['user', 'item', 'qty', 'datetime']
    df = pd.read_csv('rs.csv', sep=',', names=header, skiprows=1)
    cv_data_size = int(0.9 * len(df))
    df_cv = preprocess(df[:cv_data_size])
    df_test = preprocess(df[cv_data_size:])
    return df_cv, df_test


def preprocess(df):
    df = df.groupby(['user', 'item'], as_index=False).size().reset_index(name='counts')
    return df


def predict(predict_df, user, threshold):
    predict_item = []
    item_name_array = predict_df.columns
    for i, item_score in enumerate(predict_df.query("index==" + user).iloc[0]):
        if item_score > threshold:
            predict_item.append({"item": item_name_array[i], "score": item_score})
    predict_item.sort(key=lambda k: k["score"], reverse=True)
    return predict_item


# ref https://beckernick.github.io/matrix-factorization-recommender/
def build_model(df_train, k):
    R = df_train.as_matrix()
    user_ratings_mean = np.mean(R, axis=1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)
    U, sigma, Vt = svds(R_demeaned, k)
    sigma = np.diag(sigma)
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    predict_df = pd.DataFrame(all_user_predicted_ratings, index=df_train.index, columns=df_train.columns)
    # normalize
    predict_df = (predict_df - predict_df.mean()) / (predict_df.max() - predict_df.min())
    return predict_df


def compute_auc(df_test, predict_df):
    roc_points = []
    for threshold in np.linspace(-1, 1, 10):
        tpr_list = []
        fpr_list = []
        for user in df_test["user"].unique():
            user_buy_items = list(df_test.query("user==" + str(user))["item"])
            predict_buy_items = [i["item"] for i in predict(predict_df, str(user), threshold)]
            tp = len(set(user_buy_items).intersection(predict_buy_items))
            fp = len(predict_buy_items) - tp
            tpr_list.append(tp / len(user_buy_items))
            fpr_list.append(fp / (predict_df.shape[1] - len(user_buy_items)))
        roc_points.append((np.array(tpr_list).mean(), np.array(fpr_list).mean()))
    auc = np.array([point[0] * point[1] for point in roc_points]).sum() / len(roc_points)
    return auc


def main():
    df_train, df_test = load()
    df_train = df_train.pivot(index='user', columns='item', values='counts').fillna(0)
    # todo : 5 fold CV and find best k
    k = 900
    predict_df = build_model(df_train, k)
    auc = compute_auc(df_test, predict_df)
    print(auc, k)  # 0.500806333683 900


if __name__ == "__main__":
    main()
    # test()
