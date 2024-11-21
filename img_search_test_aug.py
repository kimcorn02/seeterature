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


def img_search(query_path):
    query_fv = preprocess_query(query_path)

    # faiss search
    top_k = 1
    distance, indices = search_faiss(top_k, idx, query_fv)

    # print description of top_1
    top1_id = file_list[indices[0][0]]

    return distance, top1_id

import random
random_files = random.sample(file_list, 30)

for f in random_files:
    distance, top1_id = img_search('./data/'+f)

    if top1_id != f:
        print(f, distance)