# Example Runner

## Setup
Make sure to download and unzip the Spider dataset from the [Spider website](https://drive.google.com/file/d/1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J/view) to th `local_data` directory. This is used for the topic generation example. Make sure to download the KaggleDBQA dataset from the [KaggleDBQA repository](https://github.com/Chia-Hsuan-Lee/KaggleDBQA) and place it in the `local_data` directory.

This project uses [Poetry](https://python-poetry.org/) for dependency management. This project was written using [Python 3.12.3](https://www.python.org/downloads/release/python-3120/). Ensure that you have installed the necessary packages for SynQL, and activate the environment. You can do this using poetry:

```bash
cd synql

poetry install

poetry shell

cd ..

cd runner
```

Make sure you have set your `.env` file at the root of the project with the following variables:
```markdown
OPENAI_API_KEY=<Your API Key Here>
```

## Topic Generation
To generate topics for a given dataset, you can use the `topic.py` script. We have provided an example script that uses the Spider dataset.

```bash
python topic.py --config configs/topic_example.json
```

This will generate topics for the Spider dataset and save them to the `local_data` directory.

## Joint Generation
We have two examples of joint generation: one for batch generation and the other for real-time generation. Batch generation is useful for generating a large number of examples at once at a discounted inference cost ([see here](https://platform.openai.com/docs/guides/batch)), while real-time generation is useful for generating examples on-the-fly. 

### Real-Time Generation
```bash
python joint.py --config configs/joint_example.json
```

### Batch Generation
```bash
python batch.py --config configs/batch_example.json
```