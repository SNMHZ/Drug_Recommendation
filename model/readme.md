# Model Description Document

## prototype
각 리뷰를 한개 토큰으로 word2vec 학습.
인풋에서 stopword 제거 후 코사인 유사도 계산.
유사도 점수를 단순 합 하여 순서대로 나타냄.
| num | pre-process  |   model  |  hyper-param  | feature |
| --- | ------------ | -------- | ------------- | ------- |
|  1  | lematization | word2vec | window_size=5 | only lematization lem-test, lem-train  |
|  2  | lematization | word2vec | window_size=5 | eliminate space from condition  |
|  3  | lematization | word2vec | window_size=5 | weight according to the frequency of appearance |