목요일에 해보다가 포기하고 토요일에 침착하게 다시 오픈클로를 켜줍니다.

일단 Node.js와 오픈클로를 설치를 설치까지는 다 한 상태라고 가정!!

`openclaw --version` 을 터미널에 입력했을 때 뭐 숫자가 나오면 설치 자체는 잘된 거!!

### 다시 설정하기(온보딩)
`openclaw onboard --install-daemon` 로 설정 켜기

1. 약관 어쩌구 yes

2. QuickStart

3. Update values
기존에 정해둔 설정을 바꿀 거라 update로 선택

4. Model : Google

5. Google Gemini API key
`https://aistudio.google.com` 여기에서 API키 받고, paste 해주기

6. Default Model : google/gemini-2.5 flash
keep current 였나 이걸로 하면 프로 모델이라 돈을 넣어야만 대화를 해준다!

나는 거지이므로 기본 모델로 해준다.

7. Select Channel : Discord
이건... 다르게 해도 될 것 같지만 그나마 친숙한 디스코드로 했다.
그리고 이것도 API키 받고 붙여넣기!

8. Configure skills now? : NO
skill들 추가하는 건데 이것까지 하면 굉장히 귀찮아질 것 같으니 일단은 생략

나중에 다시 추가하면 되니까 아마 괜찮을 것이다!

9. Hook도 생략

10. Gateway : Reinstall 
다시 설치하니까 기존에 설정해둔 openai와 충돌하는 것 같아서 게이트웨이도 다시 설치했다.

11. 끝! 
위에 막 뜨는 LLM error: {} 가 되게 미심쩍어 보이긴 하지만 일단 대화는 된다!

"hello"라고 적은 텍스트 파일을 Desktop (바탕화면)에 만들어달라고 하면 실제로 만들어준다!!!
