	 	 	
API (DB 관리 + helper func)
```
1) 디비에 저장용 검사 :
  API 명 : insert_pois
  param : pois, category
  세부기능: poi 를 넣을때마다 DB 의 poi 가 있는지 확인후 poi 가 있을 경우 카테고리 유무를 확인후
  카테고리가 있을경우 카테고리를 추가 한다 , 만약 poi 가 없는경우 poi 를 pois 집어넣는다

  ※초기요구사항 : req: 카테고리, pois(이름, 좌표, 전화번호,주소, 도로명주소) res: 성공/실패메시지
	
	
2) 리스트 검색 :	
  API 명 : query_pois
  param : keyWord , collection 
  세부기능:  collection 에서 keyWord 와 일치하는 key 값이 있다면 해당 poi 들을 query 함 
  (key 종류:  이름, 큰 주소, 중간 주소, 작은 주소 디테일 주소, 도로명주소)
  (keys : name, address_big,address_mid,address_small,address_detail,address_road)

  ※초기요구사항:DB셀렉트 req: 검색키워드 res: pois(이름, 주소, 좌표)	

3) 별점매기기 :
  API 명 : update_star
  param : id, starPoint
  세부기능: id 에 해당하는 별점을 starPoint 를 받아 별점평균을 업데이트

  ※초기요구사항:DB업데이트 req: poi's ID, starPoint res: 성공/실패메시지

4) POI하나 가져오기 :
  API 명: query_poi
  param : id
  세부기능: id에 해당하는 poi 를 query

  ※초기요구사항:DB셀렉트 req: poi's ID res: poi(이름, 주소, 좌표, 이미지, 전화번호, 카테고리 등)

5) 최적장소 추천 ( 여기서는 사각형 바운드 안의 poi set 들을 query):
  API 명: query_square_bound
  param :  squareBound
  세부기능: DB 안에있는 모든 poi 들의 컬랙션으로부터 사각형 바운드(squareBound) 내부의 poi들을 query 하여 collection으로 반환. 

  ※초기요구사항:DB셀렉트 req: TopLeft, TopRight, BottomLeft, BottomRight, 사람들 좌표 res: 수정된 pois(기본적인 	poi정보, 가중치)
```
