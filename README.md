# SynQL
SynQL is a tool for synthetically generating Text-to-SQL Question-Query Pairs (QQPs). This project is based on the SynQL paper, which we recommend reading for a detailed explanation of the methodology.

## Data 
We have previously used the SynQL method to generate the following datasets:
| Dataset | Description | Link |
| --- | --- | --- |
| SynQL-Spider-Train | Synthetically generated data based on the Spider training split | [Download](https://huggingface.co/datasets/semiotic/SynQL-Spider-Train) | 
| SynQL-KaggleDBQA-Train | Synthetically generated data based on the KaggleDBQA training split | [Download](https://huggingface.co/datasets/semiotic/SynQL-KaggleDBQA-Train) |

## Model
We have previously used data generated using the SynQL method to train the following models:
| Model | Dataset | Description | Link |
| --- | --- | --- | --- |
| T5-3B | SynQL-Spider-Train | T5-3B model finetuned on SynQL-Spider-Train | [Download](https://huggingface.co/semiotic/T5-3B-SynQL-Spider-Train-Run-00) |
| T5-3B | SynQL-KaggleDBQA-Train | T5-3B model finetuned on SynQL-Spider-Train | [Download](https://huggingface.co/semiotic/T5-3B-SynQL-KaggleDBQA-Train-Run-00) |

## Setup 
This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies, run:

```bash
cd synql

poetry install
```

## Getting Started
Checkout the [runner](runner) directory for examples on how to synthesize QQPs using SynQL.