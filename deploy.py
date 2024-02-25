import os
import json
import pandas as pd

##pbix 경로설정
file_path1 = '{your_path}'
os.chdir(file_path1)

##pbix 웹다운로드 파일로 이름설정
file_name="Report"
file_path2=file_name

##수정할 리뷰자연어 json파일 list > mallid가 포함된 슬라이서
##대시보드마다 수정할 내역이 달라서 미리 체크가 필요함
json_list= ['\\Report\\sections\\001_pp.2 %7C 키워드\\visualContainers\\00000_slicer (edc81)\\config.json',
'\\Report\\sections\\002_pp.3 %7C 상품\\visualContainers\\00000_slicer (8f09d)\\config.json',
'\\Report\\sections\\003_pp.4 %7C 고객\\visualContainers\\00000_MALLID필터\\config.json',
'\\Report\\sections\\004_쇼핑몰 선택\\visualContainers\\00000_slicer (8a29f)\\config.json',
'\\Report\\sections\\004_쇼핑몰 선택\\visualContainers\\00000_slicer (8a29f)\\dataTransforms.json',
'\\Report\\sections\\999_pp.1 %7C 통계\\visualContainers\\00000_MALLID필터\\config.json'
]

##몰리스트 불러오기(예시 파일)
##리뷰자연어를 사용 중인 리스트는 컨설팅팀 구글 시트에 있어서 해당 시트로 변경 예정
file_path100 = "{your_path}"
csv=pd.read_csv(file_path100+'mall_info1.csv')
mall_list=csv['mall_name']
mallcode_list=csv['mallid']

##mallid수정 for문
for i in range(len(mallcode_list)):

  ##pbix 추출
  os.system("pbi-tools extract ./"+file_name+".pbix")
	
	##json수정 for문
  for a in range(len(json_list)):
    file_path3=json_list[a]
    with open(file_path1+file_path2+file_path3, 'r', encoding='UTF-8') as f:
        json_data=json.load(f)
    if "00000_slicer (8a29f)\\config.json" in json_list[a]:
        json_data['singleVisual']['objects']['general'][0]['properties']['filter']['filter']['Where'][0]['Condition']['In']['Values'][0][0]['Literal']['Value']="'"+str(mallcode_list[i])+"'"
    else:
      if "00000_slicer (8a29f)\\dataTransforms.json" in json_list[a]:
        json_data['objects']['general'][0]['properties']['filter']['filter']['Where'][0]['Condition']['In']['Values'][0][0]['Literal']['Value']="'"+str(mallcode_list[i])+"'"
      else:
        json_data['singleVisual']['objects']['general'][0]['properties']['filter']['filter']['Where'][0]['Condition']['In']['Values'][0][0]['Literal']['Value']="'"+str(mallcode_list[i])+"'"
    with open(file_path1+file_path2+file_path3, 'w', encoding='UTF-8') as aa:
        json.dump(json_data, aa, indent="\t")

  ##컴파일
  # os.system("pbi-tools info")
  os.system("pbi-tools compile ./"+file_name+" ./"+file_name)

  ##pbixproj json 파일 생성 workspace와 Workspace ID 확인
  pbixproj={
    "version": "0.11",
    "created": "2022-12-03T12:10:31.1181314+09:00",
    "deployments": {
      "Model": {
        "mode": "Report",
        "source": {
          "type": "File",
          "path": "./*.pbix$"
        },
        "authentication": {
          "type": "ServicePrincipal",
          "tenantId": "{your_key}",
          "clientId": "{your_key}",
          "clientSecret": "{your_key}",
          "Workspace ID": "{your_key}"
        },
        "options": {
          "import": {
            "nameConflict": "CreateOrOverwrite",
            "skipReport": False
          },
          "dataset": {
            "replaceParameters": True,
            "deployEmbeddedReport": True
          }
        },
        "environments": {
          "Development": {
            "workspace": "{your_space}",
            "displayName": "a.pbix",
            "refresh": True
          }
        }
      }
    }
  }

  ##pbixproj 파일 경로/생성
  file_path_proj=file_path1+file_path2+'\\.pbixproj.json'

  with open(file_path_proj,'w',encoding='UTF-8') as f:
    json.dump( pbixproj ,f , indent="\t")
	
	## 생성한 pbixproj내용으로 덮어쓰기
  with open(file_path_proj, 'r', encoding='UTF-8') as f:
    json_data_proj=json.load(f)

  #파일명 바꿔야함
  # file_path=".\\"+file_name+"\\*.pbix$"
  # json_data_proj['deployments']['Model']['source']['path']=file_path

  ##pbixproj json파일 파일명 수정
  json_data_proj['deployments']['Model']['environments']['Development']['displayName']=mall_list[i]+".pbix"

  with open(file_path_proj, 'w', encoding='UTF-8') as a:
    json.dump(json_data_proj, a, indent="\t")

  ##디플로이 deploy <folder> <label> [<environment>] [<basePath>] [<whatIf>]
  os.system("pbi-tools deploy ./"+file_name+"/. Model")
  print(mall_list[i]+"deploy_complete")