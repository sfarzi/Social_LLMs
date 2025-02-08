![GitHub Repo](https://img.shields.io/badge/Research-Paper-blue)
# **ReQuEST: A Small-Scale Multi-Task Model for Community Question-Answering Systems**
## 📜 Abstract
<p align="justify">
  The burgeoning popularity of community question-answering platforms as an information-seeking strategy has prompted researchers to look for ways to save response time and effort, among which question entailment recognizing, question summarizing, and question tagging are prominent. However, none has investigated the implicit relations between these tasks and the benefits their interaction could provide. In this study, ReQuEST, a novel multi-task model based on bidirectional auto-regressive transformers (BART), is introduced to recognize question entailment, summarize questions respecting given queries, and tag questions with primary topics, simultaneously. ReQuEST comprises one shared encoder representing input sequences, two half-shared decoders providing intermediate presentations, and three task-specific heads producing summaries, tags, and entailed questions. A lightweight fine-tuning technique and a weighted loss function help us learn model parameters efficiently. With roughly 187k learning parameters, ReQuEST is almost half the size of BART<sub>large</sub> and is two-thirds smaller than its multi-task counterparts. Empirical experiments on standard summarization datasets reveal that ReQuEST outperforms competitors on Debatepedia with a Rouge-L of 46.77 and has persuasive performance with a Rouge-L of 37.37 on MeQSum. On MediQA-RQE as a medical benchmark for entailment recognition, ReQuEST is also comparable in accuracy with state-of-the-art systems without being pre-trained on domain-specific datasets.
</p>

## 📊 Results
<p align="justify">
  Table 1  illustrates the train and test results on CQAD-ReQuEST dataset. The evidence in Table 1 supports the claim that ReQuEST performs all its tasks fairly well. The TG performance on test data is improved by about 11% and 2% in Rouge-L and BERTScore metrics, respectively. Furthermore, the test accuracy and F1-Score are both 1% enhanced. In addition, despite a slight degradation in the QFQS performance in terms of Rouge-L, the BERTScore criterion declares preserving the semantic quality of produced summaries. In conclusion, ReQuEST is expected to become more efficient by tuning more and reaching a compromise between tasks.
</p>
<p align="center"><b>Table 1. Analysis of ReQuEST performance after training for ten iterations on CQAD-ReQuEST</b></p>
<table align="center">
  <thead>
    <tr>
      <th rowspan='2'>Data</th>
      <th colspan='4'>RQE</th>
      <th colspan='4'>QFQS</th>
      <th colspan='4'>TG</th>
    </tr>
    <tr>
      <th>Acc</th>
      <th>F1</th>
      <th>Re</th>
      <th>Pr</th>
      <th>BS</th>
      <th>RL</th>
      <th>R1</th>
      <th>R2</th>
      <th>BS</th>
      <th>RL</th>
      <th>R1</th>
      <th>R2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Train</td>
      <td>0.933</td>
      <td>0.931</td>
      <td>0.908</td>
      <td>0.955</td>
      <td>0.899</td>
      <td>0.422</td>
      <td>0.447</td>
      <td>0.288</td>
      <td>0.902</td>
      <td>0.603</td>
      <td>0.634</td>
      <td>0.481</td>
    </tr>
    <tr>
      <td>Test</td>
      <td>0.900</td>
      <td>0.900</td>
      <td>0.886</td>
      <td>0.914</td>
      <td>0.885</td>
      <td>0.350</td>
      <td>0.376</td>
      <td>0.213</td>
      <td>0.898</td>
      <td>0.606</td>
      <td>0.636</td>
      <td>0.492</td>
    </tr>
  </tbody>
</table>

  <p align="justify"><sub><b>Notes:</b>
  Acc: Accuracy, F1: F1-Score, Re: Recall, Pr: Precision, BS: BERTScore, RL: Rouge-L, R1: Rouge-1, R2: Rouge-2
  </sub>
  </p>

  <p align="justify">
  <br>Table 2 summarizes the assessment results on the MediQA-RQE dataset. As Table 2 indicates, even pre-trained transformers on biological data, i.e., BioBERT, are beaten by the ReQuEST.
  </p>
  <p align="center"><b>Table 2. Comparative analysis of some recently developed models on the MEDIQA-RQE test set</b></p>
  
<table align="center">
  <thead>
    <tr>
      <th>Ref.</th>
      <th>Model</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Lamurias & Couto, 2019</td>
      <td>BioBERT + Named entity recognition</td>
      <td>48.5</td>
    </tr>
    <tr>
      <td>Nguyen et al., 2019</td>
      <td>Ensemble approach (BERT + BioBERT + SVM)</td>
      <td>48.9</td>
    </tr>
    <tr>
      <td>Bandyopadhyay et al., 2019</td>
      <td>Gensim Word2Vec + Siamese Network of Bidirectional LSTM</td>
      <td>53.2</td>
    </tr>
    <tr>
      <td></td>
      <td><strong>ReQuEST</strong></td>
      <td>52.2 <br>(F1 = 60.1)</td>
    </tr>
  </tbody>
</table>

  
  <p align="justify"><sub><b>Notes:</b>
  We supposed the γ coefficient equals 0, and then examined ReQuEST performance with different combinations of α∈{0.1,⋯,0.9,1} and β∈{0,0.1,⋯,0.9} coefficients. The reported result is the best one which was obtained with α=0.5 and β=0.5, though other results were not much different.
  </sub>
  </p>

  <p align="justify">
  <br>Table 3 compares the performance of ReQuEST on the MeQSum dataset with several recent models. It signifies the superiority of ReQuEST over BART, PEGASUS, and their ensemble model in terms of BERTScore and Rouge metrics (with recall-based values in parentheses). In addition, gaining great BERTScore values indicates that summaries are well-generated, conveying the meaning of target sentences. Overall, the evidence confirms the effectiveness of multi-task learning for the QS task.
  </p>
  <p align="center"><b>Table 3. The performance comparison of some recently developed models on MEQSUM test set</b></p>
  
  <table align="center">
  <thead>
    <tr>
      <th>Ref.</th>
      <th>Model</th>
      <th>BS</th>
      <th>RL</th>
      <th>R1</th>
      <th>R2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Balumuri et al., 2021</td>
      <td>BART</td>
      <td>70.25</td>
      <td>30.77</td>
      <td>33.31</td>
      <td>13.93</td>
    </tr>
    <tr>
      <td>Sänger et al., 2021</td>
      <td>PEGASUS</td>
      <td>69.96</td>
      <td>31.49</td>
      <td>33.40</td>
      <td>15.99</td>
    </tr>
    <tr>
      <td>Y. He et al., 2021</td>
      <td>Ensemble approach + Re-ranking + Error correction</td>
      <td>68.98</td>
      <td>31.31</td>
      <td>35.14</td>
      <td>16.08</td>
    </tr>
    <tr>
      <td></td>
      <td><strong>ReQuEST</strong></td>
      <td>90.73 <br>(90.79)</td>
      <td>37.34 <br>(44.39)</td>
      <td>40.45 <br>(48.34)</td>
      <td>24.56 <br>(29.69)</td>
    </tr>
  </tbody>
</table>

  
  <p align="justify"><sub><b>Notes:</b>
  Plenty of experiments were carried out using various coefficients, from which α=0.3, β=0.7, and γ=0 provided the best fit.
  </sub>
  </p>

  <p align="justify">
  <br>Table 4 illustrates a performance comparison between ReQuEST and some competitors using the Debatepedia dataset. It is evident from this table that ReQuEST ranks the best in terms of Rouge-L. In addition, due to the simultaneous high values of Rouge-L and Rouge-1, it appears that ReQuEST can recover a considerable fraction of reference tokens in the same order. At the same time, Rouge-2 is less than a third, which means ReQuEST does not oblige itself to capture adjacent words. In contrast, it brings up to 90% BERTScore, which informs the high semantic quality of the created summaries. 
  </p>
  <p align="center"><b>Table 4. The performance comparison of some recently developed models on Debatepedia test set</b></p>
  
<table align="center">
  <thead>
    <tr>
      <th>Ref.</th>
      <th>Model</th>
      <th>RL</th>
      <th>R1</th>
      <th>R2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Nema et al., 2017</td>
      <td>Soft LSTM-based diversity attention</td>
      <td>40.43</td>
      <td>41.26</td>
      <td>18.75</td>
    </tr>
    <tr>
      <td>Aryal & Chali, 2020</td>
      <td>Seq-to-seq + LSTM + selection mechanism</td>
      <td>42.73</td>
      <td>43.22</td>
      <td>27.40</td>
    </tr>
    <tr>
      <td>Abdullah & Chali, 2020</td>
      <td>BERTSUM + Query relevance</td>
      <td>44.07</td>
      <td>47.16</td>
      <td>27.48</td>
    </tr>
    <tr>
      <td>Baumel et al., 2018</td>
      <td>Sequence-to-sequence + Query relevance + pointer generator</td>
      <td>46.18</td>
      <td>53.09</td>
      <td>16.10</td>
    </tr>
    <tr>
      <td></td>
      <td><strong>ReQuEST</strong></td>
      <td>46.77 <br>(47.30)</td>
      <td>47.87 <br>(48.45)</td>
      <td>27.71 <br>(28.00)</td>
    </tr>
  </tbody>
</table>

  
  <p align="justify"><sub><b>Notes:</b>
  In this experiment, the coefficients α, β, γ, ρ, and τ were randomly initialized with 0.3, 0.4, 0.3, 0.5, and 0.5, respectively.
  </sub>
  </p>

</p>

## 📌 Citation

If you use this work, please cite our [paper](https://ieeexplore.ieee.org/abstract/document/10413543) as follows:

```bibtex
@ARTICLE{10413543,
  author  = {Aftabi, Seyyede Zahra and Seyyedi, Seyyede Maryam and Maleki, Mohammad and Farzi, Saeed},
  title   = {ReQuEST: A Small-Scale Multi-Task Model for Community Question-Answering Systems},
  journal = {IEEE Access}, 
  year    = {2024},
  volume  = {12},
  pages   = {17137-17151},
  doi     = {10.1109/ACCESS.2024.3358287}
}
```
