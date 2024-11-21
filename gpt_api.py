from openai import OpenAI
import os
import base64
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

# app api
app = FastAPI()

# openai api
os.environ["OPENAI_API_KEY"] = ''

# Function to encode the image
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image file not found")

# OpenAI API 호출 함수
client = OpenAI()
rule = '''제공된 예술 작품을 저시력자(low-vision)인 시각장애인에게 설명해주려 한다.
    배경 지식이나 주관적인 해석을 최대한 배제하고, 작품의 소재와 형태를 위주로 묘사하라.
    묘사 시 지켜야 할 원칙은 다음과 같다.
    1. 설명의 순서 및 위치를 밝힌다. (예 : 작품의 좌상단에서부터 묘사하겠습니다.)
    2. 주요 소재를 묘사한다 (예: 6시 방향에 있는 흰색 천 같은 대상은 녹아내린 시계입니다.)
    3. 주요 소재의 형태를 자세히 묘사한다. (예 : 작품 6시 방향 내 시계의 형태)
    4. 작품의 색감을 자세히 묘사한다. (예: 작품의 전반적인 색감, 작품에서 두드러지는 색감 등)
    위의 원칙을 참고하여, 작품에서 중요한 요소나 전반적인 구조를 묘사하라. 개조식이 아닌, 미술관의 큐레이터가 설명하듯 묘사하라.'''

def generate_image_description(base64_image):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "당신은 미술품을 객관적으로, 간결하게 묘사해주는 미술관 큐레이터입니다."},
                    {"role": "user", "content": [
                        {"type": "text", "text" : rule},
                        {"type":"image_url", "image_url": {"url":f"data:image/jpeg;base64,{base64_image}"}}
                    ]}]
        )

        return response.choices[0].message.content
    except:
        raise HTTPException(status_code=response.status_code, detail="OpenAI API request failed")

class ImageRequest(BaseModel):
    image_path: str
    
# 이미지 설명을 생성하는 엔드포인트
@app.post("/gpt-describe/")
async def describe_image(request: ImageRequest):
    base64_image = encode_image(request.image_path)
    description = generate_image_description(base64_image)
    return {"description": description}