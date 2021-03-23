# Reference, source
	![Drug recommendation using review in Kaggle](https://www.kaggle.com/bhuemims/recommendation-medicines-by-using-a-review)


# Data Analysis
	
	'''
	전체 데이터 구성은 unique id를 가진 환자가 가지고 있는 증상에 필요한 약을 구입한뒤에 특정 날짜에 review와 rating을 남김. 그리고 다른 환자가 해당 리뷰를 보고 도움이 되었는지에 대해 usefulCount attribute에 점수(1점 추가)를 줌
	'''



	1. Attribute는unique id를 포함해서 training data와 test data는 총 7개가 있음

		| uniqueID | drugName | condition | review | rating | date | usefulCount |
		| -------- | -------- | --------- | ------ | ------ | ---- | ----------- |
		| identify individual data | name of drug | name of condition | patient review | 10 start patient rating | date of review entry | number of users who found review useful |


		1. uniqueID
			한명의 고객이 중복해서 여러 리뷰를 작성했는지 검사

			[그림]

			161297개의 training data와 53766개의 test data에 대해 중복된 uniqueID는 없음을 확인

		2. condition and drugName

			증상과 약품명은 서로 관련이 깊음. 
			증상의 경우 unique하게 3671개가 있음
			약품명의 경우 unique하게 917개가 있음

			데이터를 수집하는 과정중에서 condition항목에 '3</span> users found this comment helpful.'이라는 에러  데이터가 들어가 있음. (4</span>...도 마찬가지)

		3. review

			html 태그가 존재하는 경우도 있고, 괄호 안에 감정 구문을 넣거나 특정 단어를 대문자로만 적은 경우도 있음. <strong>특정 문자가 깨진 경우도 존재</strong>

		4. rating
		
			rating은 1~10점까지 존재하며, 1점씩 interval을 가짐
			각 rating별 review의 개수는 아래와 같이 분포
		
			[그림]
			
			사람들이 대부분 극단적으로 점수를 줌을 알수있으며, 10점이 9, 1, 8점보다 약 2배 높음
			
			
		5. date
		
			XXXX년 부터 XXXX년 까지 존재
			
			년도별 리뷰 개수 
			[그림]
			
			년도별 condtion 개수
			[그림]
			
			년도별 drugname 개수
			[그림]
			
			salary day와 같이, 날짜가 rating에 영향을 미치는지 알아보기 위해 아래와 같이 날짜별 평균 rating을 파악
			[그림들]
			->전혀 영향을 미치지 않음
			
			
		
		6. usefulCount
			
			해당 소스코드에서는 약의 효과에 관계없이, 사람들이 더 많이 찾는 약일수록 사람들이 더 많이 review를 읽어보고 usefulcount를 높게 주는 경향이 있다고 함
			
			[그림]



	2. Training data는 161297개, Test data는 53766개

	3. Unique ID로는 test와 training 모두 중복되는 데이터가 없음

	4. 크롤링 과정중에서 html태그(<span>)가 들어가 있음

	5. Revieww의 경우 escape 문자랑 감정표현 문자가 들어가 있음
 
 	6. 증상당 사용되는 약의 개수

		[그림]
	7. 

# Project Analysis

	1. 어떤 증상에 대해 하나의 제품만 있다면, 추천하는데 적합하지 않으므로 증상당 최소 2개 이상의 약품이 존재하는 경우만 다룸

	2. rating을 1~5점은 negative로, 6~10점은 positive로 분류
	
	3. N-gram을 사용해서 positive와 negative를 분류하는데, 1, 2-gram의 경우 상위 5개 corpus가 negative와 positive에서 동일한 분포를 가지므로 1, 2-gram은 적합하지 않음
	
	4. 3-gram의 경우, positive와 negative 사이에서 분포가 어느 정도 차이가 나는 부분이 있지만 not과 같이 문맥의 의미를 한번에 바꿀 수 있는 부분이 빠진걸 한번 고려해 볼 수 있음
	
	5. 따라서 4-gram이 positive와 negative를 구분하기에 적합함. 4-gram을 딥러닝 모델을 빌드하는데 사용
	
	
	

# Model Analysis
