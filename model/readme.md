# Model Description Document

## prototype
### Goal
웹에 집중하여 일단 돌아가는 서비스 제작

### Detail
웹 - 모델 분리하여 모델을 쉽게 갈아끼울 수 있도록 한다.

각 리뷰를 한개 토큰으로 word2vec(CBOW) 학습.<br>
인풋에서 stopword 제거 후 코사인 유사도 계산.<br>
이후 유사도 점수를 단순 합 하여 순서대로 나타냄.<br>

_word2vec(CBOW) 모델 설명_
| num | pre-process  |   model  |  hyper-param  | feature |
| --- | ------------ | -------- | ------------- | ------- |
|  1  | lematization | word2vec | window_size=5 | only lematization lem-test, lem-train  |
|  2  | lematization | word2vec | window_size=5 | eliminate space from condition  |
|  3  | lematization | word2vec | window_size=5 | weight according to the frequency of appearance |

### Conclusion
코사인 유사도만으로도 나쁘지 않은 결과.<br>
하지만 역시 너무 단순한 모델.<br>
더 정교한 예측 모델 제작 필요.<br>
<br>

## ver1.0
### Goal
모델 성능 개선

### Detail
 1. 3가지 방법으로 텍스트 임베딩

        1. 리뷰단위
        2. 문장단위
        3. pre-trained

 2. 3가지 방법으로 텍스트 임베딩 후 분류모델 학습

        1. RANDOM-FOREST
        2. MLP
        3. RNN
        4. LSTM
        5. TEXT-CNN

 3. 성능 비교

_word2vec(CBOW) 모델 설명_
| num | pre-process  |  hyper-param  | feature |
| --- | ------------ | ------------- | ------- |
|  1  | lematization | window_size=5 | 리뷰단위 |
|  2  | lematization | window_size=1 | 문장단위 |
|  3  | -            | -             | https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit |

_분류모델 성능 비교_
| num | Model Name   |  hyper-param  | feature | f1-score |
| --- | ------------ | ------------- | ------- | -------- |
|  1  | -            | -             | -       |
|  1  | -            | -             | -       |

### Conclusion
진행중~~~
어느 임베딩 방식이 가장 효과적인지?

어떤 분류 모델이 가장 효과적인지?

앞으로 개선 방향성