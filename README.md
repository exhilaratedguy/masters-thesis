<h3 align="center"> PT  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Portugal.svg/2560px-Flag_of_Portugal.svg.png" alt="PT Flag" width="22"/>
</h3>
  
<h1 align="center"> Interações Gestuais para Plataformas de Streaming de Vídeo </h1>
Este trabalho propõe uma nova abordagem para controlo, à distância, de aplicações de streaming de vídeo. A aplicação desenvolvida nesta dissertação procura um meio mais natural de interação com este tipo de plataformas usando interações gestuais, captadas pela câmara de profundidade RealSense D435. Câmaras de profundidade, ao contrário de câmaras de vídeo comuns, utilizam um fluxo de luz infravermelha para determinar a distância dos objetos relativamente à câmara. A câmara utilizada neste projeto possui capacidades de captura tanto neste modo, como no modo comum RGB.  
<br><br>
Foi criada de raiz uma interface gráfica inspirada pela plataforma Netflix, para permitir o controlo dos seus botões e os vídeos reproduzidos, programaticamente. Foram desenvolvidos dois protótipos com tecnologias distintas para interagir com a interface. O primeiro, utiliza métodos de tratamento de imagem para retirar a informação pretendida, e um modelo pré-treinado de reconhecimento de gestos para identificar o gesto realizado. O segundo, integra um modelo de deteção e classificação de objetos otimizado para deteção e rastreamento de mãos entre frames. Foram feitas análises experimentais entre ambos e selecionado o segundo protótipo para prosseguir a testes com utilizadores.
<br><br>
<b><i>(o projeto carregado para este repositório apenas contém o protótipo final, que utiliza a framework MediaPipe e o feed RGB da câmara conectada)</i></b>

<br><br>

<h3 align="center"> EN  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Flag_of_the_United_Kingdom_%282-3%29.svg/1200px-Flag_of_the_United_Kingdom_%282-3%29.svg.png" alt="UK Flag" width="22"/>
</h3>

<h1 align="center"> Gestural Interactions for Video Streaming Platforms </h1>
This work proposes a new approach to interacting with video streaming applications from afar. The program developed for this dissertation looks for a more natural way of controlling these services by using gestural interactions, which are captured by the depth camera RealSense D435. Depth cameras, unlike regular video cameras, use an infrared feed to determine the distance of objects in frame, relative to the camera. The camera used in this project offers both infrared and RGB capturing modes.
<br><br>
A graphical interface, inspired by streaming platform Netflix, was created from scratch to allow control over its buttons and the video displayed programmatically. Two prototypes to interact with the GUI were developed using distinct technologies. The first one only uses image treatment methods to get the desired data and a pre-trained model for gesture recognitions to identify the gesture performed. The second one integrates an object detection and classification model optimized for hand detection and tracking between frames. Experimental analyses were run to compare both prototypes, resulting on the second being selected to proceed to the user tests stage.
<br><br>
<b><i>(the project uploaded onto this repo contains only the final prototype, which uses the MediaPipe framework and the RGB feed of the connected camera)</i></b>

<br><br><br>

## About my thesis

If you want to read through the whole process and learn about the different methods and technologies used in this and other prototypes, you can find my Master's Thesis on [University of Madeira's online repo](https://digituma.uma.pt/handle/10400.13/3845 "DigitUma"). Alternatively, you can get it off this GitHub repo ([here](https://docs.google.com/viewer?url=https://raw.githubusercontent.com/exhilaratedguy/masters-thesis/cdddd6fb2f6930879254a94abb372a46ffe53f10/Interacoes_Gestuais_para_Plataformas_de_Streaming_de_Video.pdf "Interações Gestuais para Plataformas de Streaming de Vídeo")) as well.

<br>

## Requirements and installation

1. Make sure you are running Python 3.7 (it doesn't work with 3.8 and I haven't tested with older major releases)
2. Download and install [K-Lite Codec Pack](https://codecguide.com/download_kl.htm)
3. Pull the project and run `pip install -r requirements.txt` on its directory
4. Run `main.py`
