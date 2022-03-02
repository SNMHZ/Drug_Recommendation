## Dataset 처리

### Condition
Unique한 Condition이 총 `937개`, 이를 분류하긴 어려울 것이라 생각하여 20개의 Condition에 대해서 분류를 하는 모델을 만든다.  
review개수가 많은 상위 50개 Condition을 뽑고, 유사한 Condition을 합친 뒤, 정신적인 질병을 제외하여 20개의 Condition을 선별함.  

### DrugName
DrugName의 경우 똑같은 성분, 용량임에도 회사마다 이름이 다른 데이터가 있는 것을 확인함.  
선별한 20개의 Condition에 사용하는 약물 중 이를 모두 합쳐준다.  


### 추가 데이터
각 Condition에 대한 Symptom정보가 없었기에 아래 두 사이트를 참고하여 Symptom 추가.  
[NHS](https://www.nhs.uk/)  
[Mayo Clinic](https://www.mayoclinic.org/)  