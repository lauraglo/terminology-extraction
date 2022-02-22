# terminology-extraction
This repository contains the algorithm and preprocessed dataset used in the Master Thesis "New Deep Learning techniques to terminology extraction in specific domains"

-------
PRUEBAS
Comando (Cambiar embedding) :  python replica.py --num_epochs 100 --embedding Bert --rnn_layers 2

-Bert (ERROR) -> Error en entrenamiento, encuentra un string '' que no está en el diccionario
-TransformersXL (OK)
-RoBERTa (ERROR) -> Mismo error que Bert 
-ELMo (ERROR) -> Error al instalar: pip install allennlp==0.9.0
-XLNet: (OK)

-------
Cómo mejorar los resultados:
Probar cambiando los hiperparámetros usando una optimización Bayesiana:
https://www.analyticsvidhya.com/blog/2021/05/tuning-the-hyperparameters-and-layers-of-neural-network-deep-learning/#:~:text=The%20hyperparameters%20to%20tune%20are,tune%20the%20number%20of%20layers.
