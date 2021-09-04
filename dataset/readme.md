Dataset Description Document

[EDA](/EDA/EDA_DrugReview.md)

| num |      file name          |   pre-process  |  description  | 
| --- | ----------------------- | -------------- | ------------- | 
|  1  | drugsComTest_raw.csv    |        -       | 원본          |
|  2  | before_review_testw.csv |    drop na     | 결측치 제거    |
|  3  | lem_test.csv            | lemmatization  | 동사 -> 원형. 특수문자 전체 제거 |
|  4  | snow_test.csv           | stemming       | ing, ed등 제거  |
|  5  | lem_test2.xlsx          | lemmatization  | 동사 -> 원형. '.','!','?'유지(문장별 구분 목적) |

### lemmatization과 stemming의 차이
    lemmatization - 등록된 동사만 등록된 원형으로 변형. 등록되지 않은 동사는 변환되지 않을 수 있음.
    stemming      - 규칙에 따라 제거. 단순 규칙 기반 추출로 의도치 않은 결과 발생 가능성 높음.

### 기타
| num |      file name         |  description   | 
| --- | ---------------------- | -------------  | 
|  1  | inquirerbasic.xls      | 하버드 감정분석 |
|  2  | spaced_condition.csv   | 인덱스 / 원본 컨디션 / 공백제거한 컨디션 / 단어 수 |
|  3  | ex_merged.xlsx         | train+test(엑셀 형태) |
