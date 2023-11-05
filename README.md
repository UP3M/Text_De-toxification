# Detoxification
Detoxification is an automatic transformation of a text such that:
- text becomes non-toxic
- the content of the text stays the same.

If you want the fastest way to run the inference of these models, you can run visualization.py

## Parallel detoxification corpus

The original ParaNMT corpus (50M sentence pairs) can be downloaded from the authors page: https://www.cs.cmu.edu/~jwieting/. 
The filtered ParaNMT-detox corpus (500K sentence pairs) can be downloaded from [here](https://github.com/skoltech-nlp/detox/releases/download/emnlp2021/filtered_paranmt.zip). Original datasets data explanatory/visualization can be found in notebook initial-data-exporation.ipynb

## Data preprocessing and Training
The original dataset is transformed using make_dataset.py the result "interim.tsv" then trained using t5_train.py. The saved model then can be used to predict the test set using t5_predict.py. 

## Trained model
you can access the model here:  https://drive.google.com/drive/folders/1FoKy7AxV-7UOYk8g4iZYz-ytGLBbB2th?usp=sharing
Make sure to load it before run the code or notebook

## Evaluation

To evaluate your model, use evaluation notebook. 

First, you need to have the predicted dataset generated by t5_predict.py. 

Then run the script `6-evaluation.ipynb`.


## References
```
@inproceedings{dale-etal-2021-text,
    title = "Text Detoxification using Large Pre-trained Neural Models",
    author = "Dale, David  and
      Voronov, Anton  and
      Dementieva, Daryna  and
      Logacheva, Varvara  and
      Kozlova, Olga  and
      Semenov, Nikita  and
      Panchenko, Alexander",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.629",
    pages = "7979--7996",
}
```
