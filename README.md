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
