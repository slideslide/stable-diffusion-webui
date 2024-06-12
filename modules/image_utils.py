import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 确保你已经安装了nltk库。如果没有安装，请运行以下命令：
from deep_translator import GoogleTranslator
from zhipuai import ZhipuAI

def prompt2demand(userinput):

    def extract_nouns(sentence):
        # 分词
        words = word_tokenize(sentence)

        # 词性标注
        pos_tagged = nltk.pos_tag(words)

        # 提取名词（NN, NNS, NNP, NNPS）
        nouns = [word for word, pos in pos_tagged if pos in ['NN', 'NNS', 'NNP', 'NNPS','VB','JJ','VBG']]

        return nouns


    demand_list_1= ['refer', 'color', 'composition', 'picture', 'generate', 'picture', 'similar', 'pure', 'colors', 'plane', 'effect']
    demand_list_4= ['restore', 'blooming', 'state']
    demand_list_6 = ['girl', 'right', 'hand', 'bouquet', 'light-colored', 'flowers']
    demand_list_3 = ['red', 'texture', 'background', 'multiple', 'leaves', 'white', 'wireframe', 'graphic', 'effect']
    demand_list_2 =  ['fluffy', 'cute', 'rabbit', 'pink', 'clouds', 'wearing', 'pink', 'hat', 'ear', 'standing', 'ear', 'hanging', 'effect']
    demand_list_5 =     ['sides', 'be', 'add', 'small', 'flowers', 'be', 'small', 'flowers', 'middle', 'part']  
    demand_list_7 =     ['replace', 'pattern', 'color', 'cool', 'tone'] 
    demand_list_8 =     ['change', 'background', 'bear', 'scarf', 'warm', 'colors']  
    user_input = userinput
    translated = GoogleTranslator(source='auto', target='en').translate(user_input)  # output -> Weiter so, du bist großartig
    # print(translated)
    sentence = translated.lower()
    #sentence=user_input
    # 提取名词
    nouns = extract_nouns(sentence)
    print(nouns)
    de1=0
    de4 =0
    de6 = 0
    de3 = 0
    de2 = 0 
    de5 = 0 
    de7 = 0 
    de8  = 0 
    for items in nouns:
        if items in demand_list_1:
            de1 += 1
        if items in demand_list_4:
            de4 += 1
        if items in demand_list_6:
            de6 += 1
        if items in demand_list_3:
            de3 += 1 
        if items in demand_list_2:
            de2 += 1 
        if items in demand_list_5:
            de5 += 1 
        if items in demand_list_7:
            de7 += 1 
        if items in demand_list_8:
            de8 += 1 
    # print(de1,de2,de3)
    if de1>=3:
        return 1
    elif de4>=3:
        return 4
    elif de6>=3:
        return 6
    elif de3>=3:
        return 3
    elif de2>=3:
        return 2
    elif de5>=3:
        return 5
    elif de7>=3:
        return 7
    elif de8>=3:
        return 8
    else:
        return 9
  

def fetch_url(prompt):
    client = ZhipuAI(api_key="51d167d6b1d76b9fb63938840c41c23d.e9Ajbk2jzKowSEXZ") # 请填写您自己的APIKey
    response = client.images.generations(
        model="cogview-3", #填写需要调用的模型名称
        prompt=prompt)
    # 获取生成的图像URL
    image_url = response.data[0].url
    return image_url  