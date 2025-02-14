import streamlit as st
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings  # 라마 인덱스의 환경 설정을 해주는 라이브러리 이것을 안하면 오픈API 를 사용한다.

import os



# ============================================= 임베드 셋팅 시작 ======================================================
def get_huggingface_tonken() :
    token=st.secrets.get('HUGGINGFACE_API_TOKEN')
    return token

#모델 셋팅(라마)+ 토크나이저생성 함수
@st.cache_resource    # 스트림릿아 매번 불러 오지 말고 한번 다운로드 받았으면 캐쉬에서 써라 (다운받아 써라 계속 다운 받지 말고)
def initialize_models() :
    # 두개의 값은 허깅 페이스에서 받아올 예정이다.( 무료 모델 사용을 위해서 )
    model_name = "mistralai/Mistral-7B-Instruct-v0.2" # <<== 언어 모델 이름 (그나마 한국어 처리 잘 한다.)

    token = get_huggingface_tonken()
    llm = HuggingFaceInferenceAPI(
        model_name = model_name,
        max_new_tokens = 512,
        temperature = 0,
        system_prompt = '''당신은 한국어로만 대답 하는 AI 어시스턴트 입니다.
        주어진 질문에 대해서만 한국어로 명확하고 정확하게 답변해주세요. 
        응답의 마지막 부분은 단어로 끝내지말고 문장으로 끝내도록 해주세요''',
        token = token
        # 스트림릿에 퍼블릿으로 코드를 공개 하는데 이런 경우에 토큰이 노출 되어 해킹 같은 보안 취약점이 발생하기에 
        # 절대 토큰을 그대로 올리면 안된다.
        # 스트림릿에 크리에잍 에서 셋팅 할떄 보면 시크릿 파일로 만들어 주는 기능이 있따.
        # Secrets
        # Provide environment variables and other secrets to your app using TOML format. 
        # This information is encrypted and served securely to your app at runtime. 
        # Learn more about Secrets in our docs. Changes take around a minute to propagate.
    )

    # 허킹페이스 임버트를 가져올것이다 ( 토크나이져)
    # 마이크로 소프트에서 만든 임베딩 모델 
    embed_model_name = "sentence-transformers/all-mpnet-base-v2"
    embed_model = HuggingFaceEmbedding(model_name = embed_model_name)
    # 이제 다 가져왔으니까 셋팅을 해야 한다. 
    # 라마인덱스에 알려줘야 한다 우리는 이것을 쓸 것이라는 것을 
    Settings.llm = llm
    Settings.embed_model = embed_model
    # 임베드 모델은 위에 작성한 임베드 모델로 셋팅을 해줘야 안한다.
    
# ============================================= 임베드 셋팅 끝 ======================================================



def main():
    # 1. 사용할 모델 셋팅 (아무것도 안해도 디폴트 값이 쳇 GPT 모델 )
    # 2. 사용할 토크나이저 셋팅 : embad_model   (아무것도 안해도 디폴트 값이 쳇 GPT 모델 )
    # 3. PAG 에 필요한 인덱스 셋팅
    # 4. 유저에게 프롬프트 입력 받아서 응답
    initialize_models()
    # 함수를 만드면 테스트를 꼭 해봐라 ( 함수단위로 테스트 하는 것을 유닛 테스트 라고 한다.)

    st.title("PDF 문서 기반 질의 응답")
    st.text("선진기업 복지 업무 메뉴얼을 기반으로 질의응답을 제공 합니다.")
    # 이러한 과장들은 이력서나 면접을 볼때 꼭 이야기를 해야 한다.
if __name__ == '__main__' :
    main()
    

    # st.