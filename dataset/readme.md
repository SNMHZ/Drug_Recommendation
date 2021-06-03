Dataset Description Document

[EDA](/EDA/EDA_DrugReview.md)

| num |      file name      |   pre-process  |  description  | 
| --- | ------------------- | -------------- | ------------- | 
|  1  | drugsComTest_raw    |        -       | 원본          |
|  2  | before_review_testw |    drop na     | 결측치 제거    |
|  3  | lem_test            | lemmatization  | 동사를 원형으로 변형 |
|  4  | snow_test           | stemming       | ing, ed등 제거  |
|  5  | lem_test2           | lemmatization  | 동사 -> 원형. '.','!','?'유지(문장별 구분 목적)|

### lemmatization과 stemming의 차이
    lemmatization - 등록된 동사만 등록된 원형으로 변형. 등록되지 않은 동사는 변환되지 않을 수 있음.
    stemming      - 규칙에 따라 제거. 단순 규칙 기반 추출로 의도치 않은 결과 발생 가능성 높음.