## Building a Retrieval-Augmented Generation (RAG) System

CRAG (Corrective Retrieval Augmented Generation) is a project that enhances text generation through retrieval-augmented methods, leveraging multiple APIs for improved performance and accuracy using GPT-4o for the generation component

This project was developed using Python 3.10.12, following the instructions outlined in the document '*DS_Exam_Huma2024.pdf*', which is located in the main directory of this project.

### Project structure

The project is organized in Jupyter notebooks as structured in the '*DS_Exam_Huma2024.pdf*' file:
1. **Section 1: Understanding the Dataset**: In the directory 'Section_1_DataClean'.
2. **Section 2: Setting Up the Retrieval System**: In the directory 'Section_2_RAG'.
3. **Section 3: Integrating the Generation Component**: In the directory 'Section_3_Generation'.
4. **Section 4: Evaluation and Optimization**: In the directory 'Section_4_Eval'.
5. **Section 5: Reporting and Documentation**: In the directory 'Section_5_FinalReport'.
6. **Section 6: Expanding the RAG System to the Internet**: In the directory 'Section_6_Web'.

All scripts used are located in the 'Scripts' folder, the provided dataset is in the 'Dataset' folder, and there is a text file with all the questions from the dataset answered by the CRAG system. The text files with the API keys are located in the 'APIS' folder.


### Instructions

In order to execute all notebooks and scripts within the project, please install the dependencies listed in your enviroment the `requirements.txt` file.

```
pip install -r requirements.txt
```

Additionally, you will need to generate three API keys and save them in their respective text files within the `APIS` directory:

- Gemini: [Gemini Api](https://ai.google.dev/gemini-api/docs/api-key) -> Save in `Gemini.txt`
- GPT: [GPT Api](https://platform.openai.com/api-keys) -> Save in `gpt.txt`
- Serper: [Serper Api](https://serper.dev/api-key) -> Save in `serper.txt`

### Executing CRAG

To invoke the CRAG with web search functionality, execute the following command in a terminal from the `Scripts` folder:

```bash
~/CRAG/Scripts/$ python3 CRAG.py "query"
```
*query* is the prompt or question to evaluate the CRAG: Example:
```bash
~/CRAG/Scripts/$ python3 CRAG.py "What is Keytruda?"
```


### Cite
```bibtex
@article{yan2024corrective,
  title={Corrective Retrieval Augmented Generation},
  author={Yan, Shi-Qi and Gu, Jia-Chen and Zhu, Yun and Ling, Zhen-Hua},
  journal={arXiv preprint arXiv:2401.15884},
  year={2024}
}
```

[Corrective Retrieval Augmented Generation paper](https://arxiv.org/abs/2401.15884)

> Alan García Zermeño.
06/16/2024



