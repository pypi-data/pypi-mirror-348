# fastai_newuser_recommender

一个用于 fastai 协同过滤模型新用户冷启动推荐的简易高层API。

## 安装（开发/本地）

```bash
pip install -e .
```

## 用法

```python
from fastai_newuser_recommender import print_recommendations

# 假设 learn 是已训练好的 fastai 协同过滤模型
new_ratings = {'True Lies (1994)': 5.0, 'Titanic (1997)': 5.0}
print_recommendations(learn, new_ratings, topk=10)
```

## 主要API
- `recommend_for_new_user(learn, new_ratings, topk=10, n_iter=40, lr=0.02, verbose=False)`
- `print_recommendations(learn, new_ratings, topk=10, n_iter=40, lr=0.02)`

## 依赖
- fastai >= 2.0.0
- torch >= 1.7.0 