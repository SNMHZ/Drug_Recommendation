최종 순서
1. 전체 통계량(데이터 수)제시
2. attribute의미(표) 제시
3. 각 attribute별 특징적인 점 시각화
    uniqueID    - unique 수
    drugName    - unique 수
    condition   - unique 수, 가장 흔한 증상. 피임약이 압도적. drugname과 상관관계?
    review      - 글자 깨진거.
    rating      - 히스토그램. 점수 분포가 극단적인 부분
    date        - 날짜별 상관관계 없음. pd.to_datetime()으로 쉽게 핸들링 가능
    usefulCount - KDE(대부분 적고, 일부는 많은 추천수)
4. 각 attribute간 상관관계.


문제. n-gram 어디 넣을것인가?

각 Kaggle Review들의 분석 방법은 패스.
우리 목표와는 큰 상관관계 없는 방법들이 대부분(감성분석 등..)

현준

평점(rating)별 통계
    rating KDE(히스토그램으로 충분. 불필요) semi-O (커널밀도함수가 뭔지 알아봐야함)
    Counts of rating(히스토그램. 필요) O
    Ratio of counts(원그래프 비율. 음.. 필요한가?) O

날짜별 리뷰 통계
    Reviews per year O
    Reviews per month O
    Reviews per day O
    (크게 관계 없다는 점 시사. 진짜로 리뷰를 쓴 날이기 때문인거로 생각. ex. 5월에 사서 먹고 10월에 써도 전혀 상관이 없는 데이터.. 그냥 하나로 묶어서 보여주는게 좋을 듯!)

추천수(usefulCount)별 통계
    Distribution of usefulCount(KDE. 대부분의 usefulCount는 0 근처로 극히 일부만 200 이상)

    usefulCount와 rating 상관관계
    양의 상관관계를 가진다!
    다른 자료에도 포함되어 있음.

++ train과 test 모두 거의 동일한 분포를 보임

----------------------------------------

준기

데이터의 수, attribute의미, n-gram그래프(4-gram이 유의미)
rating->대부분이 점수를 극단적으로 준다.

----------------------------------------

준병

train, test 합병하고 시작.
약별로 상위 하위 20개 차트.(필요할 지 모르겟음) -> 만약 고려해본다면, attribute간의 상관관계에서 고려해볼수 있을듯(rating - drugName)
평점 분포(위에 많이 중복됨) O
10점짜리, 1점짜리 워드클라우드. stopword때문에 비슷하게 보임
상관관계 히트맵
 - 단어 분석.(n-gram)
 - 축약어 풀기

feature importance는 고려하려면, 모델 파트 고민할 때 붙여야 하는가? ( )
uniqueID, rating, usefulCount 간의 상관관계 추가 O
n-grams를 내건 버리고, 준병이 코드 사용하는게 좋을듯(ipython안 쓰고 로컬에서 바로 그릴수있기때문!) O
----------------------------------------

상목
1. 병마다 당연하게도 리뷰 수가 다르다. 흔한 질병 vs 덜 흔한 질병의 차이

2. 사람들을 정말로 좋거나 나쁜 약의 경우 더 리뷰를 많이 씀.
	양 극단에 비해 중간은 적다.

3. 약별 평점 평균, 상태별 평점 평균 확인 결과 평균이 높은게 더 많음
->표본이 적은 것도 1개로 들어가기에 신뢰도는 애매함

4. rating이 높다고 usefulcount가 높은 건 아님. 하지만 이것도 양 극단이 높아지는 경향을 보임
	2와 같은 맥락으로 보임

5. 높은 rating일수록 평균 usefulcount가 증가하는 경향. 아마 사람들의 포지티브 스크리닝으로 보임

6. usefulcount가 높은 리뷰는 대체로 긍정적, 반대는 부정적