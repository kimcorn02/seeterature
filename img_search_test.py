from cnn_module import *
from faiss_module import *
import json

data_path = './data/data.json'
with open (data_path, "r") as f:
    data = json.load(f)

# (all) img feature vector
img_folder_path = './data/'
file_list = sorted([i for i in os.listdir(img_folder_path) if (i[-3:].lower()=='jpg') | (i[-3:].lower()=='png')])
fv_pkl_path = 'vgg16_features.pkl'

if not os.path.isfile(fv_pkl_path):
    # feature vec pkl 없는 경우
    fv = create_fv(img_folder_path, fv_pkl_path)
else:
    with open(fv_pkl_path, 'rb') as file:
        fv = pickle.load(file)

# faiss idx
idx_path = 'faiss_idx.index'

if not os.path.isfile(idx_path):
    # faiss index 없는 경우
    idx = make_faiss_idx(fv, idx_path)
else:
    idx = faiss.read_index(idx_path)

# preprocess query
query_path = './data/ChayeonKim_OneWinter.jpg'
query_fv = preprocess_query(query_path)

# faiss search
top_k = 3
distance, indices = search_faiss(top_k, idx, query_fv)

for n, i in enumerate(indices[0]):
    print(f'top_{n+1} :',file_list[i])

# print description of top_1
top1_id = file_list[indices[0][0]]

top1 = None
for item in data:
    if item['eng_id'] == top1_id:
        top1 = item
        break

if top1:
    print(f'Top 1 description: {top1["description"]}')
    print(f'Explanation: {top1["explanation"]}')
    print(f'Comment: {top1["comment"]}')
    print(f'Meta Info: {top1["meta"]}')
else:
    print('Description not found for top1_id.')