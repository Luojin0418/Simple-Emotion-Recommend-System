from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .model import Film, kmean_recom, user
from .form import SearchForm
import random



import requests
import urllib
import json
import base64
import cv2
import time
import os
import numpy as np
 
apiURL = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
accesstokenURL = "https://aip.baidubce.com/oauth/2.0/token"
 
apikey = "WbkOxl1VvOHEiXbpNwmyxQdr"
secretkey = "v9REMrizUmNVpGMHXjq0GD7rdSDf7S8r"
 
imge_path = os.path.dirname(os.path.abspath(__file__))+'\\img.jpg'
avi_path=os.path.dirname(os.path.abspath(__file__))+'\\output.avi'
faceinfo_type = ['face_type','face_shape','gender','emotion','age','glasses','beauty','location']


def camer_open():
    cap = cv2.VideoCapture(0)  # 默认的摄像头
    return cap
    
def camer_close(fun_cap):
    fun_cap.release()
    cv2.destroyAllWindows()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(avi_path,fourcc, 20.0, (640,480))
 
def make_photo(capp):
    """使用opencv拍照"""
    emotion_list = []
    access_token=get_AcessToken(apikey,secretkey)
    t = 0
    while True:
        t = t + 1
        ret_cap, frame = capp.read()
        time.sleep(0.2)
        if ret_cap:
            #print("read ok")
            color=(0,0,0)
            img_gray= cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            cv2.imwrite(imge_path, img_gray)
            image_base64=imgeTobase64()
            ret,info_list=get_face_response(access_token,image_base64)
            #print(ret)
            if ret == 0:
                w=int(info_list[faceinfo_type.index('location')])+100
                h=int(info_list[faceinfo_type.index('location')+1])+100
                y=int(info_list[faceinfo_type.index('location')+2])-80
                x=int(info_list[faceinfo_type.index('location')+3])-50
                fun_str=[]
                fun_str.append('age:'+ str(info_list[faceinfo_type.index('age')]))
                fun_str.append('emotion:'+info_list[faceinfo_type.index('emotion')])
                fun_str.append('beauty:'+str(info_list[faceinfo_type.index('beauty')]))
                fun_str.append('gender:'+info_list[faceinfo_type.index('gender')])
                #print(fun_str)
                print(info_list[faceinfo_type.index('emotion')])
                emotion_list.append(info_list[faceinfo_type.index('emotion')])
                print(emotion_list)
                y1 = int(y+(h/2))
                dy = 11
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                for i in range(len(fun_str)): 
                    y2= y1+i*dy
                    cv2.putText(frame,fun_str[i],(x+w+20,y2),cv2.FONT_HERSHEY_PLAIN,1, (255, 0, 0),1)
        # write the flipped frame
            out.write(frame)
            cv2.imshow("capture", frame)  # 弹窗口
            if cv2.waitKey(1) & 0xFF == ord('q'):
                camer_close(capp)
                break
            if t == 11:
                camer_close(capp)
                break
        else:
            break
    return repeat_nums(emotion_list)

        
def get_AcessToken(fun_apikey,fun_secretkey):
    #print fun_apikey,fun_secretkey
    data = {
    "grant_type":"client_credentials",
    "client_id":fun_apikey,
    "client_secret":fun_secretkey
    }
    r = requests.post(accesstokenURL,data)
    #print (r.text)
    t = json.loads(r.text)
    
    #print t['access_token']
    at = t['access_token']
    return at
    
    
def response_parse(result_res):
    r = json.loads(result_res)
    #print(r)
    ret = r['error_msg']
    if r['error_code'] != 0:
        print(ret)
        return  r['error_code'], 0

    result_parse= []
    face_list = r['result']['face_list'][0]
    #print face_list
    #print(len(face_list))
    for i in range(len(faceinfo_type)):
        if (faceinfo_type[i] == 'age') or (faceinfo_type[i] == 'beauty'):
            result_parse.append(face_list[faceinfo_type[i]])
        elif faceinfo_type[i] == 'location':
            result_parse.append(face_list[faceinfo_type[i]]['width'])
            result_parse.append(face_list[faceinfo_type[i]]['height'])
            result_parse.append(face_list[faceinfo_type[i]]['top'])
            result_parse.append(face_list[faceinfo_type[i]]['left'])

        else:
            result_parse.append(face_list[faceinfo_type[i]]['type'])
 
    #print("result:%s \nface_type:%s\nface_shape:%s\ngender:%s\nemotion:%s\nglasses:%s\nage:%d\nbeauty:%d\n\
     #      "%(ret,result_parse[faceinfo_type.index('face_type')],result_parse[faceinfo_type.index('face_shape')],\
      #      result_parse[faceinfo_type.index('gender')],result_parse[faceinfo_type.index('emotion')],
       #     result_parse[faceinfo_type.index('glasses')],result_parse[faceinfo_type.index('age')],result_parse[faceinfo_type.index('beauty')]))
    return 0,result_parse

def get_face_response(fun_access_token,base64_imge):
    header = {
    "Content-Type":"application/json"
    }
    data={
    "image":base64_imge,
    "image_type":"BASE64",
    "face_field":"faceshape,facetype,age,gender,glasses,eye_status,emotion,race,beauty"
    }
    url = apiURL + "?access_token="+fun_access_token
    r = requests.post(url,json.dumps(data),header)
    #print (r.url)
    #print (r.text)
    ret=response_parse(r.text)
    return ret
 
def imgeTobase64():
    with open(imge_path,'rb') as f:
        base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    #print("data:imge/jpeg;base64,%s"%s)
    s = s[s.find(',')+1:]
    #print s
    return s

def repeat_nums(arrays):
    """
    list.count(obj):返回元素在列表中出现的次数
    :param arrays: 输入一个列表
    :return:数组里重复次数最多的值
    """
    if (type(arrays)) != list:
        print("输入类型错误，请输入一个列表类型数据")
    else:
        if (len(arrays)) == 0:
            print("该列表是为空")
        else:
            arrays = [x for x in arrays if x !='']
            dict_num = {}
            nums = 0   #列表里重复次数最多的值
            element = 0 #返回列表里重复次数最多的元素
            for item in arrays:
                if item not in dict_num.keys():
                    dict_num[item] = arrays.count(item)
                    if dict_num[item] >= nums:
                        nums = dict_num[item]
                        element = item
            print(dict_num, nums, element)
            return str(element)
        
 
 

 
 
def identify():
    #print ('face identification starting')
    #print access_token
    cap=camer_open()
    E = make_photo(cap)
    return E

# Create your views here.

def random_get(request):
    result = Film.objects.get(title='我不是药神')
    temp_dict = {
        'title': result.title,
        'rating': result.rating,
        'category': '/'.join(result.category),
        'describe': result.describe,
        'short_comment': result.short_comment,
        'actor': ' '.join(result.actor),
    }
    return render(request, 'film.html', temp_dict)
    # a = result.actor
    # return HttpResponse(' '.join(a))


def success(request):

    request.session['emotion'] = category
    return HttpResponseRedirect("recommend")

def home(request):
    return render(request, 'home.html')

def recommend(request):
    user_emotion = identify()
    emotion_dict = {
        'neutral': 1,
        'happy': 2,
        'disgust': 3,
        'sad': 4,
        'surprise': 5,
        'angry': 6,
    }

    category = emotion_dict[user_emotion]
    result = kmean_recom.objects.filter(category=category)
    number = random.sample(range(0, len(result)-1),4)

    temp = []
    for i in number:
        temp_title = result[i].title
        temp.append(Film.objects.get(title=temp_title))

    temp_dict = {'Emotion':user_emotion}
    for i in range(4):
        temp_dict['movie_'+str(i)] = temp[i].title
        temp_dict['describe_'+str(i)] = temp[i].describe[:100] + '...'
        temp_dict['url_'+str(i)] = 'images/' + temp[i].image_url.split('/')[-1]

    return render(request, 'recommend_page.html', temp_dict)


def questionnaire(request):

    temp_dict = {}
    moive_list = ['末代皇帝',
    '无双',
    '飞屋环游记',
    '寻梦环游记',
    '绿皮书',
    '疯狂动物城',
    '我不是药神',
    '那些年，我们一起追的女孩',
    '烈日灼心',
    '你的名字。',
    '哆啦A梦：伴我同行',
    '勇敢的心', 
    '大空头',
    '敦刻尔克',
    '哈利·波特与混血王子',
    '黑客帝国',
    '本杰明·巴顿奇事',
    '阿凡达']
    temp_dict['moive_list'] = moive_list

    movie_select0 = request.POST.get('movie_select0')
    movie_select1 = request.POST.get('movie_select1')
    movie_select2 = request.POST.get('movie_select2')
    movie_select3 = request.POST.get('movie_select3')
    movie_select4 = request.POST.get('movie_select4')
    movie_select5 = request.POST.get('movie_select5')

    if request.method == 'POST':
        deter_0 = kmean_recom.objects.get(title=movie_select0).category
        deter_1 = kmean_recom.objects.get(title=movie_select1).category
        deter_2 = kmean_recom.objects.get(title=movie_select2).category
        deter_3 = kmean_recom.objects.get(title=movie_select3).category
        deter_4 = kmean_recom.objects.get(title=movie_select4).category
        deter_5 = kmean_recom.objects.get(title=movie_select5).category


        temp = {
            'neutral':deter_0,
            'disgust':deter_1,
            'angry':deter_2,
            'surprise':deter_3,
            'sad':deter_4,
            'happy':deter_5,

        }

        if 1 == user.objects.filter(title='user').update(**temp):
            return HttpResponseRedirect('recommend')

    return render(request, 'questionnaire.html',temp_dict)
 #   return render(request, 'questionnaire.html', temp_dict)


def detail(request,name):

    result = Film.objects.filter(title=name)
    if len(result) == 0:
        return HttpResponse("No Result~")
        
    result = result[0]
    temp_dict = {
        'title': result.title,
        'rating': result.rating,
        'category': '/'.join(result.category),
        'describe': result.describe,
        'short_comment': result.short_comment,
        'actor': ' '.join(result.actor),
        'ciyu': 'images/' + result.title+'.jpg',
        'watch_url' : 'https://v.qq.com/x/search/?q=' + result.title + '&stag=0&smartbox_ab='
    }
    # return HttpResponseRedirect('success')
    return render(request, 'detail_page.html', temp_dict)

def search(request):
    message = ''
    if request.method == 'POST':
        title = request.POST.get('film_title')
        # form = SearchForm(request.POST or None)
        # print(title)
        result = Film.objects.filter(title__contains=title)
        if len(result) == 0:
            message = "Sorry, we have not found this film~"
            return render(request, 'search_page.html', {'message': message})
        elif (len(result) == 1) or (result[0].title == title):
            result = result[0]
            temp_dict = {
                'title': result.title,
                'rating': result.rating,
                'category': '/'.join(result.category),
                'describe': result.describe,
                'short_comment': result.short_comment,
                'actor': ' '.join(result.actor),
                'ciyu': 'images/' + result.title+'.jpg',
                'watch_url' : 'https://v.qq.com/x/search/?q=' + result.title + '&stag=0&smartbox_ab='
            }
            return render(request, 'detail_page.html', temp_dict)
        else:
            message = "It seems more than more movies being picked up. Please input the whole name~"
            return render(request, 'search_page.html', {'message': message, 'filmlist': result})
        # if form.is_valid():
        #     # title = form.cleaned_data.get("title")
        #     result = Film.objects.filter(title__contains=title)
        #     if len(result) == 0:
        #         message = "Sorry, we have not found this film~"
        #         return render(request, 'search_page.html', {'form': form, 'message': message})
        #     elif (len(result) == 1) or (result[0].title == title):
        #         result = result[0]
        #         temp_dict = {
        #             'title': result.title,
        #             'rating': result.rating,
        #             'category': '/'.join(result.category),
        #             'describe': result.describe,
        #             'short_comment': result.short_comment,
        #             'actor': ' '.join(result.actor),
        #             'ciyu': 'images/' + result.title+'.jpg',
        #             'watch_url' : 'https://v.qq.com/x/search/?q=' + result.title + '&stag=0&smartbox_ab='
        #         }
        #         # return HttpResponseRedirect('success')
        #         return render(request, 'detail_page.html', temp_dict)
        #     else:
        #         message = "It seems more than more movies being picked up. Please input the whole name~"
        #         return render(request, 'search.html', {'form': form, 'message': message, 'filmlist': result})
    else:
        form = SearchForm()

    # return render(request, 'search_page.html', {'form': form, 'message': message})
    return render(request, 'search_page.html', {'message': message})




#def register(request):
#    return render(request,'detail_page.html') 
