import streamlit as st
import re
import pandas as pd
import os 
import itertools
from collections import Counter
from io import StringIO

f_path = 'C:/Users/kmc59/Downloads' # 파일이 저장되어 있는 경로를 넣어주세요.
f_name = 'test (1).txt' # 파일 이름을 넣어주세요.

def katalk_msg_parse(file):
    my_katalk_data = list()
    katalk_msg_pattern = "[0-9]{4}[년.] [0-9]{1,2}[월.] [0-9]{1,2}[일.] 오\S [0-9]{1,2}:[0-9]{1,2},.*:"
    date_info = "[0-9]{4}년 [0-9]{1,2}월 [0-9]{1,2}일 \S요일"
    in_out_info = "[0-9]{4}[년.] [0-9]{1,2}[월.] [0-9]{1,2}[일.] 오\S [0-9]{1,2}:[0-9]{1,2}:.*"

    for line in file :
        if re.match(date_info, line) or re.match(in_out_info, line):
            continue
        elif line == '\n':
            continue
        elif re.match(katalk_msg_pattern, line):
            line = line.split(",")
            date_time = line[0]
            user_text = line[1].split(" : ", maxsplit=1)
            user_name = user_text[0].strip()
            text = user_text[1].strip()
            my_katalk_data.append({'time': date_time,
                                   'name': user_name,
                                   'text': text
                                   })

        else:
            if len(my_katalk_data) > 0:
                my_katalk_data[-1]['text'] += "\n"+line.strip()

    my_katalk_df = pd.DataFrame(my_katalk_data)

    return my_katalk_df

st.set_page_config(
    layout="wide",
    page_title="3502화작수행평가",
    page_icon="🥲",
    )
col1, empty1, col3, col4, empty2 = st.columns([4,1,2,2,1])
empty3, col5, col6,  empty3 = st.columns([1,5,5,1])

col1.title('Count')
col1.markdown('카카오톡 대화 내용을 바탕으로 욕설과 혐오표현 사용 빈도를 알려줍니다.')

with col1 :
  rl = st.file_uploader("파일 선택[txt]", type=['txt'])
  stname = st.text_input('카톡방에서 사용하는 이름을 입력해주세요')

with col5 : 
    st.info('본 프로그램은 띄어쓰기를 기준으로 단어를 찾아내기 때문에 조사가 붙은 혐오표현은 찾아내지 못합니다. (ex : 짱개 (O), 짱개가(X) 따라서, 실제 쓰는 혐오표현의 수보다 적은 수의 혐오표현이 사용되었다고 뜰 수 있습니다.')
    st.info('파일은 txt 파일만 업로드 할 수 있으며, 카카오톡 채팅방에서 메뉴창(- 세 개) -> 설정(톱니바퀴 모양) - > 대화 내용 내보내기 -> 텍스트만 보내기 를 통해 txt 파일을 다운로드 할 수 있습니다.')

with col6 :
    st.error('만약 에러코드가 뜬다면, 자신의 핸드폰 설정 언어가 한글이 아닌지(설정언어가 한글이 아니라면 내보내기 한 대화 내용의 txt 파일 형식이 달라집니다), txt파일이 잘못되지 않았는지 살펴보십니오. 또한, 자신의 이름을 입력하지 않으면 카톡방 전체에서 사용된 욕설/혐오표현의 개수가 표시됩니다. ')



if rl is not None:
    ext = rl.name.split('.')[-1]
    if ext == 'txt':
        bytes_data = rl.getvalue()
        rl_1 = StringIO(bytes_data.decode("utf_8"))
        df = katalk_msg_parse(rl_1)
        df_1= df.drop(['time'],axis=1)
        df_2= df_1[df_1['name'].str.contains(stname)]
        df_3 =df_2.drop(['name'],axis=1)

        say=df_3.values
        say_list = say.tolist()
        list_1 = list(itertools.chain.from_iterable(say_list))
        result = ' '.join(str(s) for s in list_1)

        ssfinal = result.split()
        sfinal=Counter(ssfinal)

        final_1 = sfinal['ㅅㅂ']
        final_2 = sfinal['시발']
        final_3  =sfinal['존나']
        final_4 = sfinal['짱개']
        final_5 = sfinal['병신']
        final_6 = sfinal['ㅂㅅ']
        final_7 = sfinal['걸레']
        final_8 = sfinal['게이야']
        final_9 = sfinal['꼴페미']
        final_10 = sfinal['잼민이']
        fianl = [['ㅅㅂ',final_1],['시발',final_2],['존나',final_3],['야',final_4]]
        col3.metric("'ㅅㅂ 사용 빈도", int(final_1), )
        col3.metric("'시발' 사용 빈도",int(final_2),) 
        col3.metric("'존나' 사용 빈도", int(final_3), )
        col3.metric("'짱개' 사용 빈도",int(final_4),) 
        col3.metric("'병신' 사용 빈도", int(final_5),)
        col4.metric("'ㅂㅅ' 사용 빈도", int(final_6),)
        col4.metric("'걸레' 사용 빈도", int(final_7),)
        col4.metric("'게이야' 사용 빈도", int(final_8),)
        col4.metric("'꼴페미' 사용 빈도", int(final_9),)
        col4.metric("'잼민이' 사용 빈도", int(final_10),)


        