# -*- coding: utf-8 -*-
"""Data_Preparation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k8WprvAMnHmKK63QsA9BT3RYPI9UrGEH
"""

def Preprocess_Text (txt, txttype='S'):
    dropORnot = False
    if (txttype == 'T'):
        txt = " ".join(txt)
        filtered_sentence = txt.replace('-', ' ')
        if len(filtered_sentence)<1:
          dropORnot = True
    else:
        txt = txt.replace('-', ' ')
        txt = txt.replace('\n', ' ')
        txt = txt.replace('“', ' ')
        txt = txt.replace('”', ' ')
        txt = re.sub(r'http\S+', '', txt, flags=re.MULTILINE)
        new_txt = txt.translate(str.maketrans('', '', string.punctuation))
        new_txt = nltk.word_tokenize(new_txt)
        if len(new_txt)<1:
          dropORnot = True
        filtered_sentence = ' '.join(new_txt)
        filtered_sentence = filtered_sentence.lower()
    return filtered_sentence, dropORnot



def Preprocess_Data(Data):
    Remove_list = []
    Check_list = ['long_text',
                  'short_text',
                  'long_text_title',
                  'long_text_tags',
                  'short_text_tags'
                  ]
    for index,row in Data.iterrows():
        for i, C in enumerate(Check_list):
            txttype = 'T' if i>2 else 'S'
            filtered_sentence, dropORnot = Preprocess_Text(row[C], txttype)
            if (dropORnot):
              Remove_list.append(index)
            else:
              Data.at[index, C] = filtered_sentence

    return Data



class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, pad_token_id):
        self.data = data
        self.tokenizer = tokenizer
        self.pad_tID = pad_token_id
        self.max_len, self.max_len_tag, self.max_len_Q1 = self.Calc_Max_Length()
        self.labels = [0, 1]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.loc[idx]
        label = self.labels.index(row[5])

        # ================ Tokenization for RQE ==============
        Q1Q2_Tokenized = self.tokenizer(
            row[0],
            row[1],
            max_length = 2 * self.max_len,
            padding = 'max_length'
            )

        # =========== Tokenization for Tag Generation ========
        Q1_Tokenized = self.tokenizer(
            row[0],
            max_length = self.max_len_Q1,
            padding='max_length'
            )
        Q1_Tags_Tokenized = self.tokenizer(
            row[3],
            max_length = self.max_len_Q1,
            padding='max_length'
            )
        Q1_Tags_input_ids = [-100 if t == self.pad_tID
                              else t for t in Q1_Tags_Tokenized["input_ids"]]

        # =========== Tokenization for Summarization =========
        SUM_Size = self.max_len + self.max_len_tag + 5
        if (label == 0):
          Q1Tags_Tokenized = self.tokenizer(
              row[0],
              row[3],
              max_length = SUM_Size,
              padding='max_length'
              )
          Q1Title_Tokenized = self.tokenizer(
              row[4],
              max_length = SUM_Size,
              padding='max_length'
              )
          Summary_input_ids = [-100 if t == self.pad_tID
                                  else t for t in Q1Title_Tokenized["input_ids"]]
        else:
          Q1Tags_Tokenized = self.tokenizer(
              row[0],
              row[2],
              max_length = SUM_Size,
              padding='max_length'
              )
          Q2_Tokenized = self.tokenizer(
              row[1],
              max_length = SUM_Size,
              padding='max_length'
              )
          Summary_input_ids = [-100 if t == self.pad_tID
                                  else t for t in Q2_Tokenized["input_ids"]]

        return torch.tensor(Q1_Tokenized['input_ids']),\
            torch.tensor(Q1_Tokenized['attention_mask']),\
            torch.tensor(Q1Q2_Tokenized['input_ids']),\
            torch.tensor(Q1Q2_Tokenized['attention_mask']),\
            torch.tensor(Q1Tags_Tokenized['input_ids']),\
            torch.tensor(Q1Tags_Tokenized['attention_mask']),\
            torch.tensor(Summary_input_ids),\
            torch.tensor(Q1_Tags_input_ids),\
            torch.tensor(label)

  def Calc_Max_Length(self):
      Q1 = self.data['long_text'].tolist()
      Q2 = self.data['short_text'].tolist()
      Q2_Tags = self.data['short_text_tags'].tolist()
      Q1_Tags = self.data['long_text_tags'].tolist()


      Q1_Tokenized = self.tokenizer(
          Q1, padding='longest', return_tensors='pt'
          )
      Q2_Tokenized = self.tokenizer(
          Q2, padding='longest', return_tensors='pt'
          )
      Q2Tags_Tokenized = self.tokenizer(
          Q2_Tags, padding='longest', return_tensors='pt'
          )
      Q1Tags_Tokenized = self.tokenizer(
          Q1_Tags, padding='longest', return_tensors='pt'
          )

      max_len_Q1 = Q1_Tokenized['input_ids'].shape[1]
      max_len_Q2 = Q2_Tokenized['input_ids'].shape[1]
      max_len_tag = max([Q1Tags_Tokenized['input_ids'].shape[1],
                        Q2Tags_Tokenized['input_ids'].shape[1]])
      max_len = max([Q1_Tokenized['input_ids'].shape[1],
                    Q2_Tokenized['input_ids'].shape[1]])

      print("max_len     ==> " + str(max_len))
      print("max_len_tag ==> "+ str(max_len_tag))
      print("max_len_Q1  ==> "+ str(max_len_Q1))

      return max_len, max_len_tag, max_len_Q1



class CustomDataModule(pl.LightningDataModule):
    def __init__(self,
                 MyData,
                 tokenizer,
                 pad_token_id,
                 batch_size = 16,
                 split_ratio = [0.8, 0.1, 0.1],
                 stage=None):
        super().__init__()
        self.split_ratio = split_ratio
        self.batch_size = batch_size
        self.train_dataset = None
        self.test_dataset = None
        self.val_dataset = None
        self.MyData = MyData
        self.tokenizer = tokenizer
        self.pad_id = pad_token_id

    def setup(self, stage=None):
        PreparedData = CustomDataset(self.MyData, self.tokenizer, self.pad_id)
        seed = torch.Generator().manual_seed(42)
        len_tr = int(self.split_ratio[0] * len(PreparedData))
        len_te = int(self.split_ratio[1] * len(PreparedData))
        len_va = len(PreparedData) - len_tr - len_te
        self.train_dataset, self.test_dataset, self.val_dataset = random_split(
            PreparedData, [len_tr, len_te, len_va], generator=seed
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            sampler = SequentialSampler(self.train_dataset),
            batch_size = self.batch_size
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            sampler = SequentialSampler(self.val_dataset),
            batch_size = self.batch_size
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            sampler = SequentialSampler(self.test_dataset),
            batch_size = self.batch_size
        )