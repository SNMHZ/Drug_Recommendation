# 시스템 구조

## 모델

## condition 예측 시나리오
1. 사용자로부터 `input1`을 받는다.
2. `input1`을 `model`을 사용하여 `condition`예측 수행
3. 예측된 `condition`중 확률이 가장 높은 `condition`의 `symptom`을 질문
    - `Do you have ~~ ?`  
    1. 답변이 `yes`일 경우 `input1`에 해당 `symptom`을 추가한 `input2`를 만들어 `model`을 사용해 예측.
    2. 답변이 `no`일 경우 해당 `symptom`을 제외리스트에 추가
        1. 다음으로 높은 확률을 가진 `condition`의 `symptom`중 제외 리스트에 없는 `symptom`을 질문
    3. 전체 `condition`리스트를 모두 순회하고 나면 다시 1번 `condition`부터 질문
4. 조건을 만족한 경우 `condition`3가지와 `condition`에 해당하는 `probs`, `drugName`까지 표출
    1. `drugName`의 경우 각 `condition`별 `rating` 평균을 기준으로 상위 `drug` 추천
    2. 표출조건
        - 최소 `3번`의 대화 sequence
        - `condition`하나의 예측 확률이 일정수준 이상(80~90%)
        - 확률이 `80~90%`인 `condition`이 없을 경우 `10번` 이상의 대화 sequence


## 