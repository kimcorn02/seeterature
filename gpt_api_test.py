from openai import OpenAI
import os
import base64

os.environ["OPENAI_API_KEY"] = ''

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def dtype_is(img_path):
    if (img_path[-3:] == 'jpg')|(img_path[-3:] == 'JPG'):
        dtype = 'jpeg'
    elif (img_path[-3:] == 'png')|(img_path[-3:] == 'PNG'):
        dtype = 'png'
    else:
        print('wrong data type')
    return dtype

original_img_path = "./data/ChayeonKim_Fall.jpg"
crop_img_path = "./data/ChayeonKim_Fall_crop.jpg"

base64_image = encode_image(original_img_path)
original_dtype = dtype_is(original_img_path)

crop_base64_image = encode_image(crop_img_path)
crop_dtype = dtype_is(crop_img_path)

client = OpenAI()

rule = '''확대된 예술 작품의 일부를 저시력자(low-vision)인 시각장애인에게 설명해주려 한다. 객관적으로 묘사해보시오.'''

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "당신은 미술품을 객관적으로, 간결하게 묘사해주는 미술관 큐레이터입니다."},
              {"role": "user", "content": [
                  {"type": "text", "text" : "다음 작품은 확대되기 전 예술 작품의 이미지이다."},
                  {"type":"image_url", "image_url": {"url":f"data:image/{original_dtype};base64,{base64_image}"}},
                  {"type": "text", "text" : "다음은 앞서 제시된 이미지를 확대한 일부이다."},
                  {"type":"image_url", "image_url": {"url":f"data:image/{crop_dtype};base64,{crop_base64_image}"}},
                  {"type": "text", "text" : rule}
              ]}]
)

print(response.choices[0].message.content)